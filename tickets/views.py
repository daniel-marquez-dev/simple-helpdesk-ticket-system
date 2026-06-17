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
from .forms import TicketForm, CommentForm, TicketStatusForm

class ticketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        # 1. Filtro base de seguridad: Staff ve todo, usuario común solo lo suyo
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(created_by=self.request.user)

        # 2. DÍA 8: Captura de los parámetros seleccionados en la barra de filtros HTML
        status_filter = self.request.GET.get('status')
        priority_filter = self.request.GET.get('priority')
        category_filter = self.request.GET.get('category')
        user_filter = self.request.GET.get('user')

        # 3. DÍA 8: Aplicar filtros encadenados si el usuario seleccionó opciones
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        if user_filter and (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(created_by__username__icontains=user_filter)

        # Devolvemos los tickets ordenados por fecha de creación (más recientes primero)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        # DÍA 8: Pasamos las opciones de las tuplas del modelo para rellenar los <select> del HTML
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Ticket.STATUS_CHOICES
        context['priority_choices'] = Ticket.PRIORITY_CHOICES
        context['category_choices'] = Ticket.CATEGORY_CHOICES
        return context

main

@login_required
def ticket_list(request):
    """
    Nota: Tu proyecto usa la vista basada en clase 'ticketListView' en las URLs, 
    pero dejamos esta función por si tenéis alguna ruta alternativa apuntando aquí.
    """
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


# --- DÍA 7: VISTA DE DETALLE UNIFICADA CON COMENTARIOS Y ESTADOS ---

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Control de seguridad estricto
    if not (request.user.is_staff or request.user.is_superuser) and ticket.created_by != request.user:
        raise PermissionDenied
        
    comments = ticket.comments.all()

    # Inicializamos ambos formularios para pintarlos en el HTML
    comment_form = CommentForm()
    status_form = TicketStatusForm(instance=ticket)

    if request.method == 'POST':
        # ACCIÓN A (Día 7): El staff técnico cambia el estado del ticket
        if 'update_status' in request.POST and (request.user.is_staff or request.user.is_superuser):
            status_form = TicketStatusForm(request.POST, instance=ticket)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, "¡Estado del ticket actualizado con éxito!")
                return redirect('ticket_detail', pk=ticket.pk)
        
        # ACCIÓN B (Día 6): Cualquier usuario añade un comentario
        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.author = request.user
                comment.save()
                messages.success(request, "¡Comentario añadido correctamente!")
                return redirect('ticket_detail', pk=ticket.pk)

    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form, # Cambiado de 'form' a 'comment_form' para evitar confusiones
        'status_form': status_form,   # DÍA 7: Pasamos el formulario de estados al HTML
    }
    
    return render(request, 'tickets/ticket-detail.html', context)