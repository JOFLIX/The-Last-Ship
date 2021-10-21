import django_filters
from django_filters import CharFilter
from . models import FeePayment
from accounts.models import User

class FeePaymentfilter(django_filters.FilterSet):
    registration_number=CharFilter(field_name='registration_number',lookup_expr='icontains',label="Registration Number ")
    reference_number_or_mpesa_code=CharFilter(field_name='reference_number_or_mpesa_code',lookup_expr='icontains',label="Transaction Ref ")
    class Meta:
          model=FeePayment
          fields=(
               'registration_number','year','term','course','amount_paid','reference_number_or_mpesa_code'
          )


class StudentFilter(django_filters.FilterSet):
   # registration_number=CharFilter(field_name='registration_number',lookup_expr='icontains',label="Registration Number ")
    class Meta:
          model=User
          fields=(
               'registration_number',
          )


          