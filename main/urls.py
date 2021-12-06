from django.urls import path
from . import views

app_name = "main"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register", views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.auth_logout, name='auth_logout'),
    path('information',views.information_request,name='information'),
    path('vitals/', views.vitals_view, name='vitals'),
    path('diagnosis/', views.diag_view, name='diagnosis'),
    path('rx/', views.rx_view, name='rx'),
    path('phys/', views.phys_orders_view, name='phys'),
    path('vax/', views.vaccines_view, name='vaccines'),
    path('records/', views.records_view, name='records'),
    path('makeappt/', views.make_appointments, name='makeappt'),
    path('appt/', views.appointments_view, name='appt'),
    path('admin_reg/', views.admin_reg, name='admin_reg'),
]