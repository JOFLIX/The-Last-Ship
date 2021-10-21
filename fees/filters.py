import django_filters
from django_filters import CharFilter
from . models import Payment
from accounts.models import User

class Paymentfilter(django_filters.FilterSet):
    user=CharFilter(field_name='user',lookup_expr='icontains',label="Registration Number ")
    class Meta:
          model=Payment
          fields=(
              'user','term','year'
          )
