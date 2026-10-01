
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='clinic_home'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    # Existing features
    path('appointment_booking/', views.appointment_booking, name='appointment_booking'),
    path('medicine/', views.medicine_stock, name='medicine_stock'),
    path('doctors/', views.doctor_availability, name='doctor_availability'),
    path('emergency/', views.emergency, name='emergency'),
    path('assistance/', views.virtual_assistance, name='virtual_assistance'),

    # Doctor authentication and dashboard
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('doctor/logout/', views.doctor_logout, name='doctor_logout'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

    # Doctor response to emergency request
    path(
        'doctor/request/<int:request_id>/update/',
        views.doctor_update_request,
        name='doctor_update_request'
    ),

    # Patient request status
    path(
        'emergency/status/<uuid:room_id>/',
        views.emergency_status,
        name='emergency_status'
    ),

    # Video consultation
    path(
        'doctor/consultation/<uuid:room_id>/',
        views.doctor_consultation_room,
        name='doctor_consultation_room'
    ),

    path(
        'patient/consultation/<uuid:room_id>/',
        views.patient_consultation_room,
        name='patient_consultation_room'
    ),
]
