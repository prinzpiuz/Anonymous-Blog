from django import forms
from .models import Post
from sanitizer.forms import SanitizedCharField


class Blog(forms.ModelForm):
    post_tittle = forms.CharField(max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'pattern':'.{10,}'}), required=True)
    post_content = SanitizedCharField(label='content', allowed_tags=['b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i'],
                                   max_length=2000, required=True,
                                   widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'content','min_length':'10'}),
                                   help_text='Write here your message!'
                                   )

    class Meta:
        model = Post
        fields = ["post_tittle", "post_content"]

    def clean(self):
        super().clean()
        title = self.cleaned_data.get('post_tittle')
        body = self.cleaned_data.get('post_content')
        if title and body and len(title) > len(body):
           raise forms.ValidationError("body should be longer than title")






