
from django.urls import path
from . import views

urlpatterns = [
path('view_income_statement_report/',views.view_income_statement_report,name="view_income_statement_report"),
path('pdf_full__finantial_report/',views.pdf_full__finantial_report,name="pdf_full__finantial_report")
]

