from django import forms
 feature/filters
from .models import Ticket, Comment

feature/ticket-form
from .models import Ticket, Comment 

from .models import Ticket, Comment # 1. Importamos también tu modelo Comment
main
 main

# 1. Formulario de Creación de Tickets (Día 5)
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'category', 'status', 'created_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter ticket description'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
 feature/filters
            'created_by': forms.Select(attrs={'class': 'form-select'}),

feature/ticket-form
            'created_by': forms.Select(attrs={'class': 'form-select'}),
        }

class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Actualizar Estado',
        }


            'status': forms.Select(attrs={'class': 'form-select'}),
 main
        }

# 2. Formulario de Actualización de Estados (Día 7) 👈 ¡ESTO ES LO QUE SE HABÍA BORRADO!
class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Actualizar Estado',
        }

 feature/filters
# 3. Formulario de Comentarios (Día 6)

# --- TU FORMULARIO DEL DÍA 6 (Añade esto aquí abajo) ---
main
 main
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
 feature/filters
                'placeholder': 'Write a comment...'

feature/ticket-form
                'placeholder': 'Write a comment...'

                'placeholder': 'Escribe un comentario o actualización...'
main
 main
            }),
        }
        labels = {
            'message': '',
        }