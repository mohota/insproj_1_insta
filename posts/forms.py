from account.models import UserProf
from django import forms  
from .models import Post, Comment, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ('image', 'caption')

class CommentForm(forms.ModelForm):
    class Meta:
        model   = Comment
        fields  = ('body',)

class ReplayForm(forms.ModelForm):
    class Meta:
        model   = Reply
        fields  = ('text',) 