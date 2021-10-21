
from django.urls import path
from . import views

urlpatterns = [

path('myfee/',views.myfee,name="fee"),
path('addfee/',views.addfee,name="addfee"),
path('viewfee/',views.viewfee,name="viewfee"),
path('studentfeestructure/',views.studentfeestructure,name="studentfeestructure"),
path('studentfeestatement/',views.studentfeestatement,name="studentfeestatement"),
path('paymentformview/',views.paymentformview,name="paymentformview"),
path('updatepayment/<str:pk>/',views.updatepayment,name="updatepayment"),
path('PrintPaymentReceipt/<str:pk>/',views.PrintPaymentReceipt,name="PrintPaymentReceipt")
]

