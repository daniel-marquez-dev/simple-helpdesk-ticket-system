from django import forms
from .models import Ticket, Comment # 1. Importamos también tu modelo Comment

# --- FORMULARIO DE TU COMPAÑERO (No se toca) ---
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'category', 'status',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter ticket description'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


# --- TU FORMULARIO DEL DÍA 6 (Añade esto aquí abajo) ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message'] # Solo necesitamos el campo de texto, el autor y el ticket se ponen en la vista
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Write a comment or update here...'
            }),
        }