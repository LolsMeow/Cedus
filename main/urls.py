from django.urls import path
from . import views

app_name = "main"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register", views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.auth_logout, name='auth_logout'),
    path('information',views.information_request,name='information'),
    path('vitals', views.vitals_view_test),



    path('vitals/<str:user_>', views.vitals_view, name='vitals_test'),
    path('diag/<str:user_>', views.diag_view, name = 'diagnosis'),
    path('drugs/<str:user_>', views.rx_view, name = 'rx'),
    path('phys_o/<str:user_>', views.phys_orders_view, name = 'phys'),
    path('vax/<str:user_>', views.vaccines_view, name = 'vaccines'),
    path('records/<str:user_>', views.records_view, name = 'records'),
] 