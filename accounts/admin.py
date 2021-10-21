from django.contrib import admin
from accounts.models import User,AccountsLog,AuditTrail,EnrollmentFee, CourseUnit,OnlineApplication,School,AllLecturersAnnouncements,UploadedAssignments,Module,LessonsDuration,GenerateNotice,Profile,Semester,ElearningLibraryResource,Messages,Assignment,Exam,Courses,Departments,ScheduleOnlineClass,Settings,Classes,Term,Session,Timetable,AllStudentsAnnouncements,DepartmentalStudentAnnouncement,SpecificClassAnnouncement,SpecificStudentAnnouncement
from import_export.admin import ImportExportModelAdmin
from .resources import UserResource



@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class=UserResource
    search_fields=('registration_number',)
    list_filter=('registration_number','department','class_assigned','is_student','is_lecturer','is_superuser','date_joined','is_active')
    list_display=(
       'registration_number', 'email','first_name','last_name','date_joined','is_active','is_staff','is_admin','is_superuser','is_student',
        'national_ID',
        'official_picture','dob','phone','course_assigned','department','gender','intake',
        'next_of_kin_firstname','next_of_kin_middlename','next_of_kin_lastname','next_of_kin_relationship',
        'next_of_kin_phone'
    )      


class ProfileAdmin(admin.ModelAdmin):
    list_filter=('user','studied_at','county','location','phone')
    search_fields=('user',)
    list_display=(
        'user','picture','studied_at','county','location','my_profile','phone','occupation','education','skills','notes','country'
    ) 
admin.site.register(Profile,ProfileAdmin)


@admin.register(Courses)
class CoursesAdmin(ImportExportModelAdmin):
    search_fields=('course_name','course_ID','course_description','date_added')
    list_filter=('course_name','course_ID','course_description','date_added')
    list_display=(
      'course_name','school_of','course_ID','course_description','img','date_added'
    )   


@admin.register(Departments)
class DepartmentsAdmin(ImportExportModelAdmin):
    search_fields=('Department_name','department_id','date_added')
    list_filter=('Department_name','department_id','date_added')
    list_display=(
        'Department_name','department_id','date_added'
    )   


@admin.register(Settings)
class SettingsAdmin(ImportExportModelAdmin):
    search_fields=('School_name','term','session_year')
    list_filter=('School_name','term','session_year')
    list_display=(
        'School_name','term','session_year'
    )  
    def has_delete_permission(self, request, obj=None):
            # Disable delete
        return False 
    

@admin.register(Classes)
class ClassesAdmin(ImportExportModelAdmin):
    search_fields=('Class_Name','Class_code','Registration_Date')
    list_filter=('Class_Name','Class_code','Registration_Date')
    list_display=(
        'Class_Name','Class_code','Registration_Date'
    )   


@admin.register(Term)
class TermAdmin(ImportExportModelAdmin):
    search_fields=('term','date_added')
    list_filter=('term','date_added')
    list_display=(
        'term','date_added'
    )   


@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    search_fields=('session_year','date_added')
    list_filter=('session_year','date_added')
    list_display=(
        'session_year','date_added'
    )   

@admin.register(Timetable)
class TimetableAdmin(ImportExportModelAdmin):
    search_fields=('class_ID','unit_name','lecturer_name','time_dulation','day','room','date_added')
    list_filter=('class_ID','unit_name','lecturer_name','time_dulation','day','room','date_added')
    list_display=(
       'class_ID','unit_name','lecturer_name','time_dulation','day','room','date_added','class_link'
    )   


@admin.register(LessonsDuration)
class LessonsDurationAdmin(ImportExportModelAdmin):
    search_fields=('start_time','end_time','date_added')
    list_filter=('start_time','end_time','date_added')
    list_display=(
       'start_time','end_time','date_added'
    )   

@admin.register(Exam)
class ExamAdmin(ImportExportModelAdmin):
    search_fields=( 'student_registration_number','year','term','cat_marks','end_term_marks')
    list_filter=( 'student_registration_number','year','term','cat_marks','end_term_marks')
    list_display=(
        'student_registration_number','year','term','cat_marks','end_term_marks'
    )   

@admin.register(AllStudentsAnnouncements)
class AllStudentsAnnouncementsAdmin(ImportExportModelAdmin):
    search_fields=( 'title','announcement','date_added')
    list_filter=('title','announcement','date_added')
    list_display=(
       'title','announcement','date_added'
    )   
@admin.register(DepartmentalStudentAnnouncement)
class DepartmentalStudentAnnouncementAdmin(ImportExportModelAdmin):
    search_fields=( 'department','title','announcement','date_added')
    list_filter=( 'department','title','announcement','date_added')
    list_display=(
        'department','title','announcement','date_added'
    )   

@admin.register(SpecificClassAnnouncement)
class SpecificClassAnnouncementAdmin(ImportExportModelAdmin):
    search_fields=( 'class_name','title','announcement','date_added')
    list_filter=( 'class_name','title','announcement','date_added')
    list_display=(
        'class_name','title','announcement','date_added'
    )   
@admin.register(SpecificStudentAnnouncement)
class SpecificStudentAnnouncementAdmin(ImportExportModelAdmin):
    search_fields=( 'registration_number','title','announcement','date_added')
    list_filter=( 'registration_number','title','announcement','date_added')
    list_display=(
        'registration_number','title','announcement','date_added'
    )   


@admin.register(ScheduleOnlineClass)
class ScheduleOnlineClassAdmin(ImportExportModelAdmin):
    search_fields=( 'unit','time','day','class_link')
    list_filter=('unit','time','day','class_link')
    list_display=(
       'target_class','time','class_link','date_added','unit','day'
    )   

@admin.register(Messages)
class MessagesAdmin(ImportExportModelAdmin):
    search_fields=( 'user','message','date_added')
    list_filter=('user','message','date_added')
    list_display=(
       'user','message','date_added'
    )   

@admin.register(ElearningLibraryResource)
class ElearningLibraryResourceAdmin(ImportExportModelAdmin):
    search_fields=( 'course','unit','typed_notes','file','date_added')
    list_filter=('course','unit','typed_notes','file','date_added')
    list_display=(
    'course','unit','typed_notes','file','date_added'
    )   
 

@admin.register(OnlineApplication)
class OnlineApplicationAdmin(ImportExportModelAdmin):
    search_fields=('surname','first_name','other_names','gender','dob','nationality','national_id','county','district',
              'town','course_applied_for','course_name','parent_or_guardian_tel','student_tel','approved')
    list_filter=('surname','first_name','other_names','gender','dob','nationality','national_id','county','district',
              'town','email','course_applied_for','course_name','parent_or_guardian_tel','student_tel','approved')
    list_display=(
             'surname','first_name','other_names','gender','dob','nationality','national_id','county','district',
            'town','email','course_applied_for','course_name','parent_or_guardian_tel','student_tel','approved'
    )   





@admin.register(CourseUnit)
class CourseUnitAdmin(ImportExportModelAdmin):
    search_fields=( 'unit_name','course','module','date_added')
    list_filter=( 'unit_name','course','module','date_added')
    list_display=(
     'unit_name','course','module','date_added'
    )   
 



admin.site.register(Assignment)

admin.site.register(GenerateNotice)
admin.site.register(Semester)
admin.site.register(Module)


admin.site.register(UploadedAssignments)

admin.site.register(School)
admin.site.register(AllLecturersAnnouncements)





@admin.register(AuditTrail)
class AuditTrailAdmin(ImportExportModelAdmin):
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

@admin.register(AccountsLog)
class AccountsLogAdmin(ImportExportModelAdmin):
    search_fields=( 'user','action','item','date','page','description')
    list_filter=('user','action','item','date','page','description','date_added')
    list_display=(
     'user','action','item','date','page','description','date_added'
    )   
    def has_delete_permission(self, request, obj=None):
            # Disable delete wollan
        return False
    def has_add_permission(self, request):
        return False
    def save_model(self, request, obj, form, change):
            #Return nothing to make sure user can't update any data woo
        pass

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user']
        else:
            return []


admin.site.register(EnrollmentFee)





































#logs admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag',    
    ]

    search_fields = [

        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"