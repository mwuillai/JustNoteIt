from django import forms
from Note.models import Notes

class NotesForm(forms.ModelForm):
    
    class Meta:
        model = Notes
        fields = ("title", "body", "category_id")
