from django import forms
from Note.models import Notes, Category

class NotesForm(forms.ModelForm):
    
    class Meta:
        model = Notes
        fields = ("title", "body", "category_id")


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ("title",)
