from django.urls import path
from . import views

app_name ='accounts'

urlpatterns =[
    path('login/', views.Login.as_view(), name='login'),
    path('guest_login/', views.GuestLogin, name='guest_login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]