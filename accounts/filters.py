import django_filters
from django_filters import CharFilter
from . models import User,Timetable,Exam,ElearningLibraryResource,CourseUnit,Courses,UploadedAssignments



class student_filter_form(django_filters.FilterSet):
    #registration_number=CharFilter(field_name='registration_number',lookup_expr='icontains',label="Registration No")
    national_ID=CharFilter(field_name='national_ID',lookup_expr='icontains',label="National ID")
    registration_number=CharFilter(field_name='registration_number',lookup_expr='icontains',label="Reg No")
    
    class Meta:
          model=User
          fields=(
           'registration_number','email','national_ID','module',
           'course_assigned','department','gender','intake','class_assigned'
          )
class lecturer_filter_form(django_filters.FilterSet):
   # registration_number=CharFilter(field_name='registration_number',lookup_expr='icontains',label="Lecturer No")
    national_ID=CharFilter(field_name='national_ID',lookup_expr='icontains',label="National ID")
    class Meta:
          model=User
          fields=(
           'registration_number','email','national_ID',
           'department','gender'
          )


class timetable_filter_form(django_filters.FilterSet):
    unit_name=CharFilter(field_name='unit_name',lookup_expr='icontains',label="Unit Name")
    lecturer_name=CharFilter(field_name='lecturer_name',lookup_expr='icontains',label="Lecturer Name")
    class Meta:
          model=Timetable
          fields=(
            'day', 'unit_name','lecturer_name','class_ID','lecturer_number'
          )

class Exam_filter_form(django_filters.FilterSet):
    year=CharFilter(field_name='year',lookup_expr='icontains',label="Exam Year")
    student_registration_number=CharFilter(field_name='student_registration_number',lookup_expr='icontains',label="Registration Number")
    unit_name=CharFilter(field_name='unit_name',lookup_expr='icontains',label="Unit Name ")
    class Meta:
          model=Exam
          fields=(
          'student_registration_number',  'year', 'term','module','unit_name'
          )


class ElearningLibraryResourceFilter(django_filters.FilterSet):
    unit=CharFilter(field_name='unit',lookup_expr='icontains',label="Unit")
    class Meta:
          model=ElearningLibraryResource
          fields=(
            'course', 'unit'
          )

class CourseUnitFilterForm(django_filters.FilterSet):
    unit_name=CharFilter(field_name='unit_name',lookup_expr='icontains',label="Unit name ")
    class Meta:
          model=CourseUnit
          fields=(
            'unit_name','course','module'
          )


class Course_filter(django_filters.FilterSet):
    course_name=CharFilter(field_name='course_name',lookup_expr='icontains',label="Course Name ")
    class Meta:
          model=Courses
          fields=(
              'course_name','school_of'
          )
class UploadedAssignmentsFilter(django_filters.FilterSet):
#    user=CharFilter(field_name='user',lookup_expr='icontains',label="Reg No ")
    class Meta:
          model=UploadedAssignments
          fields=(
              'class_name','user'
          )





class parent_filter_form(django_filters.FilterSet):
    registration_number=CharFilter(field_name='registration_number',lookup_expr='icontains',label="Registration No")
    national_ID=CharFilter(field_name='national_ID',lookup_expr='icontains',label="National ID")
    class Meta:
          model=User
          fields=(
           'registration_number','email','national_ID','student_number'
          )