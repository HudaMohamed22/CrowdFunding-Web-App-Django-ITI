from django import  forms
from project.models import  Project,Category,Tag
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
    
    # def clean_tag(self):
    #     tags = self.cleaned_data.get('tag')
    #     if tags:
    #         for tag in tags:
    #             if not tag.name.isalnum():
    #                 raise forms.ValidationError("Tags should only contain letters or numbers.")
    #     return tags
    

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

    # give me this field can't be null !!
    # def clean_end_time(self):
    #     start_date = self.cleaned_data.get("start_date")
    #     end_date = self.cleaned_data.get("end_time")
    #     print(end_date)
    #     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     today_date = datetime.now().date()
    #     print(today_date)
    #     print("ffffffffffffffffffffffffffffffffff")

    #     if today_date >= end_date:
    #         print("oooooooooooooo1111111111")
    #         raise forms.ValidationError("End date should be greater than Today date.")
        
    #     if start_date and (end_date <= start_date):
    #         print("pppppppppppp222222222222222")
    #         raise forms.ValidationError("End date should be greater than start date.")


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