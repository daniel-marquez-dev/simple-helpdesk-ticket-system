"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🔐 Rutas nativas de Django para Login y Logout
    # Añadimos 'next_page' para forzar a Django a ir al listado de tickets en vez de buscar la ruta rota antigua
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', next_page='ticket_list'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Ruta personalizada de registro
    path('register/', register_view, name='register'),
    
    # Rutas de la aplicación de tickets
    path('tickets/', include('tickets.urls')),
]