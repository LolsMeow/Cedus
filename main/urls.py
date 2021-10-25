from django.urls import path
from . import views

app_name = "main"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register", views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.auth_logout, name='auth_logout'),
    path('information',views.information_request,name='information'),
    path('vitals/', views.vitals_view),
    path('diagnosis/', views.diag_view),
    path('rx/', views.rx_view),
    path('phys/', views.phys_orders_view),
    path('vax/', views.vaccines_view),
    path('records/', views.records_view),

]