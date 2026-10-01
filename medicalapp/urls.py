
from django.contrib import admin
from django.urls import path, include
from clinic import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main landing page
    path('', views.home, name='home'),

    # Existing clinic pages
    path('clinic/', include('clinic.urls')),
]