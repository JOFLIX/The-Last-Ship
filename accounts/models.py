from __future__ import unicode_literals

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from accounts.managers import UserManager
from django.conf import settings


from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

from datetime import timezone

from django.utils import timezone


from django.db import models





COURSE_LEVEL=(
    ('DIPLOMA','DIPLOMA'),
    ('CERTIFICATE','CERTIFICATE'),
    ('ARTISAN/PROF','ARTISAN/PROF'),
)
GENDER_CHOICES=(
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
)
DAY_CHOICES=(
    ('Mon','Mon'),
    ('Tue','Tue'),
    ('Wed','Wed'),
    ('Thu','Thu'),
    ('Fri','Fri'),
    ('Sat','Sat'),
    ('Sun','Sun'),
)

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

RERATIONSHIP_CHOICES=(
    ('Brother','Brother'),
    ('Mother','Mother'),
    ('Father','Father'),
    ('Gradfather','Gradfather'),
    ('Grandmother','Grandmother'),
    ('Uncle','Uncle'),
    ('Aunt','Aunt'),
    ('Cousin','Cousin'),
    ('Other','Other'),
)





class School(models.Model):
    school_of_Name=models.CharField(max_length=100,unique=True)
    Registration_Date=models.DateField(auto_now_add=True)
    def __str__(self):
        return  str(self.school_of_Name) 
    class Meta:
        verbose_name = _('School')
        verbose_name_plural = _('Schools ')


class Courses (models.Model):
   course_name=models.CharField(max_length=100,unique=True)
   school_of=models.ForeignKey(School, on_delete=models.CASCADE,blank=True, null=True)
   course_ID=models.IntegerField(unique=True,blank=True, null=True)
   course_description=models.TextField(max_length=1000,blank=True,null=True)
   duration=models.CharField(max_length=50)
   img=models.ImageField(upload_to='courses_images',blank=True, null=True)
   date_added=models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return str(self.course_name)
   class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
    
class Classes(models.Model):
    Class_Name=models.CharField(max_length=100,unique=True)
    Class_code=models.IntegerField(unique=True)
    Registration_Date=models.DateField(auto_now_add=True)
    def __str__(self):
        return  str(self.Class_Name) 
    
    class Meta:
        verbose_name = _('Class')
        verbose_name_plural = _('Classes ')
    

class Semester(models.Model):
    semester_name=models.CharField(max_length=50)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.semester_name)
    class Meta:
            verbose_name = _('Semester')
            verbose_name_plural = _('Semesters')



class Module(models.Model):
    module_name=models.CharField(max_length=50)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.module_name)
    class Meta:
            verbose_name = _('Module')
            verbose_name_plural = _('Modules')

class Departments (models.Model):
    Department_name=models.CharField(max_length=100,unique=True)
    department_id=models.IntegerField(unique=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Department_name
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
    

class Term (models.Model):
   term=models.CharField(max_length=100,unique=True)
   date_added=models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return str(self.term)
   class Meta:
        verbose_name = _('Term')
        verbose_name_plural = _('Terms')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    is_lecturer=models.BooleanField(default=False)
    is_parent=models.BooleanField(default=False)


    student_number=models.IntegerField(blank=True,null=True)
    module=models.ForeignKey(Module, on_delete=models.CASCADE,blank=True, null=True)
    semester=models.ForeignKey(Semester, on_delete=models.CASCADE,blank=True, null=True)
    national_ID=models.IntegerField(blank=True,null=True,unique=True)
    official_picture=models.ImageField(upload_to='pics',blank=True,null=True)
    dob=models.DateField(default=timezone.now)
    phone=models.IntegerField(blank=True,null=True)
    course_assigned= models.ForeignKey(Courses,on_delete=models.SET_NULL,blank=True,null=True)
    department= models.ForeignKey(Departments,on_delete=models.SET_NULL,null=True)
    class_assigned=models.ForeignKey(Classes,on_delete=models.SET_NULL,blank=True,null=True)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=100)
    intake=models.CharField(choices=INTAKE_CHOICES,max_length=100,blank=True, null=True)
    next_of_kin_firstname=models.CharField(max_length=200,blank=True,null=True)
    next_of_kin_middlename=models.CharField(max_length=200,blank=True,null=True)
    next_of_kin_lastname=models.CharField(max_length=200,blank=True,null=True)
    next_of_kin_relationship=models.CharField( max_length=40, choices=RERATIONSHIP_CHOICES,blank=True,null=True)
    next_of_kin_phone=models.IntegerField(blank=True,null=True)
    registration_number=models.CharField(max_length=100,unique=True)
    student_term=models.ForeignKey(Term, on_delete=models.CASCADE,blank=True, null=True)
    next_of_kin=models.CharField(max_length=100,blank=True, null=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'registration_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture=models.ImageField(upload_to='pics',default="np_pic.png")
    studied_at=models.CharField(max_length=200,blank=True,null=True)
    county=models.CharField(max_length=200,blank=True,null=True)
    location=models.CharField(max_length=200,blank=True,null=True)
    my_profile=models.CharField(max_length=200,blank=True,null=True)
    phone=models.CharField(max_length=200,blank=True,null=True)
    occupation=models.CharField(max_length=200,blank=True,null=True)
    education=models.CharField(max_length=200,blank=True,null=True)
    skills=models.CharField(max_length=200,blank=True,null=True)
    notes=models.CharField(max_length=200,blank=True,null=True)
    country =CountryField(blank=True,null=True)

    def __str__(self):
        return str(self.user.email)
    @receiver(post_save, sender=User)
    def create_user_p(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def save_user_p(sender, instance, **kwargs):
        instance.profile.save()



class Session (models.Model):
   session_year=models.IntegerField(unique=True)
   date_added=models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return str(self.session_year)
   class Meta:
        verbose_name = _('session')
        verbose_name_plural = _('sessions')

class Settings (models.Model):
   School_name=models.CharField(max_length=100)
   term=models.ForeignKey(Term, on_delete=models.CASCADE)
   session_year=models.ForeignKey(Session, on_delete=models.CASCADE)
   date_added=models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return str(self.School_name)
   class Meta:
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

class LessonsDuration (models.Model):
    start_time=models.CharField(max_length = 150)
    end_time=models.CharField(max_length = 150)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.start_time) + ' - ' + str(self.end_time)
    class Meta:
            verbose_name = _('Lessons Duration')
            verbose_name_plural = _('Lessons Durations')



class CourseUnit (models.Model):
    unit_name=models.CharField(max_length=50)
    course=models.ForeignKey(Courses, on_delete=models.CASCADE)
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.unit_name) 
    class Meta:
            verbose_name = _('Course Unit')
            verbose_name_plural = _('Course Units')


class Timetable (models.Model):
    class_ID= models.ForeignKey(Classes, on_delete=models.CASCADE)
    day=models.CharField(choices=DAY_CHOICES,max_length=100)
    time_dulation=models.ForeignKey(LessonsDuration, on_delete=models.CASCADE)
    unit_name = models.ForeignKey( CourseUnit, on_delete=models.CASCADE)
    lecturer_name = models.CharField(max_length = 150)
    lecturer_number = models.IntegerField()
    room=models.CharField(max_length = 150,blank=True, null=True)
    class_link=models.URLField(max_length=400,blank=True, null=True)
     
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.class_ID) + ' - ' + str(self.unit_name) + '  by Lecturer --->' + str(self.lecturer_name) + ' time --->' + str(self.time_dulation)
    class Meta:
            verbose_name = _('Timetable')
            verbose_name_plural = _('Timetables')

class Exam (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    year=models.IntegerField()
    student_registration_number=models.CharField( max_length=50)
    term =models.ForeignKey(Term,on_delete=models.CASCADE,blank=True, null=True)
    unit_name=models.CharField(max_length=50)
    cat_marks=models.IntegerField(default=0,blank=True, null=True)
    end_term_marks=models.IntegerField(default=0,blank=True, null=True)
    #total=models.IntegerField()
   #grade=models.CharField(max_length = 150)
    date_added=models.DateTimeField(auto_now_add=True)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return str(self.student_registration_number)
    class Meta:
            verbose_name = _('Exam Result')
            verbose_name_plural = _('Exam Results')
    def get_total(self):
        if self.cat_marks:
            if self.end_term_marks:
                return self.end_term_marks + self.cat_marks
   
    def get_grade(self):
        if self.cat_marks > 0 and self.end_term_marks > 0 : 
            grade=''
            total=self.get_total()
            if total >= 80:
                grade='DISTINCTION 1'
            elif total >= 71 :
                grade='DISTINCTION 2'
            elif total >=61 :
                grade='CREDIT 3'
            elif total >=51 :
                grade='CREDIT 4'
            elif total >=40 :
                grade='PASS 5'
            elif total >=20 :
                grade='REFER 6'
            else :
                grade='FAIL'
            return  grade


class AllStudentsAnnouncements (models.Model):
    title = models.CharField(max_length = 150)
    announcement=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.title)
    class Meta:
            verbose_name = _('Student Announcement')
            verbose_name_plural = _('All Students Announcements')

class DepartmentalStudentAnnouncement(models.Model):
    department=models.ForeignKey(Departments,on_delete=models.CASCADE)
    title = models.CharField(max_length = 150)
    announcement=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.department)
    class Meta:
            verbose_name = _('Students Departmental Announcement')
            verbose_name_plural = _(' Students Departmental Announcements')

class SpecificClassAnnouncement(models.Model):
    class_name=models.ForeignKey(Classes,on_delete=models.CASCADE)
    title = models.CharField(max_length = 150)
    announcement=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.class_name)
    class Meta:
            verbose_name = _('Specific Class Announcement')
            verbose_name_plural = _('Specific Class Announcements')


class SpecificStudentAnnouncement(models.Model):
    registration_number=models.IntegerField()
    title = models.CharField(max_length = 150)
    announcement=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.registration_number)
    class Meta:
            verbose_name = _('Specific Student Announcement')
            verbose_name_plural = _('Specific Students Announcements')

class ScheduleOnlineClass(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    target_class=models.ForeignKey(Classes, on_delete=models.CASCADE)
    day=models.CharField(choices=DAY_CHOICES, max_length=50)
    time=models.CharField(max_length=50)
    unit=models.CharField(max_length=50)
    class_link=models.URLField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.target_class)
    class Meta:
            verbose_name = _('Online Class')
            verbose_name_plural = _('Online Classes')


class Assignment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    to_class=models.ForeignKey(Classes, on_delete=models.CASCADE)
    assignment_title=models.CharField( max_length=50)
    assignment_instructions=models.TextField(max_length=700)
    questions=models.TextField(max_length=1000,blank=True, null=True)
    file=models.FileField( upload_to='files', max_length=1000,blank=True, null=True)
    deadline=models.DateField(auto_now_add=False)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.assignment_title)
    class Meta:
            verbose_name = _('Assignment')
            verbose_name_plural = _('Assignments')

class Messages(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    reply=models.TextField(max_length=300)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Sender : " + str(self.user)
    class Meta:
            verbose_name = _('Message')
            verbose_name_plural = _('Messages')



class ElearningLibraryResource(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Courses, on_delete=models.CASCADE)
    unit=models.CharField(max_length=50)
    typed_notes=models.TextField(max_length=1000)
    file=models.FileField(upload_to='files', max_length=100,blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.course) +' , '+ ' Unit ' + str(self.unit)
    class Meta:
            verbose_name = _('Elearning Library Resource')
            verbose_name_plural = _('Elearning Library Resources')


class GenerateNotice(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    description=models.TextField(max_length=500)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.title)
    class Meta:
            verbose_name = _('Generate Notice')
            verbose_name_plural = _('Generate Notices')

class OnlineApplication(models.Model):
    surname=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    other_names=models.CharField(max_length=50,blank=True, null=True)
    gender=models.CharField(choices=GENDER_CHOICES, max_length=50)
    dob=models.DateField( auto_now_add=False)
    nationality=models.CharField(max_length=50)
    national_id=models.IntegerField(blank=True, null=True)
    county=models.CharField( max_length=50)
    district=models.CharField( max_length=50,blank=True, null=True)
    town=models.CharField(max_length=50,blank=True, null=True)
    course_applied_for=models.CharField(choices=COURSE_LEVEL, max_length=50)
    course_name=models.ForeignKey(Courses, on_delete=models.CASCADE)
    email=models.EmailField( max_length=254)
    parent_or_guardian_tel=models.IntegerField()
    student_tel=models.IntegerField()
    approved=models.BooleanField(default=False)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return   str(self.surname)  +   str(self.first_name)
    class Meta:
            verbose_name = _('Online Application')
            verbose_name_plural = _('Online Applications')


class UploadedAssignments(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_code=models.IntegerField()
    file=models.FileField(upload_to='student_uploads', max_length=100)
    class_name=models.ForeignKey(Classes, on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.file)
    class Meta:
            verbose_name = _('Uploaded Assignment')
            verbose_name_plural = _('Uploaded Assignments')



class AllLecturersAnnouncements (models.Model):
    title = models.CharField(max_length = 150)
    announcement=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.title)
    class Meta:
            verbose_name = _('Lecturer Announcement')
            verbose_name_plural = _('Lecturer Announcements')


class AuditTrail(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    action=models.CharField(max_length=50)
    item=models.TextField(max_length=300)
    date=models.CharField(max_length=400)
    page=models.CharField(max_length=1000)
    description=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.user)
    class Meta:
            verbose_name = ('Audit Trail')
            verbose_name_plural = ('Audit Trail ' )

class AccountsLog(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    action=models.CharField(max_length=50)
    item=models.CharField(max_length=300)
    date=models.CharField(max_length=400)
    page=models.CharField(max_length=1000)
    description=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.user)
    class Meta:
            verbose_name = ('Accounts Log')
            verbose_name_plural = ('Accounts Logs ' )


class EnrollmentFee(models.Model):
    received_from = models.CharField(max_length = 150 )
    reg_no = models.CharField(max_length = 150 , unique=True)
    Registration_admission_fee=models.IntegerField(default=0 ,blank=True, null=True)
    Tution_fee=models.IntegerField(default=0,blank=True, null=True)
    boarding_hostel_fees=models.IntegerField(default=0,blank=True, null=True)
    repair_and_maintanance=models.IntegerField(default=0,blank=True, null=True)
    electricity_water_and_conservancy=models.IntegerField(default=0,blank=True, null=True)
    activity_fund=models.IntegerField(default=0,blank=True, null=True)
    medical_fud_insurance=models.IntegerField(default=0,blank=True, null=True)
    rent_hire=models.IntegerField(default=0,blank=True, null=True)
    examination=models.IntegerField(default=0,blank=True, null=True)
    computer_studies=models.IntegerField(default=0,blank=True, null=True)
    production_contracts=models.IntegerField(default=0,blank=True, null=True)
    evening_classes=models.IntegerField(default=0,blank=True, null=True)
    citc_uniform_badge_id_card_t_shirt=models.IntegerField(default=0,blank=True, null=True)
    sundry_debtors_fees_arrears=models.IntegerField(default=0,blank=True, null=True)
    income_genarating_act=models.IntegerField(default=0,blank=True, null=True)
    miscellaneous=models.IntegerField(default=0,blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.received_from)
    class Meta:
            verbose_name = ('Enrollment Fee')
            verbose_name_plural = ('Enrollment Fees ' )
    def total(self):
        return (self.Registration_admission_fee) + self.Tution_fee + self.boarding_hostel_fees +self.repair_and_maintanance + self.electricity_water_and_conservancy + self.activity_fund+self.medical_fud_insurance+self.rent_hire+self.examination+self.computer_studies+self.production_contracts+self.evening_classes+self.citc_uniform_badge_id_card_t_shirt+self.sundry_debtors_fees_arrears+self.income_genarating_act+self.miscellaneous
