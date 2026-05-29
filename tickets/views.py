from django.shortcuts import render
from .forms import TicketForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Ticket

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        user = self.request.user
        # Si es admin o staff, ve todos los tickets del sistema
        if user.is_staff or user.is_superuser:
            return Ticket.objects.all()
        # Si es un usuario normal, SOLO ve sus propios tickets
        return Ticket.objects.filter(created_by=user)

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save() # Guarda el ticket en la base de datos automáticamente
            return render(request, 'tickets/successful.html')
    else:
        form = TicketForm() # Formulario vacío para la petición GET
        
    return render(request, 'tickets/create_ticket.html', {'form': form})

def successful(request):
    return render(request, 'tickets/successful.html')