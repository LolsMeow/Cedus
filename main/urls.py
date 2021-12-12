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
    path('add_vitals', views.add_vitals, name='add_vitals'),
    path('add_diag', views.add_diag, name='add_diag'),
    path('add_po', views.add_po, name='add_po'),
    path('add_prescription', views.add_prescription, name='add_prescription'),
    path('add_vaccine', views.add_vaccine, name='add_vaccine'),
    path('add_records', views.add_records, name='add_records'),
    path('add_appointments', views.add_appointments, name='add_appointments'),
    path('edit_vitals/(?P<pk>\d+)', views.edit_vitals, name='edit_vitals'),
    path('edit_diag/(?P<pk>\d+)', views.edit_diag, name='edit_diag'),
    path('edit_po/(?P<pk>\d+)', views.edit_po, name='edit_po'),
    path('edit_prescription/(?P<pk>\d+)', views.edit_prescription, name='edit_prescription'),
    path('edit_vaccine/(?P<pk>\d+)', views.edit_vaccine, name='edit_vaccine'),
    path('edit_records/(?P<pk>\d+)', views.edit_records, name='edit_records'),
    path('edit_appointments/(?P<pk>\d+)', views.edit_appointments, name='edit_appointments'),
    path('delete_vitals/(?P<pk>\d+)', views.delete_vitals, name='delete_vitals'),
    path('delete_diag/(?P<pk>\d+)', views.delete_diag, name='delete_diag'),
    path('delete_po/(?P<pk>\d+)', views.delete_po, name='delete_po'),
    path('delete_prescription/(?P<pk>\d+)', views.delete_prescription, name='delete_prescription'),
    path('delete_vaccine/(?P<pk>\d+)', views.delete_vaccine, name='delete_vaccine'),
    path('delete_records/(?P<pk>\d+)', views.delete_records, name='delete_records'),
    path('delete_appointments/(?P<pk>\d+)', views.delete_appointments, name='delete_appointments'),
    path('admin_reg/', views.admin_reg, name='admin_reg'),
]