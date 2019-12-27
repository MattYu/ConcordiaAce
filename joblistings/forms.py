from django import forms

MAX_LENGTH_TITLE = 120
MAX_LENGTH_DESCRIPTION = 1000
MAX_LENGTH_RESPONSABILITIES = 600
MAX_LENGTH_REQUIREMENTS = 600
MAX_LENGTH_STANDARDFIELDS= 30

class JobForm(forms.Form):
    title = forms.CharField(max_length=MAX_LENGTH_TITLE, 
                            help_text='Your title here',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your job title here'})
                            )
    email = forms.EmailField(max_length=254)
    description = forms.CharField(
        max_length=MAX_LENGTH_DESCRIPTION,
        widget=forms.Textarea(attrs={'class': 'tinymce-editor tinymce-editor-1', 'placeholder': 'Description text here'})
    )

    def clean(self):
        cleaned_data = super(JobForm, self).clean()
        '''
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
        '''