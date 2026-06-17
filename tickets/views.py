from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count # 👈 CAMBIO 1: Añadimos esta importación para las métricas

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
    
    # Control de seguridad: solo el staff, superusuarios o el creador pueden ver el ticket
    if not (request.user.is_superuser or request.user.is_staff) and ticket.created_by != request.user:
        raise PermissionDenied
        
    comments = ticket.comments.all()

    # Inicializamos los formularios con los datos actuales
    comment_form = CommentForm()
    status_form = TicketStatusForm(instance=ticket)

    if request.method == 'POST':
        # 1. ¿El usuario es administrador y ha enviado el campo de estado (status)?
        if (request.user.is_superuser or request.user.is_staff) and 'status' in request.POST:
            status_form = TicketStatusForm(request.POST, instance=ticket)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, "Ticket status updated successfully!")
                return redirect('ticket_detail', pk=ticket.pk)
        
        # 2. Si no es un cambio de estado, comprobamos si está enviando un comentario (campo message)
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


# --- DÍA 9: VISTA DEL DASHBOARD (PANEL DE CONTROL) 👈 CAMBIO 2: Añadimos la nueva vista ---

@login_required
def ticket_dashboard(request):
    # 1. Filtro base: Staff ve métricas globales; usuario común solo ve las de sus propios tickets
    if request.user.is_staff or request.user.is_superuser:
        base_queryset = Ticket.objects.all()
    else:
        base_queryset = Ticket.objects.filter(created_by=request.user)

    # 2. Agrupamos y contamos por estado en una sola consulta
    status_counts = base_queryset.values('status').annotate(total=Count('id'))
    
    # Lo pasamos a un diccionario simple para mapearlo fácilmente
    counts_dict = {item['status']: item['total'] for item in status_counts}

    # 3. Pasamos las métricas al contexto asegurando un valor de 0 si no hay registros todavía
    context = {
        'total_tickets': base_queryset.count(),
        'tickets_new': counts_dict.get('new', 0),
        'tickets_in_progress': counts_dict.get('in_progress', 0),
        'tickets_resolved': counts_dict.get('resolved', 0),
    }

    return render(request, 'tickets/dashboard.html', context)