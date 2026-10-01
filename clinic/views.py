from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import (
    Medicine,
    Doctor,
    Appointment,
    VirtualAssistance,
    EmergencyRequest
)

import re
from datetime import date, datetime

# ============================================================
# APPOINTMENT BOOKING
# ============================================================

def appointment_booking(request):

    if request.method == 'POST':

        email = request.POST.get('email', '').strip()
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('date', '').strip()
        appointment_time = request.POST.get('time', '').strip()

        # ----------------------------------------------------
        # Validate Woxsen email
        # ----------------------------------------------------

       
  
        # ----------------------------------------------------
        # Validate appointment date
        # ----------------------------------------------------

        try:
            parsed_date = date.fromisoformat(appointment_date)

            if parsed_date < date.today():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please select today or a future date.'
                })

        except (ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Please select a valid appointment date.'
            })
        try:
            validate_email(email)
        except ValidationError:
           return JsonResponse({
        'status': 'error',
        'message': 'Please enter a valid email address.'
    })
        # ----------------------------------------------------
        # Validate doctor
        # ----------------------------------------------------

        try:
            doctor = Doctor.objects.get(id=doctor_id)

        except (Doctor.DoesNotExist, ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Please select a valid doctor.'
            })

        # ----------------------------------------------------
        # Validate time
        # ----------------------------------------------------

        try:
            parsed_time = datetime.strptime(
                appointment_time,
                '%H:%M'
            )

        except (ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Please select a valid appointment time.'
            })

        # ----------------------------------------------------
        # Create appointment
        # ----------------------------------------------------

        appointment = Appointment.objects.create(
            email=email,
            date=appointment_date,
            time=appointment_time,
            doctor=doctor
        )

        # ----------------------------------------------------
        # Format values only for display
        # ----------------------------------------------------

        formatted_date = parsed_date.strftime(
            '%d %B %Y'
        )

        formatted_time = parsed_time.strftime(
            '%I:%M %p'
        )

        # ----------------------------------------------------
        # Success response
        # ----------------------------------------------------

        return JsonResponse({
            'status': 'success',
            'message': 'Appointment booked successfully.',
            'doctor': doctor.name,
            'specialty': doctor.specialty,
            'date': formatted_date,
            'time': formatted_time
        })

    # --------------------------------------------------------
    # GET request
    # --------------------------------------------------------

    doctors = Doctor.objects.all()

    specialties = Doctor.objects.values_list(
        'specialty',
        flat=True
    ).distinct()

    return render(
        request,
        'booking.html',
        {
            'doctors': doctors,
            'specialties': specialties
        }
    )


# ============================================================
# MEDICINE STOCK
# ============================================================

def medicine_stock(request):

    medicines = Medicine.objects.all()

    return render(
        request,
        'stock.html',
        {
            'medicines': medicines
        }
    )


# ============================================================
# DOCTOR AVAILABILITY
# ============================================================

def doctor_availability(request):

    doctors = Doctor.objects.filter(
        available_today=True
    )

    return render(
        request,
        'availability.html',
        {
            'doctors': doctors
        }
    )


# ============================================================
# EMERGENCY
# ============================================================


def emergency(request):

    if request.method == 'POST':

        patient_name = request.POST.get('patient_name', '').strip()
        patient_email = request.POST.get('patient_email', '').strip()
        patient_phone = request.POST.get('patient_phone', '').strip()
        symptoms = request.POST.get('symptoms', '').strip()
        consultation_type = request.POST.get('consultation_type', '').strip()
        doctor_id = request.POST.get('doctor')

        if not all([patient_name, patient_email, symptoms, doctor_id]):
            return render(request, 'video_chat.html', {
                'error': 'Please complete all required fields.',
                'doctors': Doctor.objects.filter(
                    available_today=True,
                    user__is_active=True
                )
            })

        if consultation_type not in ['video', 'chat']:
            return render(request, 'video_chat.html', {
                'error': 'Please select a valid consultation type.',
                'doctors': Doctor.objects.filter(
                    available_today=True,
                    user__is_active=True
                )
            })

        try:
            doctor = Doctor.objects.get(
                id=doctor_id,
                available_today=True,
                user__is_active=True
            )
        except (Doctor.DoesNotExist, ValueError, TypeError):
            return render(request, 'video_chat.html', {
                'error': 'The selected doctor is unavailable.',
                'doctors': Doctor.objects.filter(
                    available_today=True,
                    user__is_active=True
                )
            })

        emergency_request = EmergencyRequest.objects.create(
            patient_name=patient_name,
            patient_email=patient_email,
            patient_phone=patient_phone,
            symptoms=symptoms,
            consultation_type=consultation_type,
            doctor=doctor
        )

        return redirect(
            'emergency_status',
            room_id=emergency_request.room_id
        )

    doctors = Doctor.objects.filter(
        available_today=True,
        user__is_active=True
    )

    return render(
        request,
        'video_chat.html',
        {'doctors': doctors}
    )
# ============================================================
# VIRTUAL ASSISTANCE
# ============================================================

def virtual_assistance(request):

    if request.method == 'POST':

        problem = request.POST.get(
            'problem',
            ''
        ).strip()

        if not problem:
            return JsonResponse({
                'advice': 'Please describe your problem first.'
            })

        advice = VirtualAssistance.objects.filter(
            problem__icontains=problem
        ).first()

        if advice:

            return JsonResponse({
                'advice': advice.first_aid
            })

        return JsonResponse({
            'advice': 'Please visit the clinic for better assistance.'
        })

    return render(
        request,
        'assistance.html'
    )



# ============================================================
# DOCTOR LOGIN
# ============================================================

def doctor_login(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:
                doctor = user.doctor_profile
            except Doctor.DoesNotExist:
                return render(request, 'doctor_login.html', {
                    'error': 'This account is not linked to a doctor.'
                })

            if not user.is_active:
                return render(request, 'doctor_login.html', {
                    'error': 'This account is inactive.'
                })

            login(request, user)
            return redirect('doctor_dashboard')

        return render(request, 'doctor_login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'doctor_login.html')


# ============================================================
# DOCTOR LOGOUT
# ============================================================

@login_required(login_url='doctor_login')
@require_POST
def doctor_logout(request):

    logout(request)
    return redirect('doctor_login')


# ============================================================
# DOCTOR DASHBOARD
# ============================================================

@login_required(login_url='doctor_login')
def doctor_dashboard(request):

    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        logout(request)
        return redirect('doctor_login')

    emergency_requests = EmergencyRequest.objects.filter(
        doctor=doctor
    ).order_by('-created_at')

    return render(
        request,
        'doctor_dashboard.html',
        {
            'doctor': doctor,
            'emergency_requests': emergency_requests
        }
    )


# ============================================================
# ACCEPT, REJECT OR COMPLETE EMERGENCY REQUEST
# ============================================================

@login_required(login_url='doctor_login')
@require_POST
def doctor_update_request(request, request_id):

    try:
        doctor = request.user.doctor_profile

    except Doctor.DoesNotExist:
        logout(request)
        return redirect('doctor_login')

    emergency_request = get_object_or_404(
        EmergencyRequest,
        id=request_id,
        doctor=doctor
    )

    action = request.POST.get('action')

    # ACCEPT EMERGENCY REQUEST
    if action == 'accept' and emergency_request.status == 'pending':

        emergency_request.status = 'accepted'

    # REJECT EMERGENCY REQUEST
    elif action == 'reject' and emergency_request.status == 'pending':

        emergency_request.status = 'rejected'

    # COMPLETE VIDEO CONSULTATION
    elif (
        action == 'complete'
        and emergency_request.status == 'accepted'
        and emergency_request.consultation_type == 'video'
    ):

        emergency_request.status = 'completed'

    else:
        return redirect('doctor_dashboard')

    emergency_request.save(update_fields=['status'])

    return redirect('doctor_dashboard')


# ============================================================
# PATIENT EMERGENCY REQUEST STATUS
# ============================================================

def emergency_status(request, room_id):

    emergency_request = get_object_or_404(
        EmergencyRequest,
        room_id=room_id
    )

    return render(
        request,
        'emergency_status.html',
        {
            'emergency_request': emergency_request
        }
    )


@login_required(login_url='doctor_login')
def doctor_consultation_room(request, room_id):
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect('doctor_login')

    emergency_request = get_object_or_404(
        EmergencyRequest,
        room_id=room_id,
        doctor=doctor,
        status='accepted',
        consultation_type='video'
    )

    return render(
        request,
        'consultation_room.html',
        {
            'emergency_request': emergency_request,
            'role': 'doctor',
            'display_name': doctor.name
        }
    )


def patient_consultation_room(request, room_id):
    emergency_request = get_object_or_404(
        EmergencyRequest,
        room_id=room_id,
        status='accepted',
        consultation_type='video'
    )

    return render(
        request,
        'consultation_room.html',
        {
            'emergency_request': emergency_request,
            'role': 'patient',
            'display_name': emergency_request.patient_name
        }
    )

# ============================================================
# MAIN LANDING PAGE
# ============================================================

def home(request):
    return render(request, 'home.html')


# ============================================================
# PATIENT DASHBOARD
# ============================================================

def patient_dashboard(request): 
    context = {
        'doctor_count': Doctor.objects.filter(
            available_today=True
        ).count(),

        'medicine_count': Medicine.objects.count(),
    }

    return render(
        request,
        'patient_dashboard.html',
        context
    )