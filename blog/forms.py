from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
                'title': forms.TextInput(attrs={'class': 'textinputclass'}), #linked to css(exterl source or our own)
                'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),# only postcontent is our own created class
                }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
                'author': forms.TextInput(attrs={'class': 'textinputclass'}),#the same as PostForm has for same style
                'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
                }
