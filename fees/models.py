from django.db import models
from accounts.models import Courses,Term,User



PAYMENT_METHOD_CHOICES=(
    ('Bank','Bank'),
    ('M-pesa','M-pesa'),
    ('Cash','Cash'),
    ('Other','Other'),
)

class FeesParticular(models.Model):
    course_name = models.ForeignKey(Courses, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    amount_payable=models.IntegerField(default=0)
    year=models.IntegerField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
       return str(self.course_name) + ' ' +  str(self.term) + ' -----> ' + str(self.amount_payable)

class Payment(models.Model):
    registration_number=models.CharField(max_length=200)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    previous_arrears=models.IntegerField()
    amount_paid=models.IntegerField(blank=True, null=True)
    payment_method=models.CharField(max_length=200,blank=True, null=True)
    reference_code=models.CharField(max_length=100,blank=True, null=True)
    current_arrears=models.IntegerField()
    course_name = models.ForeignKey(Courses, on_delete=models.CASCADE)
    student_name=models.CharField(max_length=200,blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    year=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
       return str(self.course_name) + str(self.term)




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