from django.urls import path
from.import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('diet-form/', views.diet_form, name='diet_form'),
    path('profile/', views.diet_form, name='profile'),
    path('download-pdf', views.download_pdf, name='download_pdf'),
]