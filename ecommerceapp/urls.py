from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('checkout', views.checkout, name='checkout'),
    path('handlerequest/',views.handlerequest, name='handlerequest'),
    path('profile', views.profile, name='profile'),
]
