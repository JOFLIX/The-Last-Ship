from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from twilio.rest import Client
from accounts.models import User
from .models import TextMessage

# Create your views here.
@login_required(login_url='loginuser')
def sms (request):
    if request.user.is_superuser:
        message=request.POST.get('message')
        receiver = request.POST.get('receivers')
        msg=message
        print(message)
        print(receiver)
        phone=''
        if receiver:
            if receiver=='is_student':
                user_objects=User.objects.filter(is_student=True)
            elif receiver=='is_lecturer':
                user_objects=User.objects.filter(is_lecturer=True)
            elif receiver=='is_superuser':
                user_objects=User.objects.filter(is_superuser=True)
            else:
                user_objects=User.objects.filter(is_parent=True)
            for x in user_objects:
                phone= str(x.phone)
                phone='+254' + phone
                if phone and message:
                    print(phone,"pffrhvdh ")
                    # Your Account SID from twilio.com/console
                    account_sid = "ACec4331327aeb4da8982521050be3afdc"
                    # Your Auth Token from twilio.com/console
                    auth_token  = "26b998983b3ba8a41b9c2a0cecdafb8c"

                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                        to=phone, 
                        from_="+19097643267",
                        body=message)
                    print(message.sid)
                    messages.info(request,'Message Have Been Sent ')
                    obj=TextMessage.objects.create(message=msg,receiver="james kamiri")
                    obj.save()
                    messages.info(request,'And Saved ')

        return render (request,'sms/sms.html')
    else:
        return redirect ('dashboard')