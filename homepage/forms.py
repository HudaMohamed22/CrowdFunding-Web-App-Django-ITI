from django import  forms

class SearchForm(forms.Form):
    options = [('project', 'Project'), ('tag', 'Tag')]
    search_option = forms.ChoiceField(choices=options)
    query = forms.CharField(max_length=100, label='', required=True)

    def clean_query(self):
        query = self.cleaned_data.get("query")
        if not query or query.isspace():
            raise forms.ValidationError("This field cannot be empty.")
        return query
