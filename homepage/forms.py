from django import forms
from .models import Post


class Blog(forms.ModelForm):
    post_tittle = forms.CharField(max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control' , 'pattern':'.{10,}'}))
    post_content = forms.CharField(label='content',
                                   max_length=2000,
                                   widget=forms.Textarea(attrs={'class': 'form-control','minlength':'10'}),
                                   help_text='Write here your message!'
                                   )

    class Meta:
        model = Post
        fields = ["post_tittle", "post_content"]

    def clean(self):
        super().clean()
        title = self.cleaned_data.get('post_tittle')
        body = self.cleaned_data.get('post_content')
        if len(title) > len(body):
            raise forms.ValidationError("body should be longer than title")






