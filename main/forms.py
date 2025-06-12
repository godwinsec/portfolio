from django import forms

from froala_editor.widgets import FroalaEditor
from .models import BlogPost

    
class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=FroalaEditor)  
    class Meta:
        model = BlogPost
        fields = ("title", 'content', 'image')