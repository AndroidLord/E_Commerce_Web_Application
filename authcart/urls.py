from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('login',views.handlelogin,name='handlelogin'),
    path('logout',views.handlelogout,name='handlelogout'),
    path('verify/<uidb64>/<token>',views.VerifyAccountView.as_view(),name='verifyMail')
]