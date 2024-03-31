from django import  forms
from project.models import  Project,Category,Tag,Project_Report,Comment_Report
from datetime import datetime
from django.forms.widgets import NumberInput

class Project_ModelForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Title", "class": "form-control"})
    )
    
    details = forms.CharField( 
        widget=forms.Textarea(attrs={"placeholder": "Details", "class": "form-control"}),
    )
    
    total_target = forms.FloatField(
        widget=forms.NumberInput(attrs={"placeholder": "Total Target", "class": "form-control"})
    )

    start_date = forms.DateField(
        widget=NumberInput(attrs={"placeholder": "Start Date", "type": "date", "class": "form-control"}),
        required=False,
        initial=datetime.now().date()
    )
    end_date = forms.DateField(
        widget=forms.NumberInput(attrs={"placeholder": "End Date", "type": "date", "class": "form-control"})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"placeholder": "Project Category", "class": "form-control"})
    )
   
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        required=False
    )

    class Meta:
        model = Project
        fields = ('title', 'details', 'total_target', 'start_date', 'end_date', 'category', 'tag')
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        elif Project.objects.filter(title=title).exists() and self.instance.title != title:
            raise forms.ValidationError("A project with this title already exists.")
        return title

    def clean_total_target(self):
        total_target = self.cleaned_data.get('total_target')
        if total_target is not None and total_target <= 0:
            raise forms.ValidationError("Total Target must be a positive number.")
        return total_target

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        today_date = datetime.now().date()
  
        if (start_date) and today_date > start_date:
            self._errors["start_date"] = self.error_class(["Start date should be greater than Today date"])

        if today_date > end_date:
            self._errors["end_date"] = self.error_class(["End date should be greater than Today date"])
        else:
            if (start_date) and end_date <= start_date:
                self._errors["end_date"] = self.error_class(["End date should be greater than start date."])


class Category_ModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name= self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Category name must be at least 3 characters.")
        elif Category.objects.filter(name=name).exists() and name != self.instance.name:
            raise forms.ValidationError("Category name is already exist")
        return name
    
class Report_ModelForm(forms.ModelForm):
    reason = forms.CharField( 
        widget=forms.Textarea(attrs={"placeholder": "Reason of reporting", "class": "form-control"}),
    )

    class Meta:
        model=Project_Report
        fields=['reason']    

class ProjectReport_ModelForm(forms.ModelForm):
    reason = forms.CharField( 
        widget=forms.Textarea(attrs={"placeholder": "Reason of reporting", "class": "form-control"}),
    )

    class Meta:
        model=Project_Report
        fields=['reason']   
