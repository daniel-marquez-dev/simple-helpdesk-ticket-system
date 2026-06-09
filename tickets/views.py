from django.shortcuts import render, get_object_or_404, redirect # Añadimos get_object_or_404 y redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required # Añadimos este decorador para tu vista
from django.views.generic import ListView
from django.contrib import messages # Para mostrar mensajes de éxito de Bootstrap
from django.http import Http404

from .models import Ticket, Comment # 1. Importamos tu modelo Comment
from .forms import TicketForm, CommentForm # 2. Importamos tu CommentForm

# --- VISTAS DE TU COMPAÑERO (No se tocan, están perfectas) ---

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(created_by=user).order_by('-created_at')

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            # NOTA DE SEGURIDAD: Aquí tu compañero debería asignar el usuario, 
            # pero no tocamos su lógica para no romper su entrega.
            form.save() 
            return render(request, 'tickets/successful.html')
    else:
        form = TicketForm()
        
    return render(request, 'tickets/create_ticket.html', {'form': form})

def successful(request):
    return render(request, 'tickets/successful.html')


# --- TU NUEVA VISTA DEL DÍA 6: DETALLE Y COMENTARIOS ---

@login_required
def ticket_detail_view(request, pk):
    # Buscamos el ticket por su ID (pk). Si no existe, lanza un error 404.
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # CONTROL DE SEGURIDAD: Si el usuario NO es staff/admin y el ticket NO es suyo, bloqueamos el acceso.
    if not (request.user.is_staff or request.user.is_superuser) and ticket.created_by != request.user:
        raise Http404("You do not have permission to view this ticket.")
        
    # Obtenemos todos los comentarios de este ticket ordenados del más viejo al más nuevo
    comments = ticket.comments.all().order_by('created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket       # Enlazamos el comentario al ticket actual
            comment.author = request.user   # El autor es el usuario logueado
            comment.save()
            
            messages.success(request, "Comment added successfully!")
            return redirect('ticket_detail', pk=ticket.pk) # Recarga la página para ver el comentario
    else:
        form = CommentForm() # Formulario vacío para la petición GET
        
    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'tickets/ticket_detail.html', context)