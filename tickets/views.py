from django.shortcuts import render, get_object_or_404, redirect
feature/ticket-form
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from tickets.models import Ticket
from .forms import TicketForm, TicketStatusForm, CommentForm 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Ticket, Comment 
from .forms import TicketForm, CommentForm 

# --- VISTAS DE TICKET LIST & CREATION (Intern 1) ---

class ticketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(created_by=self.request.user).order_by('-created_at')

main

@login_required
def ticket_list(request):
    if request.user.is_staff or request.user.is_superuser:
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
        
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

feature/ticket-form
@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Verificación de seguridad
    if not (request.user.is_staff or request.user.is_superuser) and ticket.created_by != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
        
    comments = ticket.comments.all()

    # Inicializamos ambos formularios para el contexto de la página
    comment_form = CommentForm()
    status_form = TicketStatusForm(instance=ticket)

    if request.method == 'POST':
        # ACCIÓN 1: El administrador cambia el estado del ticket
        if 'update_status' in request.POST and (request.user.is_staff or request.user.is_superuser):
            status_form = TicketStatusForm(request.POST, instance=ticket)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, "¡Estado del ticket actualizado con éxito!")
                return redirect('ticket_detail', pk=ticket.pk)
        
        # ACCIÓN 2: Cualquiera de los dos añade un comentario
        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.author = request.user
                comment.save()
                messages.success(request, "¡Comentario añadido!")
                return redirect('ticket_detail', pk=ticket.pk)

    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
        'status_form': status_form,
    }
    return render(request, 'tickets/ticket-detail.html', context)

main

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return render(request, 'tickets/successful.html')
    else:
        form = TicketForm()
        
    return render(request, 'tickets/create_ticket.html', {'form': form})


def successful(request):
    return render(request, 'tickets/successful.html')


# --- DÍA 6: VISTA DE DETALLE UNIFICADA CON COMENTARIOS (Intern 2) ---

@login_required
def ticket_detail(request, pk):
    # 1. Usamos 'pk' para mantener la consistencia con las URLs de tu compañero
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # 2. Control de seguridad estricto que dejó tu compañero
    if not (request.user.is_staff or request.user.is_superuser) and ticket.created_by != request.user:
        raise PermissionDenied
        
    # 3. Tu lógica del Día 6: Obtener comentarios existentes
    comments = ticket.comments.all()

    # 4. Tu lógica del Día 6: Procesar el formulario de comentarios
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, "¡Comentario añadido correctamente!")
            # Redirigimos usando 'pk' para evitar errores de reversión de URL
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = CommentForm()

    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': form,
    }
    
    # NOTA: Asegúrate de si tu archivo HTML se llama 'ticket-detail.html' o 'ticket_detail.html'
    # He dejado 'ticket-detail.html' porque es el que tu compañero configuró originalmente.
    return render(request, 'tickets/ticket-detail.html', context)