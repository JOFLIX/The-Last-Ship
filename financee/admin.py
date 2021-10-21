from django.contrib import admin
from . models import FeesParticulars,FeePayment,AuditTrailFinance
from import_export.admin import ImportExportModelAdmin


@admin.register(FeesParticulars)
class FeesAdmin(ImportExportModelAdmin):
    search_fields=( 'particular_name','course','year','module','term','amount','date_added')
    list_filter=( 'particular_name','course','year','module','term','amount','date_added')
    list_display=(
     'particular_name','course','year','module','term','amount','date_added'
    )  

@admin.register(FeePayment)
class FeesPayableForCourseAdmin(ImportExportModelAdmin):
    search_fields=( 'registration_number','student_name','course','module','year','term','payment_mthd','prev_arrears','amount_paid','date_paid','current_arrears','payment_mthd','reference_number_or_mpesa_code')
    list_filter=('registration_number','student_name','course','module','year','term','payment_mthd','prev_arrears','amount_paid','date_paid','current_arrears','payment_mthd','reference_number_or_mpesa_code')
    list_display=(
   'registration_number','student_name','course','module','year','term','payment_mthd','amount_paid','date_paid','prev_arrears','current_arrears','payment_mthd','reference_number_or_mpesa_code'
    )  



@admin.register(AuditTrailFinance)
class AuditTrailFinanceAdmin(ImportExportModelAdmin):
    search_fields=()
    list_filter=('user','action','item','date','page','description','date_added')
    list_display=(
     'user','action','item','date','page','description','date_added'
    )   
    def has_delete_permission(self, request, obj=None):
            # Disable delete
        return False
    def has_add_permission(self, request):
        return False
    def save_model(self, request, obj, form, change):
            #Return nothing to make sure user can't update any data
        pass
    def get_readonly_fields(self, request, obj=None):
        if obj:
          return ['user']
        else:
            return []