from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = "main"


urlpatterns = [
    # Search box urls starts from here
    path('search_vitals', csrf_exempt(views.search_vitals), name='search_vitals'),
    path('search_diag', csrf_exempt(views.search_diag), name='search_diag'),
    path('search_phyorders', csrf_exempt(views.search_phyorders), name='search_phyorders'),
    path('search_rx', csrf_exempt(views.search_rx), name='search_rx'),
    path('search_vaccine', csrf_exempt(views.search_vaccine), name='search_vaccine'),
    path('search_appointments', csrf_exempt(views.search_appointments), name='search_appointments'),
    path('search_billrecords', csrf_exempt(views.search_billrecords), name='search_billrecords'),



   # Remaining methods' urls starts from here
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
    path('provider_details/', views.provider_details, name='provider_details'),
    path('Allergy_Edit/<int:id>', views.Allergy_Edit, name='Allergy_Edit'),
    path('insurance_Edit/<int:id>', views.insurance_Edit, name='insurance_Edit'),
    path('makeappt/', views.make_appointments, name='makeappt'),
    path('appt/', views.appointments_view, name='appt'),

    # Add Information
    path('add_vitals', views.add_vitals, name='add_vitals'),
    path('add_diag', views.add_diag, name='add_diag'),
    path('add_po', views.add_po, name='add_po'),
    path('add_prescription', views.add_prescription, name='add_prescription'),
    path('add_vaccine', views.add_vaccine, name='add_vaccine'),
    path('add_records', views.add_records, name='add_records'),
    path('add_appointments', views.add_appointments, name='add_appointments'),

    # Edit Information
    path('edit_vitals/(?P<pk>\d+)', views.edit_vitals, name='edit_vitals'),
    path('edit_diag/(?P<pk>\d+)', views.edit_diag, name='edit_diag'),
    path('edit_po/(?P<pk>\d+)', views.edit_po, name='edit_po'),
    path('edit_prescription/(?P<pk>\d+)', views.edit_prescription, name='edit_prescription'),
    path('edit_vaccine/(?P<pk>\d+)', views.edit_vaccine, name='edit_vaccine'),
    path('edit_records/(?P<pk>\d+)', views.edit_records, name='edit_records'),
    path('edit_appointments/(?P<pk>\d+)', views.edit_appointments, name='edit_appointments'),

    # Delete Information
    path('delete_vitals/(?P<pk>\d+)', views.delete_vitals, name='delete_vitals'),
    path('delete_diag/(?P<pk>\d+)', views.delete_diag, name='delete_diag'),
    path('delete_po/(?P<pk>\d+)', views.delete_po, name='delete_po'),
    path('delete_prescription/(?P<pk>\d+)', views.delete_prescription, name='delete_prescription'),
    path('delete_vaccine/(?P<pk>\d+)', views.delete_vaccine, name='delete_vaccine'),
    path('delete_records/(?P<pk>\d+)', views.delete_records, name='delete_records'),
    path('delete_appointments/(?P<pk>\d+)', views.delete_appointments, name='delete_appointments'),

    # Admin Side
    path('admin_reg/', views.admin_reg, name='admin_reg'),
    path('patient_search/', views.patient_search, name='patient_search'),
    path('patient_search_failed/', views.patient_search_failed, name='patient_search_failed'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_vitals/', views.admin_vitals, name='admin_vitals'),
    path('admin_diagnosis/', views.admin_diagnosis, name='admin_diagnosis'),
    path('admin_phys/', views.admin_phys, name='admin_phys'),
    path('admin_rx/', views.admin_rx, name='admin_rx'),
    path('admin_vaccines/', views.admin_vaccines, name='admin_vaccines'),
    path('admin_records/', views.admin_records, name='admin_records'),
    path('admin_makeappt/', views.admin_makeappt, name='admin_makeappt'),
    path('admin_appt/', views.admin_appt, name='admin_appt'),

    path('admin_search_vitals', csrf_exempt(views.admin_search_vitals), name='admin_search_vitals'),
    path('admin_search_diag', csrf_exempt(views.admin_search_diag), name='admin_search_diag'),
    path('admin_search_phyorders', csrf_exempt(views.admin_search_phyorders), name='admin_search_phyorders'),
    path('admin_search_rx', csrf_exempt(views.admin_search_rx), name='admin_search_rx'),
    path('admin_search_vaccine', csrf_exempt(views.admin_search_vaccine), name='admin_search_vaccine'),
    path('admin_search_appointments', csrf_exempt(views.admin_search_appointments), name='admin_search_appointments'),
    path('admin_search_billrecords', csrf_exempt(views.admin_search_billrecords), name='admin_search_billrecords'),
]