from django.shortcuts import render, redirect
from .forms import TicketForm

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save() # Guarda el ticket en la base de datos automáticamente
            return redirect('tickets/successful.html') # Redirige a una página de éxito
    else:
        form = TicketForm() # Formulario vacío para la petición GET
        
    return render(request, 'tickets/create_ticket.html', {'form': form})

def successful(request):
    return render(request, 'tickets/successful.html')