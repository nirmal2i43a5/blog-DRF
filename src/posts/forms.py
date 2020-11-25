from django import forms

        
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]

