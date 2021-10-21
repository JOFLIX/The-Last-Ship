
from django.urls import path

from . import views


urlpatterns = [
  
    path('email_students/',views.sendemailtostudents,name="sendemailtostudents"),
    path('email_lecturers/',views.sendemaillecturers,name="sendemaillecturers"),
    
]
