from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form of creation a new post"""
    image_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta():
        model = Post
        fields = ('title', 'text', 'topic',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):
    """Form of creation a new comment to a post"""
    class Meta():
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }