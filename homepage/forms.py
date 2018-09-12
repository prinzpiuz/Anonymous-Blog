from django import forms
from .models import Post



class Blog(forms.ModelForm):
    post_tittle = forms.CharField(label='title', max_length=100)
    post_content = forms.CharField(label='content',
                              max_length=2000,
                              widget=forms.Textarea(),
                              help_text='Write here your message!'
                              )
    class Meta:
        model = Post
        fields = ["post_tittle", "post_content"]
