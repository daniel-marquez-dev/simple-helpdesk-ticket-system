from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket
from .forms import TicketForm

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
    # Requirement: Fetch the ticket or return 404
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Security check: If the user is NOT an admin AND doesn't own the ticket, deny access
    if not (request.user.is_staff or request.user.is_superuser) and ticket.created_by != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
        
    return render(request, 'tickets/ticket-detail.html', {'ticket': ticket})

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