from django.contrib import admin
from . models import FeesParticular,Payment,AuditTrailFinance

from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(FeesParticular)
admin.site.register(Payment)



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