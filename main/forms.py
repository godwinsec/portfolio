from django import forms
from django.conf import settings

from froala_editor.widgets import FroalaEditor
from .models import BlogPost

    
class BlogForm(forms.ModelForm):
    content = forms.CharField(
        widget=FroalaEditor(
            options=settings.FROALA_EDITOR_OPTIONS
        )
    )
    
    class Meta:
        model = BlogPost
        fields = ("title", 'content', 'image')