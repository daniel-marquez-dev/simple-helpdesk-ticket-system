from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticketListView.as_view(), name='ticket_list'),
    path('dashboard/', views.ticket_dashboard, name='ticket_dashboard'), 
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('successful/', views.successful, name='successful'),
]