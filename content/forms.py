from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    hashtags = forms.CharField(
        required=False,
        help_text="Enter hashtags separated by commas (e.g., travel,food,fun)"
    )

    class Meta:
        model = Post
        fields = ['caption', 'image', 'video', 'hashtags']