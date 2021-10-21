from django.db import models
from accounts.models import Term
# Create your models here.
from django.utils import timezone
from accounts.models import Session , Term,Courses,Settings,Module
from accounts.models import User

PAYMENT_METHOD_CHOICES=(
    ('Bank','Bank'),
    ('M-pesa','M-pesa'),
    ('Cash','Cash'),
    ('Other','Other'),
)


class FeesParticulars(models.Model):
    particular_name=models.CharField(max_length=50)
    course=models.ForeignKey(Courses, on_delete=models.CASCADE)
    year=models.ForeignKey(Session, on_delete=models.CASCADE)
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    term=models.ForeignKey(Term, on_delete=models.CASCADE)
    amount=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.course)
    class Meta:
            verbose_name = ('Fees Particular')
            verbose_name_plural = ('Fees Particulars' )


class FeePayment(models.Model):
    registration_number= models.CharField(max_length = 100)
    student_name = models.CharField(max_length = 50)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year =models.ForeignKey(Session, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    payment_mthd = models.CharField(max_length=100,blank=True, null=True)
  #  mpesa_code = models.CharField(max_length = 50,blank=True, null=True)
    reference_number_or_mpesa_code= models.CharField(max_length = 50,blank=True, null=True)
    prev_arrears= models.IntegerField()
    amount_paid=models.IntegerField()
    date_paid=models.DateTimeField(auto_now_add=True)
    current_arrears = models.IntegerField()
    def __str__(self):
        return  'Registration Number ' +  str(self.registration_number) +  ' Fess Paid '  +  str(self.amount_paid)
    class Meta:
            verbose_name = ('Fee Payment')
            verbose_name_plural = ('Fees Payment')



class AuditTrailFinance(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    action=models.CharField(max_length=50)
    item=models.TextField(max_length=300)
    date=models.CharField(max_length=400)
    page=models.CharField(max_length=1000)
    description=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.user)
    class Meta:
            verbose_name = ('Audit Trail')
            verbose_name_plural = ('Audit Trail ' )