from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from tickets.models import Ticket
from .forms import TicketForm, TicketStatusForm, CommentForm 

@login_required
def ticket_list(request):
    # Requirement: show all tickets for admin users, only own tickets for normal users
    if request.user.is_staff or request.user.is_superuser:
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
        
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

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
        form = TicketForm() # Formulario vacío para la petición GET
        
    return render(request, 'tickets/create_ticket.html', {'form': form})

def successful(request):
    return render(request, 'tickets/successful.html')