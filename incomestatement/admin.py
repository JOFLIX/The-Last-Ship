from django.contrib import admin
from .models import Revenue ,Taxrate,Expenses,Liabilities,Assets
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Revenue)
class RevenueAdmin(ImportExportModelAdmin):
    search_fields=('revenue_name','revenue_amount','date_added')
    list_filter=('revenue_name','revenue_amount','date_added')
    list_display=(
    'revenue_name','revenue_amount','year','date_added'
    )  

@admin.register(Taxrate)
class TaxrateAdmin(ImportExportModelAdmin):
    search_fields=('tax_rate',)
    list_filter=('tax_rate',)
    list_display=(
       'tax_rate','year'
    )  


@admin.register(Expenses)
class ExpensesAdmin(ImportExportModelAdmin):
    search_fields=('expenses_name','expenses_amount','date_added')
    list_filter=('expenses_name','expenses_amount','date_added')
    list_display=(
    'expenses_name','expenses_amount','date_added','year'
    )  



@admin.register(Liabilities)
class LiabilitiesAdmin(ImportExportModelAdmin):
    search_fields=('Liabilities_name','Liabilities_amount','date_added')
    list_filter=('Liabilities_name','Liabilities_amount','date_added')
    list_display=(
 'Liabilities_name','Liabilities_amount','date_added','year'
    )  



@admin.register(Assets)
class AssetsAdmin(ImportExportModelAdmin):
    search_fields=('asset_name','asset_amount','date_added')
    list_filter=('asset_name','asset_amount','date_added')
    list_display=(
'asset_name','asset_amount','date_added','year'
    )  
