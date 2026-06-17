from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.db.models import Count

from .models import Ticket, Comment 
from .forms import TicketForm, CommentForm, TicketStatusForm

# =========================================================================
# 1. LISTADO DE TICKETS (DÍA 8: CON FILTROS ENCADENADOS)
# =========================================================================
class ticketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        # Filtro base de seguridad: Staff/Superuser ve todo, usuario común solo lo suyo
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(created_by=self.request.user)

        # Captura de los parámetros seleccionados en la barra de filtros HTML
        status_filter = self.request.GET.get('status')
        priority_filter = self.request.GET.get('priority')
        category_filter = self.request.GET.get('category')
        user_filter = self.request.GET.get('user')

        # Aplicar filtros encadenados dinámicamente
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        if user_filter and (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(created_by__username__icontains=user_filter)

        # Ordenar por fecha de creación (más recientes primero)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Ticket.STATUS_CHOICES
        context['priority_choices'] = Ticket.PRIORITY_CHOICES
        context['category_choices'] = Ticket.CATEGORY_CHOICES
        return context


# =========================================================================
# 2. DETALLE DEL TICKET (DÍA 7 Y 9: COMENTARIOS Y CAMBIO DE ESTADO SMART)
# =========================================================================
@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Control de seguridad: solo staff, superusuarios o el creador pueden ver el ticket
    if not (request.user.is_superuser or request.user.is_staff) and ticket.created_by != request.user:
        raise PermissionDenied
        
    comments = ticket.comments.all()

    # Inicializamos los formularios con los datos actuales
    comment_form = CommentForm()
    status_form = TicketStatusForm(instance=ticket)

    if request.method == 'POST':
        # ACCIÓN 1: El administrador cambia el estado del ticket (Detecta el campo 'status')
        if (request.user.is_superuser or request.user.is_staff) and 'status' in request.POST:
            status_form = TicketStatusForm(request.POST, instance=ticket)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, "Ticket status updated successfully!")
                return redirect('ticket_detail', pk=ticket.pk)
        
        # ACCIÓN 2: El usuario o admin envía un comentario (Detecta el campo 'message')
        elif 'message' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.author = request.user
                comment.save()
                messages.success(request, "Comment added successfully!")
                return redirect('ticket_detail', pk=ticket.pk)

    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
        'status_form': status_form,
    }
    
    return render(request, 'tickets/ticket_detail.html', context)


# =========================================================================
# 3. CREACIÓN DE TICKETS (DÍA 6)
# =========================================================================
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('successful')
    else:
        form = TicketForm()
        
    return render(request, 'tickets/create_ticket.html', {'form': form})


# =========================================================================
# 4. VISTA DEL DASHBOARD / PANEL DE CONTROL (DÍA 9)
# =========================================================================
@login_required
def ticket_dashboard(request):
    # Filtro base: Staff ve métricas globales; usuario común solo ve las de sus propios tickets
    if request.user.is_staff or request.user.is_superuser:
        base_queryset = Ticket.objects.all()
    else:
        base_queryset = Ticket.objects.filter(created_by=request.user)

    # Agrupamos y contamos por estado en una sola consulta eficiente
    status_counts = base_queryset.values('status').annotate(total=Count('id'))
    counts_dict = {item['status']: item['total'] for item in status_counts}

    # Pasamos las métricas al contexto asegurando un valor de 0 si no hay registros todavía
    context = {
        'total_tickets': base_queryset.count(),
        'tickets_new': counts_dict.get('new', 0),
        'tickets_in_progress': counts_dict.get('in_progress', 0),
        'tickets_resolved': counts_dict.get('resolved', 0),
    }

    return render(request, 'tickets/dashboard.html', context)


# =========================================================================
# 5. PÁGINA DE ÉXITO
# =========================================================================
@login_required
def successful(request):
    return render(request, 'tickets/successful.html')