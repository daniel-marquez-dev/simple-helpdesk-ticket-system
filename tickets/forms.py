from django import forms
<<<<<<< HEAD
from .models import Ticket, Comment 
from .models import Ticket, Comment # 1. Importamos también tu modelo Comment

=======
from .models import Ticket, Comment
>>>>>>> 76fc53ac6dc48b2ebf034a05fffca77f52460ceb

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
<<<<<<< HEAD

=======
>>>>>>> 76fc53ac6dc48b2ebf034a05fffca77f52460ceb
            'created_by': forms.Select(attrs={'class': 'form-select'}),
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
<<<<<<< HEAD
        {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


# --- TU FORMULARIO DEL DÍA 6 (Añade esto aquí abajo) ---

=======

# 3. Formulario de Comentarios (Día 6)
>>>>>>> 76fc53ac6dc48b2ebf034a05fffca77f52460ceb
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
<<<<<<< HEAD

                'placeholder': 'Write a comment...',

                'placeholder': 'Escribe un comentario o actualización...',

=======
                'placeholder': 'Write a comment...'
>>>>>>> 76fc53ac6dc48b2ebf034a05fffca77f52460ceb
            }),
        }
        labels = {
            'message': '',
        }