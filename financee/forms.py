from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminTimeWidget , AdminDateWidget
from .models import FeePayment

class FeePaymentForm(forms.ModelForm):
    class Meta:
       model = FeePayment
       fields=[
        'registration_number','student_name','course','module','year','term','payment_mthd','reference_number_or_mpesa_code','prev_arrears','amount_paid','current_arrears'
       ]

