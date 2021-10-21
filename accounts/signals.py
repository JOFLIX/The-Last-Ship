from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.dispatch import receiver
from datetime import datetime
from .models import AccountsLog


d=datetime.now()
print(d)

@receiver(user_logged_in)
def log_user_login(sender,request,**kwargs):
    print ("User {} Logged In Through Page {} ".format(request.user.registration_number,request.META.get('HTTP_REFERER')))
    user=request.user
    action='LOGIN'
    date=d
    page=request.META.get('HTTP_REFERER')
    description=("User {} Logged In Through Page {} ".format(request.user.registration_number,request.META.get('HTTP_REFERER')))
    item=request.user.first_name
    obj=AccountsLog.objects.create(
        user=user,
        action=action,
        page=page,
        description=description,
        date=date,
        item=item,
    )
    obj.save()
@receiver(user_login_failed)
def log_user_login_failed(sender,request,credentials,**kwargs):
    print ("Ooops User Failed To Login Through Page {} ".format(request.META.get('HTTP_REFERER')))

@receiver(user_logged_out)
def log_user_logout(sender,request,**kwargs):
    print ("User {} Logged Out Through Page {} ".format(request.user.registration_number,request.META.get('HTTP_REFERER')))
    user=request.user
    action='LOGOUT'
    date=d
    page=request.META.get('HTTP_REFERER')
    description= ("User {} Logged Out Through Page {} ".format(request.user.registration_number,request.META.get('HTTP_REFERER')))
    item=request.user.first_name
    obj=AccountsLog.objects.create(
        user=user,
        action=action,
        page=page,
        description=description,
        date=date,
        item=item,
    )
    obj.save()