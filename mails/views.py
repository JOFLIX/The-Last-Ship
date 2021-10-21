from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings 
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User

@login_required(login_url='loginuser')
def sendemailtostudents(request):
    if request.user.is_superuser:
        emails = User.objects.filter(is_active=True,is_student=True).values_list('email', flat=True)
        print(emails)
        if request.method == 'POST':
           message = request.POST['message']
           print('james admin is sending this to all users ',message)
           send_mail(
           'HAVARD INSTITUTE OF DEVELOPMENT STUDIES',
            message,
            settings.EMAIL_HOST_USER,
            emails,
            fail_silently=False,
        )
           messages.info(request,'The email have been sent to all Active Students ')
        
    else:
        return redirect('dashboard')
    return render(request,"mails/sendemailtostudents.html")


@login_required(login_url='loginuser')
def sendemaillecturers(request):
    if request.user.is_superuser:
        emails = User.objects.filter(is_active=True,is_lecturer=True).values_list('email', flat=True)
        print(emails)
        if request.method == 'POST':
           message = request.POST['message']
           print('james admin is sending this to all users ',message)
           send_mail(
           'HAVARD INSTITUTE OF DEVELOPMENT STUDIES',
            message,
            settings.EMAIL_HOST_USER,
            emails,
            fail_silently=False,
        )
           messages.info(request,'The email have been sent to all Active Lectures ')
        
    else:
        return redirect('dashboard')
    return render(request,"mails/sendemaillecturers.html")


    