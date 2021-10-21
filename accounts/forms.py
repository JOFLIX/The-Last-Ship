from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User ,Profile,Settings,Classes,Courses
from django.contrib.admin.widgets import AdminTimeWidget , AdminDateWidget
from .models import Classes,UploadedAssignments ,EnrollmentFee, Semester,CourseUnit,GenerateNotice,Module,Session,OnlineApplication,Term,ScheduleOnlineClass,ElearningLibraryResource,Departments,Messages,Assignment,Timetable,Exam,AllStudentsAnnouncements,DepartmentalStudentAnnouncement,SpecificClassAnnouncement,SpecificStudentAnnouncement

INTAKE_CHOICES=(
    ('January','January'),
    ('February','February'),
    ('March','March'),
    ('April','April'),
    ('May','May'),
    ('June','June'),
    ('July','July'),
    ('August','August'),
    ('September','September'),
    ('October','October'),
    ('November','November'),
    ('December','December'),
)


class DateInput(forms.DateInput):
    input_type='date'  
class student_creation_form(UserCreationForm):
   intake=forms.ChoiceField(choices=INTAKE_CHOICES)
   dob=forms.DateField(widget=DateInput)
   is_student=forms.BooleanField(required=True,initial=True)
   course_assigned=forms.ModelChoiceField(queryset=Courses.objects.all())
   class_assigned=forms.ModelChoiceField(queryset=Classes.objects.all())
  # semester=forms.ModelChoiceField(queryset=Semester.objects.all())
  # module=forms.ModelChoiceField(queryset=Module.objects.all())
   student_term=forms.ModelChoiceField(queryset=Term.objects.all())
   phone=forms.IntegerField(required=True)
   class Meta:
        model = User
        fields=[
           'registration_number','email','first_name','last_name','is_student','national_ID',
           'official_picture','dob','phone','course_assigned','department','gender','intake',
           'next_of_kin_firstname','next_of_kin_middlename','next_of_kin_lastname','next_of_kin_relationship',
           'next_of_kin_phone','password1','password2','next_of_kin_phone','class_assigned','student_term','next_of_kin'
       ]



class parent_creation_form(UserCreationForm):
   is_parent=forms.BooleanField(required=True,initial=True)
   phone=forms.IntegerField(required=True)
   student_number=forms.CharField(required=True)
   national_ID=forms.IntegerField(required=True)

   registration_number=forms.CharField(label="Parent Number (phone number or national ID Number ... )")
   class Meta:
        model = User
        fields=[
           'registration_number','email','first_name','last_name','is_parent','national_ID','phone','gender','student_number',
          'password1','password2'
       ]


class update_parent_form (forms.ModelForm):
   is_parent=forms.BooleanField(required=True,initial=True)
   phone=forms.IntegerField(required=True)
   student_number=forms.CharField(required=True)
   national_ID=forms.IntegerField(required=True)

   registration_number=forms.CharField(label="Parent Number (phone number or national ID Number ... )")
   class Meta:
        model = User
        fields=[
           'registration_number','email','first_name','last_name','is_parent','national_ID','phone','gender','student_number',
          
       ]






class lecturer_creation_form(UserCreationForm):
   dob=forms.DateField(widget=DateInput)
   is_lecturer=forms.BooleanField(required=True,initial=True)
   registration_number=forms.CharField(label="Lecturer Number")
   national_ID=forms.IntegerField(required=True)
   phone=forms.IntegerField(required=True)
   class Meta:
       model = User
       fields=[
           'registration_number','email','first_name','last_name','is_lecturer','national_ID',
           'official_picture','dob','phone','department','gender',
           'next_of_kin_firstname','next_of_kin_middlename','next_of_kin_lastname','next_of_kin_relationship',
           'next_of_kin_phone','password1','password2','next_of_kin_phone'
       ]

class update_lecturer_form_form(forms.ModelForm):
   dob=forms.DateField(widget=DateInput)
   is_lecturer=forms.BooleanField(required=True)
   registration_number=forms.CharField(label="Lecturer Number")
   national_ID=forms.IntegerField(required=True)
   phone=forms.IntegerField(required=True)
   class Meta:
       model = User
       fields=[
           'registration_number','email','first_name','last_name','is_lecturer','national_ID',
           'official_picture','dob','phone','department','gender','is_active',
           'next_of_kin_firstname','next_of_kin_middlename','next_of_kin_lastname','next_of_kin_relationship',
           'next_of_kin_phone','next_of_kin_phone'
       ]

class update_student_form(forms.ModelForm):
   dob=forms.DateField(widget=DateInput)
   is_student=forms.BooleanField(required=True)
   #semester=forms.ModelChoiceField(queryset=Semester.objects.all())
  # semester=forms.ModelChoiceField()
   #module=forms.ModelChoiceField(queryset=Module.objects.all())
   student_term=forms.ModelChoiceField(queryset=Term.objects.all())
   class Meta:
       model = User
       fields=[
           'registration_number','email','first_name','last_name','is_student','national_ID',
           'official_picture','dob','phone','course_assigned','department','gender','intake',
           'next_of_kin_firstname','next_of_kin_phone','class_assigned','is_active','student_term','next_of_kin'
       ]

class add_class_form(forms.ModelForm):
   class Meta:
       model = Classes
       fields=[
           'Class_Name','Class_code'
    
       ]



class ProfileForm(forms.ModelForm):
   class Meta:
       model = Profile
       fields=[
           'picture','studied_at','county','location','my_profile','phone','country','occupation','skills','notes'
       ]

class Settings_form(forms.ModelForm):
   class Meta:
       model = Settings
       fields=[
           'School_name','term','session_year'
       ]

class Session_form(forms.ModelForm):
   class Meta:
       model = Session
       fields=[
           'session_year'
       ]

class term_form(forms.ModelForm):
   class Meta:
       model = Term
       fields=[
           'term'
       ]


class courses_form(forms.ModelForm):
   class Meta:
       model = Courses
       fields=[
           'course_name','school_of','course_ID','course_description','img'
       ]


class department_form(forms.ModelForm):
   class Meta:
       model = Departments
       fields=[
           'Department_name','department_id'
       ]


class update_superuser_form(forms.ModelForm):
   is_superuser=forms.BooleanField()
   class Meta:
       model = User
       fields=[
           'registration_number','first_name','last_name','is_active','email','is_superuser'
       ]


class superuser_creation_form(UserCreationForm):
   is_superuser=forms.BooleanField(required=True,initial=True)
   registration_number=forms.IntegerField(label="Staff Number")
   class Meta:
       model = User
       fields=[
           'registration_number','first_name','last_name','is_active','email','is_superuser','password1','password2'
       ]

class timetable_form(forms.ModelForm):
   class Meta:
       model = Timetable
       fields=[
             'class_ID','unit_name','time_dulation','day','room','lecturer_number','lecturer_name','class_link'
       ]



class Exam_form(forms.ModelForm):
  # student_registration_number=forms.IntegerRangeField(labe='Registration Number')
   class Meta:
       model = Exam
       fields=[
             'student_registration_number','year','term','cat_marks','end_term_marks','unit_name','module'
       ]

class AllStudentsAnnouncements_form(forms.ModelForm):
   class Meta:
       model = AllStudentsAnnouncements
       fields=[
               'title','announcement'
       ]

class ScheduleOnlineClassForm(forms.ModelForm):
   # date=forms.DateField(widget=DateInput)
  #  start_time=forms.CharField(widget=forms.TimeInput(attrs={'type':'time'}))
    class Meta:
       model = ScheduleOnlineClass
       fields=[
      'target_class',  'unit','day','time','class_link'
       ]

class AssignmentForm(forms.ModelForm):
    deadline=forms.DateField(widget=DateInput)
    class Meta:
       model = Assignment
       fields=[
        'to_class','assignment_title','assignment_instructions','questions','file','deadline'
       ]

class MessagesForm(forms.ModelForm):
    class Meta:
       model = Messages
       fields=[
      'message'
       ]
class AdminReplyMessageForm(forms.ModelForm):
    class Meta:
       model = Messages
       fields=[
         'user','message','reply'
       ]


class ElearningLibraryResourceForm(forms.ModelForm):
    class Meta:
       model = ElearningLibraryResource
       fields=[
       'course','unit','typed_notes','file'
       ]

class GenerateNoticeForm(forms.ModelForm):
    class Meta:
       model = GenerateNotice
       fields=[
       'title','description'
       ]


class OnlineApplicationForm(forms.ModelForm):
    dob=forms.DateField(widget=DateInput)
    class Meta:
       model = OnlineApplication
       fields=[
         'surname','first_name','other_names','gender','dob','nationality','national_id','county','district',
            'town','course_applied_for','email','course_name','parent_or_guardian_tel','student_tel'
       ]



class CourseUnitForm(forms.ModelForm):
    class Meta:
       model = CourseUnit
       fields=[
       'unit_name','course','module'
       ]






class UploadedAssignmentsForm(forms.ModelForm):
    class Meta:
       model = UploadedAssignments
       fields=[
       'assignment_code','file','class_name','assignment_code'
              ]


class approve_online_applications_form(forms.ModelForm):
    class Meta:
       model = OnlineApplication
       fields=[
                'approved'
              ]


class EnrollmentFeeForm(forms.ModelForm):
    class Meta:
       model = EnrollmentFee
       fields=[
        'received_from', 'reg_no' ,'Registration_admission_fee', 'Tution_fee',
        'boarding_hostel_fees' ,'repair_and_maintanance', 'electricity_water_and_conservancy',
        'activity_fund' ,'medical_fud_insurance', 'rent_hire' ,'examination', 'computer_studies',
        'production_contracts', 'evening_classes', 'citc_uniform_badge_id_card_t_shirt',
        'sundry_debtors_fees_arrears' ,'income_genarating_act', 'miscellaneous'
                
              ]
