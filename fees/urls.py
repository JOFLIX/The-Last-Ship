
from django.urls import path
from . import views

urlpatterns = [
path('add_fee/',views.add_fee,name="add_fee"),
path('view_fee/',views.view_fee,name="view_fee"),
path('view_my_fee/',views.view_my_fee,name="view_my_fee"),
path('print_receipt/<str:pk>/',views.print_receipt,name="print_receipt"),
path('pdfstudentfeesstatement/',views.pdfstudentfeesstatement,name="pdfstudentfeesstatement"),


]

