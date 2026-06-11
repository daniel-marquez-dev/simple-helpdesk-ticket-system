from django.urls import path
from . import views

urlpatterns = [
    path('create_ticket/',views.create_ticket, name='create_ticket'),
    path('successful/',views.successful, name='successful'),
    path('', views.ticketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
]