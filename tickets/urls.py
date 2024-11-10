from django.urls import path
from tickets import views

urlpatterns = [
    path('',views.base,name='base'),
    path('tickets/dashboard',views.dashboard, name='dashboard'),
    path('signup/',views.signup_view, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('ticket_list/',views.ticket_list, name='ticket_list'),
    path('create/',views.ticket_create, name='ticket_create'),
    path('<int:id>/',views.ticket_detail, name='ticket_detail'),
    path('update/<int:id>/',views.ticket_update_status, name='ticket_update_status'),
]
