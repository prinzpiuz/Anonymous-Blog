from django import forms
from .models import Post


class Blog(forms.ModelForm):
    post_tittle = forms.CharField(max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    post_content = forms.CharField(label='content',
                                   max_length=2000,
                                   widget=forms.Textarea(attrs={'class': 'form-control'}),
                                   help_text='Write here your message!'
                                   )

    class Meta:
        model = Post
        fields = ["post_tittle", "post_content"]


class BlogEdit(forms.ModelForm):
    post_tittle = forms.CharField(label='edit your title here', max_length=100)
    post_content = forms.CharField(label='edit your content here',
                                   max_length=2000,
                                   widget=forms.Textarea(),
                                   )

    class Meta:
        model = Post
        fields = ["post_tittle", "post_content"]
