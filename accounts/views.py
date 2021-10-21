from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#password change 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# FOR WEASY PRINT pdf zote
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
import tempfile
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import requests


from . forms import ProfileForm,approve_online_applications_form,EnrollmentFeeForm , update_parent_form,MessagesForm,parent_creation_form,UploadedAssignmentsForm,CourseUnitForm,OnlineApplicationForm,GenerateNoticeForm,ElearningLibraryResourceForm,AdminReplyMessageForm,student_creation_form,AssignmentForm,ScheduleOnlineClassForm,Settings_form,lecturer_creation_form,update_lecturer_form_form,update_student_form,add_class_form,Session_form,term_form,courses_form,department_form,superuser_creation_form,update_superuser_form,timetable_form,Exam_form,AllStudentsAnnouncements_form
from accounts.models import OnlineApplication,OnlineApplication,AuditTrail, EnrollmentFee, Profile,SpecificClassAnnouncement,AllLecturersAnnouncements,UploadedAssignments ,CourseUnit,GenerateNotice,ElearningLibraryResource,ScheduleOnlineClass,Messages,User,Assignment,Settings,Classes,Session,Exam,Term,Courses,Departments,Timetable,AllStudentsAnnouncements,DepartmentalStudentAnnouncement,SpecificClassAnnouncement,SpecificStudentAnnouncement
from .filters import student_filter_form,UploadedAssignmentsFilter,parent_filter_form,CourseUnitFilterForm,Course_filter,timetable_filter_form,ElearningLibraryResourceFilter,Exam_filter_form,lecturer_filter_form
from django.core.paginator import Paginator 




def loginuser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method=="POST":
        reg_no = request.POST.get('reg_no')
        password = request.POST.get('password')
        userlogin = authenticate(request, registration_number=reg_no, password=password)
        if userlogin is not None:
            login(request, userlogin)
            return redirect('dashboard')
        else:
            messages.info( request, 'Registration Number Or Password incorrect')
            return redirect('loginuser')
    return render (request,'accounts/login.html')

def loginstaff(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method=="POST":
        reg_no = request.POST.get('reg_no')
        password = request.POST.get('password')
        userlogin = authenticate(request, registration_number=reg_no, password=password)
        if userlogin is not None:
            login(request, userlogin)
            return redirect('dashboard')
        else:
            messages.info( request, 'Registration Number Or Password incorrect')
            return redirect('loginuser')
    return render (request,'accounts/loginstaff.html')

    

@login_required(login_url='loginuser')
def dashboard(request):
    if request.user.is_superuser:
        online_application_count=OnlineApplication.objects.count()
        settings=Settings.objects.all()
        student_count=User.objects.filter(is_student=True).count()
        active_students=User.objects.filter(is_student=True,is_active=True).count()
        superuser_count=User.objects.filter(is_superuser=True).count()
        all_users=User.objects.all().count()
        active_users=User.objects.filter(is_active=True).count()
        lecturers_count=User.objects.filter(is_lecturer=True).count()
        active_lecturers=User.objects.filter(is_lecturer=True,is_active=True).count()
        data=[student_count,lecturers_count,superuser_count,all_users]
        online_application_count=OnlineApplication.objects.all().count()
        messages_count=Messages.objects.all().count()
        total_active_user=User.objects.filter(is_active=True).count()
        total_parents=User.objects.filter(is_parent=True).count()
   
        return render (request,'accounts/dashboard.html',{'settings':settings,'student_count':student_count,'superuser_count':superuser_count,'all_users':all_users,'active_users':active_users,'lecturers_count':lecturers_count,'data':data,'online_application_count':online_application_count,'messages_count':messages_count,'total_active_user':total_active_user,'online_application_count':online_application_count,'total_parents':total_parents,'active_students':active_students,'active_lecturers':active_lecturers})
    elif request.user.is_student:
        settings=Settings.objects.all()
        student_class=request.user.class_assigned
        student_course=request.user.course_assigned
        student_email=request.user.email
        student_department=request.user.department
        timetable=Timetable.objects.filter(class_ID=request.user.class_assigned)
        form=timetable_filter_form(request.GET,queryset=timetable)
        timetable=form.qs
        timetable_count=timetable.count()
        online_classs_count=ScheduleOnlineClass.objects.filter(target_class=student_class).count()
        messages_count=Messages.objects.filter(user=request.user).count()
        assignment_count=Assignment.objects.filter(to_class=student_class).count()
        module=request.user.module
        units=CourseUnit.objects.filter(course=student_course,module=module)
        print(units)
        return render (request,'accounts/dashboard.html',{'student_course':student_course,'student_email':student_email,'student_department':student_department,'timetable':timetable,'settings':settings,'form':form,'timetable_count':timetable_count,'online_classs_count':online_classs_count,'messages_count':messages_count,'assignment_count':assignment_count,'units':units,'module':module})
    elif request.user.is_lecturer:
        timetable=Timetable.objects.filter(lecturer_number=request.user.registration_number)
        form=timetable_filter_form(request.GET,queryset=timetable)
        timetable=form.qs
        timetable_count=timetable.count()
        messages_count=Messages.objects.filter(user=request.user).count()
        print(messages_count)
        return render (request,'accounts/dashboard.html',{'timetable':timetable,'form':form,'timetable_count':timetable_count,'messages_count':messages_count})
    elif request.user.is_parent:
        student_no=request.user.student_number
        print(student_no,'ddd')
        user_obj=User.objects.filter(registration_number=student_no)
        for x in user_obj:
            student_course=x.course_assigned
            class_assigned=x.class_assigned
        print(student_course)
        
        return render (request,'accounts/dashboard.html',{'student_course':student_course,'class_assigned':class_assigned})

    else:
        return render (request,'accounts/dashboard.html')

@login_required(login_url='loginuser')
def profile(request):
    form=ProfileForm()
    return render(request,'accounts/profile.html',{'form':form})

@login_required(login_url='loginuser')
def updateprofile(request,pk):
    form=ProfileForm(instance=request.user.profile)
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            user=request.user
            action='Profile Update'
            date=datetime.now()
            
            page=request.META.get('HTTP_REFERER')
            description= ("User {} updated profile On Page {} ".format(request.user.registration_number,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            messages.info(request,'Your Profile Information Has Been Successfully Updated ')
            return redirect('viewprofile')   
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request,'accounts/profile.html',{'form':form})

@login_required(login_url='loginuser')
def viewprofile(request):
    profile_objects=Profile.objects.filter(user=request.user)
    return render(request,'accounts/viewprofile.html',{'profile_objects':profile_objects})

def logoutuser(request):
    logout(request)
    return redirect('loginuser') 

@login_required(login_url='loginuser')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # update pass yenye ilikuwa james 
            messages.success(request, 'Your password was successfully updated!')
            user=request.user
            action='Password Change'
            date=datetime.now()
            page=request.META.get('HTTP_REFERER')
            description= ("User {} chenged password  On Page {} ".format(request.user.registration_number,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

@login_required(login_url='loginuser')
def register_students_view(request):
    if request.user.is_superuser:
        student_count=User.objects.filter(is_student=True).count()
        form=student_creation_form()
        if request.method=="POST":
            form=student_creation_form(request.POST,request.FILES)
            if form.is_valid():
                form.save()
            
              #  user=str(form.cleaned_data.get('email'))
     
            #     reg_no=str(form.cleaned_data.get('registration_number'))
            #     p=str(form.cleaned_data.get('password1'))
            #     print(user)
            #     msg='Dear ' + user + 'Registration Was Successfully  You can login using Registration Number : ' + reg_no + 'Password : ' + p
            #     send_mail(
            #    'MOMBASA CITC',
            #     msg,
            #     settings.EMAIL_HOST_USER,
            #     [user],
            #     fail_silently=False,
            #     )
            #     inf='Another Student was registered '
            #     send_mail(
            #    'CITC MOMBASA',
            #     inf,
            #     settings.EMAIL_HOST_USER,
            #     ['kamirijames11@gmail.com'],
            #     fail_silently=False,
            #     )
                
                user=request.user
                action=' Student Registration'
                date=datetime.now()
                item=str(form.cleaned_data.get('registration_number'))
                page=request.META.get('HTTP_REFERER')
                description= ("User {} REGISTERED  {}  On Page {} ".format(user,item,request.META.get('HTTP_REFERER')))
                obj=AuditTrail.objects.create(
                user=user,
                action=action,
                page=page,
                description=description,
                date=date,
                )
                obj.save()
                adm=str(form.cleaned_data.get('registration_number'))
                messages.success(request,'Registration for student ADM : '+ adm + ' Completed successfuly !')
                return redirect('register_students_view')
    else:
        return redirect('/')

    return render(request,'accounts/register_students.html',{'form':form,'student_count':student_count})



@login_required(login_url='loginuser')
def settings_view(request):
    if request.user.is_superuser:
        s=Settings.objects.all()
        if not s:
            form=Settings_form() 
            if request.method=="POST":
                form=Settings_form(request.POST)
                if form.is_valid():
                    form.save() 
                    messages.success(request,'Settings have been successfully Added')
                    return redirect('settings_view')
        else:
            form=Settings_form() 
            messages.warning(request,'You can only have one settings instance kindly edit or delete the current one incase you want to change system settings')
    else:
        return redirect('/')
    return render(request,'accounts/settings.html',{'form':form,'s':s})

@login_required(login_url='loginuser')
def update_settings(request,pk):
    if request.user.is_superuser:
        i=Settings.objects.get(id=pk)
        s=Settings.objects.all()
        form=Settings_form(instance=i) 
        if request.method=="POST":
            form=Settings_form(request.POST,instance=i)
            if form.is_valid():
                form.save() 
                messages.success(request,'Settings have been successfully updated ')
                return redirect('settings_view')
    else:
        return redirect('/')
    return render(request,'accounts/settings.html',{'form':form,'s':s})





@login_required(login_url='loginuser')
def View_all_students(request):
    if request.user.is_superuser:
        students=User.objects.filter(is_student=True).order_by('-date_joined')
        form=student_filter_form(request.GET,queryset=students)
        students=form.qs
        
        search_count=students.count()
        paginator=Paginator(students,100)
        page=request.GET.get('page')
        students=paginator.get_page(page)
    else:
        return redirect('/')
    return render(request,'accounts/view_all_students.html',{'students':students,'form':form,'search_count':search_count})


@login_required(login_url='loginuser')
def update_students_form(request):
    if request.user.is_superuser:
        form=update_student_form()
    else:
        return redirect('/')
    return render(request,'accounts/update_students_form.html',{'form':form})


@login_required(login_url='loginuser')
def update_students(request,pk):
    if request.user.is_superuser:
        i=User.objects.get(id=pk)
        form=update_student_form(instance=i)
        if request.method=="POST":
            form=update_student_form(request.POST,request.FILES,instance=i)
            if form.is_valid():
                form.save()
                adm=str(form.cleaned_data.get('registration_number'))
                messages.success(request,'Student ADM '+ adm + '  Details Updated  successfuly !')
                user=request.user
                action=' Student Update'
                date=datetime.now()
                item=str(form.cleaned_data.get('registration_number'))
                page=request.META.get('HTTP_REFERER')
                description= ("User {}  updated {}  On Page {} ".format(user,item,request.META.get('HTTP_REFERER')))
                obj=AuditTrail.objects.create(
                user=user,
                action=action,
                page=page,
                description=description,
                date=date,
                item=item,
                )
                obj.save()
                return redirect('View_all_students')
    else:
        return redirect('/')
    return render(request,'accounts/update_students_form.html',{'form':form})

@login_required(login_url='loginuser')
def delete_student(request,pk):
    if request.user.is_superuser:
        student=User.objects.get(id=pk)
        if request.method=="POST":
            student.delete()
            messages.info(request,'Student deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=student
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted {} On Page {} ".format(request.user.registration_number,student,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('View_all_students')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_student.html',{'student':student})


@login_required(login_url='loginuser')
def add_class_view(request):
    if request.user.is_superuser:
        class_count=Classes.objects.all().count()
        form=add_class_form()
        if request.method=="POST":
            form=add_class_form(request.POST)
            if form.is_valid():
                form.is_valid()
                form.save()
                messages.info(request,'Class Added Succesfully')
                return redirect ('view_classes')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_class_form.html',{'form':form,'class_count':class_count})


@login_required(login_url='loginuser')
def view_classes(request):
    if request.user.is_superuser:
        classes=Classes.objects.all()
        classes_count=classes.count()
    else:
        return redirect("dashboard")

    return render (request,'accounts/view_classes.html',{'classes':classes,'classes_count':classes_count})
    

@login_required(login_url='loginuser')
def update_class(request,pk):
    if request.user.is_superuser:
        i=Classes.objects.get(id=pk)
        class_count=Classes.objects.all().count()
        form=add_class_form(instance=i)
        if request.method=="POST":
            form=add_class_form(request.POST,instance=i)
            if form.is_valid():
                form.save()
                messages.info(request,'Class Updated Succesfully')
                return redirect ('view_classes')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_class_form.html',{'form':form,'class_count':class_count})

@login_required(login_url='loginuser')
def delete_class(request,pk):
    if request.user.is_superuser:
        class_name=Classes.objects.get(id=pk)
        if request.method=="POST":
            class_name.delete()
            messages.warning(request,'Class deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=class_name
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,class_name,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_classes')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_class.html',{'class_name':class_name})


@login_required(login_url='loginuser')
def delete_settings(request,pk):
    if request.user.is_superuser:
        s=Settings.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.warning(request,'Settings deleted succesfully')
            return redirect('settings_view')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_settings.html',{'s':s})

@login_required(login_url='loginuser')
def session_view(request):
    if request.user.is_superuser:
        form=Session_form()
        if request.method=="POST":
            form=Session_form(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request,'Session Added succesfully')
                return redirect('view_session')
    else:
        return redirect("dashboard")
    return render (request,'accounts/session_form.html',{'form':form})


@login_required(login_url='loginuser')
def update_session(request,pk):
    if request.user.is_superuser:
        i=Session.objects.get(id=pk)
        form=Session_form(instance=i)
        if request.method=="POST":
            form=Session_form(request.POST,instance=i)
            if form.is_valid():
                form.save()
                messages.info(request,'Session Updated succesfully')
                return redirect('view_session')
    else:
        return redirect("dashboard")
    return render (request,'accounts/session_form.html',{'form':form})

    


@login_required(login_url='loginuser')
def view_session(request):
    if request.user.is_superuser:
       sessions=Session.objects.all()
       count=sessions.count()
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_session.html',{'sessions':sessions,'count':count})


@login_required(login_url='loginuser')
def delete_session(request,pk):
    if request.user.is_superuser:
        s=Session.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.warning(request,'Session deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=s
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,s,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_session')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_session.html',{'s':s})
    
@login_required(login_url='loginuser')
def add_term_view(request):
    if request.user.is_superuser:
        term_count=Term.objects.all().count()
        form=term_form()
        if request.method=="POST":
            form=term_form(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request,'Term Added succesfully')
                return redirect('view_term')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_term.html',{'form':form,'term_count':term_count})

@login_required(login_url='loginuser')
def update_term_view(request,pk):
    if request.user.is_superuser:
        i=Term.objects.get(id=pk)
        term_count=Term.objects.all().count()
        form=term_form(instance=i)
        if request.method=="POST":
            form=term_form(request.POST,instance=i)
            if form.is_valid():
                form.save()
                messages.info(request,'Term Updated succesfully')
                return redirect('view_term')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_term.html',{'form':form,'term_count':term_count})

@login_required(login_url='loginuser')
def view_term(request):
    if request.user.is_superuser:
        obj=Term.objects.all()
        term_count=obj.count()
    else:
        return redirect("dashboard")

    return render (request,'accounts/view_term.html',{'obj':obj,'term_count':term_count})
    

@login_required(login_url='loginuser')
def delete_term(request,pk):
    if request.user.is_superuser:
        t=Term.objects.get(id=pk)
        if request.method=="POST":
            t.delete()
            messages.warning(request,'Term deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=t
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,t,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_term')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_term.html',{'t':t})



@login_required(login_url='loginuser')
def add_courses_view(request):
    if request.user.is_superuser:
        courses_count=Courses.objects.all().count()
        form=courses_form()
        if request.method=="POST":
            form=courses_form(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.info(request,'Course Added succesfully')
                return redirect('view_courses')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_courses.html',{'form':form,'courses_count':courses_count})

def update_courses(request,pk):
    if request.user.is_superuser:
        i=Courses.objects.get(id=pk)
        courses_count=Courses.objects.all().count()
        form=courses_form(instance=i)
        if request.method=="POST":
            form=courses_form(request.POST,request.FILES,instance=i)
            if form.is_valid():
                form.save()
                messages.info(request,'Course Updated succesfully')
                return redirect('view_courses')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_courses.html',{'form':form,'courses_count':courses_count})

@login_required(login_url='loginuser')
def view_courses_view(request):
    if request.user.is_superuser:
        x=Courses.objects.all()
        courses_count=x.count()
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_courses.html',{'x':x,'courses_count':courses_count})
    

@login_required(login_url='loginuser')
def delete_course(request,pk):
    if request.user.is_superuser:
        t=Courses.objects.get(id=pk)
        if request.method=="POST":
            t.delete()
            messages.warning(request,'Course deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=t
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,t,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_courses')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_course.html',{'t':t})



@login_required(login_url='loginuser')
def add_department_view(request):
    if request.user.is_superuser:
        department_count=Departments.objects.all().count()
        form=department_form()
        if request.method=="POST":
            form=department_form(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request,'Department Added succesfully')
                return redirect('view_department')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_department.html',{'form':form,'department_count':department_count})

@login_required(login_url='loginuser')
def view_department(request):
    if request.user.is_superuser:
        x=Departments.objects.all()
        department_count=x.count()
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_department.html',{'department_count':department_count,'x':x})


@login_required(login_url='loginuser')
def update_department_view(request,pk):
    if request.user.is_superuser:
        i=Departments.objects.get(id=pk)
        department_count=Departments.objects.all().count()
        form=department_form(instance=i)
        if request.method=="POST":
            form=department_form(request.POST,instance=i)
            if form.is_valid():
                form.save()
                messages.info(request,'Department Updated succesfully')
                return redirect('view_department')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_department.html',{'form':form,'department_count':department_count})



@login_required(login_url='loginuser')
def delete_department(request,pk):
    if request.user.is_superuser:
        t=Departments.objects.get(id=pk)
        if request.method=="POST":
            t.delete()
            messages.warning(request,'Department deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=t
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,t,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_department')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_department.html',{'t':t})



  
@login_required(login_url='loginuser')
def pdf_timetable_export(request):
    if request.user.is_student:
        timetable=Timetable.objects.filter(class_ID=request.user.class_assigned)
        get_date=datetime.now()
        first_name=request.user.first_name
        last_name=request.user.last_name
        u=request.user
        class_a=request.user.class_assigned
        get_programme=request.user.course_assigned
        get_department=request.user.department
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="TIMETABLE"

        # Rendered
        html_string = render_to_string('accounts/pdf_timetable_export.html', {'u':u,'timetable': timetable,'get_date':get_date,'first_name':first_name,'last_name':last_name,'class_a':class_a,'get_programme':get_programme,'get_department':get_department,'school_name':school_name})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; Timetable.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response


@login_required(login_url='loginuser')
def member_staff(request):
    if request.user.is_superuser:
        u=request.user
        staff=User.objects.filter(is_superuser=True)
        superuser_count=staff.count()
    else:
        return redirect("dashboard")

    return render (request,'accounts/view_member_staff.html',{'staff':staff,'superuser_count':superuser_count})

@login_required(login_url='loginuser')
def register_superuser(request):
    if request.user.is_superuser:
        form=superuser_creation_form()
        if request.method=="POST":
            form=superuser_creation_form(request.POST)
            if form.is_valid():
                form.save()
                user=str(form.cleaned_data.get('email'))
                reg_no=str(form.cleaned_data.get('registration_number'))
                p=str(form.cleaned_data.get('password1'))
                print(user)
                msg='Dear ' + user + ' Registration Was Successfully  You can login using Registration Number : ' + reg_no + 'Password : ' + p
                send_mail(
               'SUPERUSER REGISTRATION',
                msg,
                settings.EMAIL_HOST_USER,
                [user],
                fail_silently=False,
                )
                inf='Mambo Jay Another SUPERUSER was registered , you programmed me'
                send_mail(
               'HELLO JAMES_SVG',
                inf,
                settings.EMAIL_HOST_USER,
                ['kamirijames11@gmail.com'],
                fail_silently=False,
                )
                
                user=request.user
                action=' Superuser Registration'
                date=datetime.now()
                item=str(form.cleaned_data.get('registration_number'))
                page=request.META.get('HTTP_REFERER')
                description= ("User {} REGISTERED  {}  On Page {} ".format(user,item,request.META.get('HTTP_REFERER')))
                obj=AuditTrail.objects.create(
                user=user,
                action=action,
                page=page,
                description=description,
                date=date,
                )
                obj.save()
                messages.info(request,'Superuser have been successfully registerd')
                return redirect('member_staff')

    else:
        return redirect("dashboard")

    return render (request,'accounts/register_superuser.html',{'form':form})

@login_required(login_url='loginuser')
def superuser_update_form(request):
    if request.user.is_superuser:
        form=update_superuser_form()
    else:
        return redirect("dashboard")

    return render (request,'accounts/superuser_update_form.html',{'form':form})


@login_required(login_url='loginuser')
def update_superuser(request,pk):
    if request.user.is_superuser:
        i=User.objects.get(id=pk)
        form=update_superuser_form(instance=i)
        if request.method=="POST":
            form=update_superuser_form(request.POST , instance=i)
            if form.is_valid():
                form.save()
                messages.info(request,'Superuser updated successfully')
                user=request.user
                action=' Superuser Update'
                date=datetime.now()
                item=str(form.cleaned_data.get('registration_number'))
                page=request.META.get('HTTP_REFERER')
                description= ("User {}  updated {}  On Page {} ".format(user,item,request.META.get('HTTP_REFERER')))
                obj=AuditTrail.objects.create(
                user=user,
                action=action,
                page=page,
                description=description,
                date=date,
                item=item,
                )
                obj.save()
                
                return redirect('member_staff')
    else:
        return redirect("dashboard")

    return render (request,'accounts/superuser_update_form.html',{'form':form})


@login_required(login_url='loginuser')
def delete_superuser(request,pk):
    if request.user.is_superuser:
        t=User.objects.get(id=pk)
        if request.method=="POST":
            t.delete()
            messages.warning(request,'Superuser deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=t
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted Superuser {} On Page {} ".format(request.user.registration_number,t,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('member_staff')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_superuser.html',{'t':t})


@login_required(login_url='loginuser')
def add_timetable(request):
    if request.user.is_superuser:
       timetable_count=Timetable.objects.all().count()
       form=timetable_form()
       if request.method=="POST":
           form=timetable_form(request.POST)
           if form.is_valid():
               form.save()
               messages.info(request,'Timetable Added succesfully')
               return redirect('view_timetable')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_timetable.html',{'form':form,'timetable_count':timetable_count})

@login_required(login_url='loginuser')
def update_timetable(request,pk):
    if request.user.is_superuser:
       i=Timetable.objects.get(id=pk)
       timetable_count=Timetable.objects.all().count()
       form=timetable_form(instance=i)
       if request.method=="POST":
           form=timetable_form(request.POST,instance=i)
           if form.is_valid():
               form.save()
               messages.info(request,'Timetable Updated succesfully')
               return redirect('view_timetable')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_timetable.html',{'form':form,'timetable_count':timetable_count})




@login_required(login_url='loginuser')
def view_timetable(request):
    if request.user.is_superuser:
      obj=Timetable.objects.all()
      form=timetable_filter_form(request.GET,queryset=obj)
      obj=form.qs
      c=obj.count()
    else:
        return redirect("dashboard")

    return render (request,'accounts/view_timetable.html',{'obj':obj,'c':c,'form':form})

@login_required(login_url='loginuser')
def delete_timetable(request,pk):
    if request.user.is_superuser:
        t=Timetable.objects.get(id=pk)
        if request.method=="POST":
            t.delete()
            messages.warning(request,'Timetable deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=t
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,t,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_timetable')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_timetable.html',{'t':t})

@login_required(login_url='loginuser')  
def add_exam_ressults(request):
    if request.user.is_superuser or request.user.is_lecturer: 
        form=Exam_form()
        if request.method=="POST":
            form=Exam_form(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.info(request,'Examination Result created Successfully ')
                return redirect('view_results_admin')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_exam_resut.html',{'form':form})

@login_required(login_url='loginuser')
def Update_exam_result(request,pk):
    if request.user.is_superuser:
        i=Exam.objects.get(id=pk)
        form=Exam_form(instance=i)
        if request.method=="POST":
            form=Exam_form(request.POST,instance=i)
            if form.is_valid():
                form.save()
                messages.info(request,'Examination Result Updated Successfully ')
                return redirect('view_results_admin')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_exam_resut.html',{'form':form})

@login_required(login_url='loginuser')
def view_results_admin(request):
    if request.user.is_superuser or request.user.is_lecturer:
        exam=Exam.objects.filter(user=request.user)
        c=exam.count()
        form=Exam_filter_form(request.GET,queryset=exam)
        exam=form.qs
        paginator=Paginator(exam,100)
        page=request.GET.get('page')
        exam=paginator.get_page(page)
 
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_results_admin.html',{'exam':exam,'c':c,'form':form})
    

@login_required(login_url='loginuser')
def delete_exam_result(request,pk):
    if request.user.is_superuser:
        t=Exam.objects.get(id=pk)
        if request.method=="POST":
            t.delete()
            messages.warning(request,'Exam Result deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=t
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,t,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_results_admin')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_exam_result.html',{'t':t})




@login_required(login_url='loginuser')
def view_exam_result_student(request):
    if request.user.is_student or request.user.is_parent :
        if request.user.is_student:
            student_reg_no=request.user.registration_number
        else:
            student_reg_no=request.user.student_number
        result=Exam.objects.filter(student_registration_number=student_reg_no)
        result_count=result.count()
        form=Exam_filter_form(request.GET,queryset=result)
        result=form.qs
        count=result.count()
        total=0
        for x in result:
            if x.cat_marks >  0 and x.end_term_marks > 0 :
                total= total + x.get_total()
            else:
                pass
        average_grade=0
        print(total,'total mks ')
        try:
            average_grade=(total/count)
        except ZeroDivisionError:
            pass
        print(average_grade,'average_grade')
        
        average_grade_for_all_units=''
        if average_grade >= 80:
            average_grade_for_all_units='DISTINCTION 1'
        elif total >= 71 :
            average_grade_for_all_units='DISTINCTION 2'
        elif total >=61 :
            average_grade_for_all_units='CREDIT 3'
        elif total >=51 :
            average_grade_for_all_units='CREDIT 4'
        elif total >=40 :
            average_grade_for_all_units='PASS 5'
        elif total >=20 :
            average_grade_for_all_units='REFER 6'
        else :
            average_grade_for_all_units='FAIL'
            
    else:
        return redirect("dashboard")

    return render (request,'accounts/view_exam_result_student.html',{'result':result,'result_count':result_count,'form':form,'total':total,'average_grade_for_all_units':average_grade_for_all_units})

    

@login_required(login_url='loginuser')
def pdf_student_exam_export(request):
    if request.user.is_student or request.user.is_parent:
        if request.user.is_student:
            student_reg_no=request.user.registration_number
            result=Exam.objects.filter(student_registration_number=student_reg_no)
            get_date=datetime.now()
            first_name=request.user.first_name
            last_name=request.user.last_name
            u=request.user
            class_a=request.user.class_assigned
            get_programme=request.user.course_assigned
            get_department=request.user.department
        else:
            get_date=datetime.now()
            student_reg_no=request.user.student_number
            result=Exam.objects.filter(student_registration_number=student_reg_no)
            obj=User.objects.filter(registration_number=student_reg_no)
            for x in obj:
                u=x.registration_number
                class_a=x.class_assigned
                first_name=x.first_name
                last_name=x.last_name
                get_programme=x.course_assigned
                get_department=x.department
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="TIMETABLE"
        # Rendered
        html_string = render_to_string('accounts/pdf_student_exam_export.html', {'u':u,'result': result,'get_date':get_date,'first_name':first_name,'last_name':last_name,'class_a':class_a,'get_programme':get_programme,'get_department':get_department,'school_name':school_name})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; Timetable.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response

@login_required(login_url='loginuser')
def register_lecturer(request):
    if request.user.is_superuser:
        form=lecturer_creation_form()
        if request.method=="POST":
            form=lecturer_creation_form(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                user=request.user
                action=' Lecturer Registration'
                date=datetime.now()
                item=str(form.cleaned_data.get('registration_number'))
                page=request.META.get('HTTP_REFERER')
                description= ("User {} REGISTERED  {}  On Page {} ".format(user,item,request.META.get('HTTP_REFERER')))
                obj=AuditTrail.objects.create(
                user=user,
                action=action,
                page=page,
                description=description,
                date=date,
                )
                obj.save()
                user=str(form.cleaned_data.get('email'))
                reg_no=str(form.cleaned_data.get('registration_number'))
                p=str(form.cleaned_data.get('password1'))
                print(user)
                msg='Dear ' + user + 'Registration Was Successfully  You can login using Registration Number : ' + reg_no + 'Password : ' + p
                send_mail(
               'LECTURER REGISTRATION',
                msg,
                settings.EMAIL_HOST_USER,
                [user],
                fail_silently=False,
                )
                inf='Mambo Jay Another Student was registered , you programmed me'
                send_mail(
               'HELLO JAMES_SVG',
                inf,
                settings.EMAIL_HOST_USER,
                ['kamirijames11@gmail.com'],
                fail_silently=False,
                )
                
                lec=str(form.cleaned_data.get('registration_number'))
                messages.success(request,'Registration for Lecturer Number : '+ lec + ' Completed successfuly !')
                return redirect('view_all_lecturers')

    else:
        return redirect("dashboard")

    return render (request,'accounts/register_lecturer.html',{'form':form})

    
@login_required(login_url='loginuser')
def view_all_lecturers(request):
    if request.user.is_superuser:
        obj=User.objects.filter(is_lecturer=True).order_by('-date_joined')
        form=lecturer_filter_form(request.GET,queryset=obj)
        obj=form.qs
        total_lec=obj.count()
        paginator=Paginator(obj,100)
        page=request.GET.get('page')
        obj=paginator.get_page(page)
        
    else:
        return redirect("dashboard")

    return render (request,'accounts/view_all_lecturers.html',{'obj':obj,'total_lec':total_lec,'form':form})


@login_required(login_url='loginuser')
def update_lecturer_form(request):
    if request.user.is_superuser:
       form=update_lecturer_form_form()         
    else:
        return redirect("dashboard")

    return render (request,'accounts/update_lecturer_form.html',{'form':form})

@login_required(login_url='loginuser')
def edit_lec(request,pk):
    if request.user.is_superuser:
        i=User.objects.get(id=pk)
        form=update_lecturer_form_form(instance=i) 
        if request.method=="POST":
            form=update_lecturer_form_form(request.POST,request.FILES,instance=i)
            if form.is_valid():
                form.save() 
                code=str(form.cleaned_data.get('registration_number'))    
                messages.info(request,'Lecturer number ' + code  + ' Updated Successfully')  
                user=request.user
                action=' Lecturer Update'
                date=datetime.now()
                item=str(form.cleaned_data.get('registration_number'))
                page=request.META.get('HTTP_REFERER')
                description= ("User {}  updated {}  On Page {} ".format(user,item,request.META.get('HTTP_REFERER')))
                obj=AuditTrail.objects.create(
                user=user,
                action=action,
                page=page,
                description=description,
                date=date,
                item=item,
                )
                obj.save()
                return redirect('view_all_lecturers') 
    else:
        return redirect("dashboard")

    return render (request,'accounts/update_lecturer_form.html',{'form':form})


@login_required(login_url='loginuser')
def delete_lec(request,pk):
    if request.user.is_superuser:
        lec=User.objects.get(id=pk)
        if request.method=="POST":
            lec.delete()
            messages.info(request,'Lecturer deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=lec
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted Lectuter {} On Page {} ".format(request.user.registration_number,lec,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_all_lecturers')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_lec.html',{'lec':lec})



 
@login_required(login_url='loginuser')
def pdf_all_students_export(request):
    if request.user.is_superuser:
        
        get_date=datetime.now()
        u=request.user.first_name
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="ALL STUDENTS"
        students=User.objects.filter(is_student=True)
        # Rendered
        html_string = render_to_string('accounts/pdf_students.html', {'get_date':get_date,'u':u,'school_name':school_name,'students':students})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; Students.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response


@login_required(login_url='loginuser')
def add_all_student_announcement(request):
    if request.user.is_superuser:
       announcement_count=AllStudentsAnnouncements.objects.all().count()
       form=AllStudentsAnnouncements_form()
       if request.method=="POST":
            form=AllStudentsAnnouncements_form(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request,'Announcement Sent to all students ' )
                return redirect('admin_view_all_student_announcement')

    else:
        return redirect("dashboard")

    return render (request,'accounts/add_all_student_announcement.html',{'form':form,'announcement_count':announcement_count})

@login_required(login_url='loginuser')
def update_all_student_announcement(request,pk):
    if request.user.is_superuser:
       i=AllStudentsAnnouncements.objects.get(id=pk)
       announcement_count=AllStudentsAnnouncements.objects.all().count()
       form=AllStudentsAnnouncements_form(instance=i)
       if request.method=="POST":
            form=AllStudentsAnnouncements_form(request.POST,instance=i)
            if form.is_valid():
                form.save()
                messages.info(request,'Announcement Updated Successfully ' )
                return redirect('admin_view_all_student_announcement')

    else:
        return redirect("dashboard")

    return render (request,'accounts/add_all_student_announcement.html',{'form':form,'announcement_count':announcement_count})


@login_required(login_url='loginuser')
def admin_view_all_student_announcement(request):
    if request.user.is_superuser:
       announcement=AllStudentsAnnouncements.objects.all()
       count=announcement.count()
    else:
        return redirect("dashboard")
    return render (request,'accounts/admin_view_all_student_announcement.html',{'announcement':announcement,'count':count})


@login_required(login_url='loginuser')
def delete_all_student_announcement(request,pk):
    if request.user.is_superuser:
        s=AllStudentsAnnouncements.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.warning(request,'Announcement deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=s
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,s,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('admin_view_all_student_announcement')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_all_student_announcement.html',{'s':s})

@login_required(login_url='loginuser')
def pdf_all_lecturers_export(request):
    if request.user.is_superuser:
        get_date=datetime.now()
        u=request.user.first_name
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="ALL LECTURER"
        lecturer=User.objects.filter(is_lecturer=True)
        # Rendered
        html_string = render_to_string('accounts/pdf_lecturer.html', {'get_date':get_date,'u':u,'school_name':school_name,'lecturer':lecturer})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; lecturers.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response
@login_required(login_url='loginuser')
def pdf_all_superusers_export(request):
    if request.user.is_superuser:
        get_date=datetime.now()
        u=request.user.first_name
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="ALL SUPERUSERS"
        superuser=User.objects.filter(is_superuser=True)
        # Rendered
        html_string = render_to_string('accounts/pdf_superusers.html', {'get_date':get_date,'u':u,'school_name':school_name,'superuser':superuser})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; lecturers.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response

@login_required(login_url='loginuser')
def add_online_class(request):
    if request.user.is_superuser or request.user.is_lecturer:
        class_count=ScheduleOnlineClass.objects.all().count()
        form=ScheduleOnlineClassForm()    
        if request.method=="POST":
            form=ScheduleOnlineClassForm(request.POST,request.FILES)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.info(request,'Class Has Been Set ')     
                print('cool')
                return redirect('view_online_class_adm_lec')
    else:
        return redirect("dashboard")
    return render (request,'accounts/add_online_class.html',{'form':form,'class_count':class_count})

@login_required(login_url='loginuser')
def update_online_class(request,pk):
    if request.user.is_superuser or request.user.is_lecturer:
        i=ScheduleOnlineClass.objects.get(id=pk)
        class_count=ScheduleOnlineClass.objects.all().count()
        form=ScheduleOnlineClassForm(instance=i)    
        if request.method=="POST":
            form=ScheduleOnlineClassForm(request.POST,request.FILES,instance=i)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.info(request,'Class Has Been Updated ')     
                print('cool')
                return redirect('view_online_class_adm_lec')
    else:
        return redirect("dashboard")
    return render (request,'accounts/add_online_class.html',{'form':form,'class_count':class_count})


@login_required(login_url='loginuser')
def view_online_class_adm_lec(request):
    if request.user.is_superuser or request.user.is_lecturer:
       user=request.user
       obj=ScheduleOnlineClass.objects.filter(user=user)
       count=obj.count()
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_online_class_adm_lec.html',{'obj':obj,'count':count})

@login_required(login_url='loginuser')
def delete_online_class(request,pk):
    if request.user.is_superuser or request.user.is_lecturer:
        s=ScheduleOnlineClass.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.info(request,'Online Class Deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=s
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,s,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_online_class_adm_lec')
    else:
        return redirect("dashboard")
    return render (request,'accounts/delete_online_class.html',{'s':s})


@login_required(login_url='loginuser')
def add_assignment(request):
    if request.user.is_superuser or request.user.is_lecturer:
      form=AssignmentForm()
      if request.method=="POST":
            form=AssignmentForm(request.POST,request.FILES)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                print('assignment posted')
                messages.info(request,'Assignment Has Been Posted')
                return redirect('view_assignment_adm_lec')
    else:
        return redirect("dashboard")
    return render (request,'accounts/add_assignment.html',{'form':form})

@login_required(login_url='loginuser')
def update_assignment_adm_lec(request,pk):
    if request.user.is_superuser or request.user.is_lecturer:
      i=Assignment.objects.get(id=pk)
      form=AssignmentForm(instance=i)
      if request.method=="POST":
            form=AssignmentForm(request.POST,request.FILES,instance=i)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                print('assignment posted')
                messages.info(request,'Assignment Has Been Updated')
                return redirect('view_assignment_adm_lec')
    else:
        return redirect("dashboard")
    return render (request,'accounts/add_assignment.html',{'form':form})


@login_required(login_url='loginuser')
def view_assignment_adm_lec(request):
    if request.user.is_superuser or request.user.is_lecturer:
      asg=Assignment.objects.filter(user=request.user)
      count=asg.count()
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_assignment_adm_lec.html',{'asg':asg,'count':count})


@login_required(login_url='loginuser')
def delete_assignment_adm_lec(request,pk):
    if request.user.is_superuser or request.user.is_lecturer:
        s=Assignment.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.warning(request,'Assignment deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=s
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,s,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_assignment_adm_lec')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_assignment_adm_lec.html',{'s':s})
    
@login_required(login_url='loginuser')
def student_view_own_online_classes(request):
    if request.user.is_student:
        online_classes=ScheduleOnlineClass.objects.filter(target_class=request.user.class_assigned)
        count=online_classes.count()
    else:
        return redirect("dashboard")
    return render (request,'accounts/student_view_own_online_classes.html',{'online_classes':online_classes,'count':count})
    

@login_required(login_url='loginuser')
def view_announcements_students(request):
    if request.user.is_student or request.user.is_parent :
        if request.user.is_student:
            all_students_announcements=AllStudentsAnnouncements.objects.all()
            all_s_announcements_count=all_students_announcements.count()
            departmental=DepartmentalStudentAnnouncement.objects.filter(department=request.user.department)
            specific_class=SpecificClassAnnouncement.objects.filter(class_name=request.user.class_assigned)
            specific_student=SpecificStudentAnnouncement.objects.filter(registration_number=request.user.registration_number)
        else:
            registration_number=request.user.student_number
            print (registration_number)
            user=User.objects.filter(registration_number=registration_number)
            for x in user:
                department=x.department
                class_name=x.class_assigned
            all_students_announcements=AllStudentsAnnouncements.objects.all()
            all_s_announcements_count=all_students_announcements.count()
            departmental=DepartmentalStudentAnnouncement.objects.filter(department=department)
            specific_class=SpecificClassAnnouncement.objects.filter(class_name=class_name)
            specific_student=SpecificStudentAnnouncement.objects.filter(registration_number=registration_number)

                

    else:
        return redirect("dashboard")
    return render (request,'accounts/view_announcements_students.html',{'all_students_announcements':all_students_announcements,'all_s_announcements_count':all_s_announcements_count,'departmental':departmental,'specific_class':specific_class,'specific_student':specific_student})
    
@login_required(login_url='loginuser')
def add_message_lec_std(request):
    if request.user.is_student or request.user.is_lecturer:
        msg=Messages.objects.filter(user=request.user)
        count=msg.count()
        form=MessagesForm()
        if request.method=="POST":
            form=MessagesForm(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.warning(request,'Message Sent succesfully')     
    else:
        return redirect("dashboard")
    return render (request,'accounts/add_message_lec_std.html',{'form':form,'msg':msg,'count':count})
    
@login_required(login_url='loginuser')
def view_all_messages_adm(request):
    if request.user.is_superuser:
        msg=Messages.objects.all()
        total=msg.count()
        not_replied=Messages.objects.filter(reply__isnull=True).count() 
        replied=total-not_replied    
       
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_all_messages_adm.html',{'msg':msg,'total':total,'not_replied':not_replied,'replied':replied})


@login_required(login_url='loginuser')
def admin_reply_message_form(request):
    if request.user.is_superuser:
        form=AdminReplyMessageForm()
       
    else:
        return redirect("dashboard")
    return render (request,'accounts/admin_reply_message_form.html',{'form':form})

@login_required(login_url='loginuser')
def update_admin_reply_message(request,pk):
    if request.user.is_superuser:
        i=Messages.objects.get(id=pk)
        form=AdminReplyMessageForm(instance=i)
        if request.method=="POST":
            form=AdminReplyMessageForm(request.POST,instance=i)
            if form.is_valid():
                form.save()
                messages.warning(request,'Reply Sent succesfully') 
                return redirect('view_all_messages_adm')
    else:
        return redirect("dashboard")
    return render (request,'accounts/admin_reply_message_form.html',{'form':form})
    

@login_required(login_url='loginuser')
def delete_message_adm(request,pk):
    if request.user.is_superuser:
        i=Messages.objects.get(id=pk)
        if request.method=="POST":
            i.delete()
            messages.info(request,'Message deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=i
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,i,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_all_messages_adm')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_message_adm.html',{'i':i})

@login_required(login_url='loginuser')
def view_assignment_student(request):
    if request.user.is_student:
       a=UploadedAssignments.objects.filter(user=request.user)
       asg=Assignment.objects.filter(to_class=request.user.class_assigned)
       count=asg.count()
       form=UploadedAssignmentsForm()
       if request.method=="POST":
            form=UploadedAssignmentsForm(request.POST,request.FILES)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.info(request,'Assignment Submitted Successfully')
                print("woo")
       
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_assignment_student.html',{'asg':asg,'count':count,'form':form,'a':a})

@login_required(login_url='loginuser')
def update_assignment_student(request,pk):
    if request.user.is_student:
       i=UploadedAssignments.objects.get(id=pk)
       a=UploadedAssignments.objects.filter(user=request.user)
       asg=Assignment.objects.filter(to_class=request.user.class_assigned)
       count=asg.count()
       form=UploadedAssignmentsForm(instance=i)
       if request.method=="POST":
            form=UploadedAssignmentsForm(request.POST,request.FILES,instance=i)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.info(request,'Assignment Updated Successfully')
                return redirect('view_assignment_student')
       
    else:
        return redirect("dashboard")
    return render (request,'accounts/view_assignment_student.html',{'asg':asg,'count':count,'form':form,'a':a})



@login_required(login_url='loginuser')
def pdf_assignment_export(request):
    if request.user.is_student:
        asg=Assignment.objects.filter(to_class=request.user.class_assigned)
        get_date=datetime.now()
        first_name=request.user.first_name
        last_name=request.user.last_name
        u=request.user
        class_a=request.user.class_assigned
        get_programme=request.user.course_assigned
        get_department=request.user.department
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="ASSIGNMENTS"

        # Rendered
        html_string = render_to_string('accounts/pdf_assignment_export.html', {'u':u,'asg': asg,'get_date':get_date,'first_name':first_name,'last_name':last_name,'class_a':class_a,'get_programme':get_programme,'get_department':get_department,'school_name':school_name})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; Assignments.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response


@login_required(login_url='loginuser')
def AddElearningLibraryResouurce(request):
    if request.user.is_lecturer or request.user.is_superuser:
        resources=ElearningLibraryResource.objects.filter(user=request.user)
        count=resources.count()
        form=ElearningLibraryResourceForm() 
        if request.method=="POST":
            form=ElearningLibraryResourceForm(request.POST,request.FILES)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.info(request,'Resource Submitted Successfully')
                return redirect('ViewElearningLibraryResouurceLec')
    else:
        return redirect("dashboard")

    return render (request,'accounts/AddElearningLibraryResouurce.html',{'form':form,'count':count})

@login_required(login_url='loginuser')
def UpdateElearningLibraryResouurce(request,pk):
    if request.user.is_lecturer or request.user.is_superuser:
        i=ElearningLibraryResource.objects.get(id=pk)
        form=ElearningLibraryResourceForm(instance=i) 
        if request.method=="POST":
            form=ElearningLibraryResourceForm(request.POST,request.FILES,instance=i)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                print('woo')
                messages.info(request,'Resource Updated Successfully')
                return redirect('ViewElearningLibraryResouurceLec')
    else:
        return redirect("dashboard")

    return render (request,'accounts/AddElearningLibraryResouurce.html',{'form':form})


@login_required(login_url='loginuser')
def ViewElearningLibraryResouurceLec(request):
    if request.user.is_lecturer or request.user.is_superuser:
       resources=ElearningLibraryResource.objects.filter(user=request.user)
       count=resources.count()
    else:
        return redirect("dashboard")

    return render (request,'accounts/ViewElearningLibraryResouurceLec.html',{'resources':resources,'count':count})



@login_required(login_url='loginuser')
def delete_elearning_resource(request,pk):
    if request.user.is_lecturer or request.user.is_superuser:
        s=ElearningLibraryResource.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.info(request,'Resource deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=s
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,s,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('ViewElearningLibraryResouurceLec')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_elearning_resource.html',{'s':s})

@login_required(login_url='loginuser')
def ViewLibraryStudentLec(request):
    if request.user.is_student or request.user.is_lecturer or request.user.is_superuser:
        resources=ElearningLibraryResource.objects.all()
        form=ElearningLibraryResourceFilter(request.GET,queryset=resources)
        resources=form.qs
        count=resources.count()
    else:
        return redirect("dashboard")

    return render (request,'accounts/ViewLibraryStudentLec.html',{'resources':resources,'count':count,'form':form})


@login_required(login_url='loginuser')
def pdf_timetable_export_lecturer(request):
    if request.user.is_lecturer:
        timetable=Timetable.objects.filter(lecturer_number=request.user.registration_number)
        get_date=datetime.now()
        first_name=request.user.first_name
        last_name=request.user.last_name
        u=request.user
        get_department=request.user.department
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="TIMETABLE"

        # Rendered
        html_string = render_to_string('accounts/pdf_timetable_lec_export.html', {'u':u,'timetable': timetable,'get_date':get_date,'first_name':first_name,'last_name':last_name,'get_department':get_department,'school_name':school_name})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; LecturerTimetable.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response


@login_required(login_url='loginuser')
def generate_a_printing_notice(request):
    if  request.user.is_superuser:
        notice=GenerateNotice.objects.all()
        count=notice.count()
        form=GenerateNoticeForm()
        if request.method=="POST":
            form=GenerateNoticeForm(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.info(request,'notice Has Been Added ')     
                print('cool')
                return redirect('generate_a_printing_notice')
    else:
        return redirect("dashboard")

    return render (request,'accounts/generate_a_printing_notice.html',{'form':form,'notice':notice,'count':count})

@login_required(login_url='loginuser')
def update_generate_a_printing_notice(request,pk):
    if  request.user.is_superuser:
        i=GenerateNotice.objects.get(id=pk)
        notice=GenerateNotice.objects.all()
        form=GenerateNoticeForm(instance=i)
        if request.method=="POST":
            form=GenerateNoticeForm(request.POST,instance=i)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                messages.info(request,'notice Has Been Updated ')     
                print('cool')
                return redirect('generate_a_printing_notice')
    else:
        return redirect("dashboard")

    return render (request,'accounts/generate_a_printing_notice.html',{'form':form,'notice':notice})

@login_required(login_url='loginuser')
def delete_notice_adm(request,pk):
    if request.user.is_superuser:
        i=GenerateNotice.objects.get(id=pk)
        if request.method=="POST":
            i.delete()
            messages.info(request,'Notice deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=i
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,i,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('generate_a_printing_notice')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_notice_adm.html',{'i':i})

@login_required(login_url='loginuser')
def pdf_notice_admin(request):
    if request.user.is_superuser:
        notice=GenerateNotice.objects.all()
        get_date=datetime.now()
        u=request.user
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="NOTICE"

        # Rendered
        html_string = render_to_string('accounts/pdf_notice_admin.html', {'u':u,'notice': notice,'get_date':get_date,'school_name':school_name})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; notice.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response


def online_applications(request):
    if not request.user.is_authenticated:
        form=OnlineApplicationForm()
        if request.method=="POST":
            form=OnlineApplicationForm(request.POST)
            if form.is_valid():
                form.save()
                user=str(form.cleaned_data.get('email'))
                course_name=str(form.cleaned_data.get('course_name'))
                print(user)
                print(course_name)
                msg='Dear ' + user + 'Your Application has been received and will be processed for more information email us on info@citcmombasa.co.ke or call us Tel:+254 718 393 125 . thank you for choosing us '
                msg_for_admin= 'Hello '+ user + ' has aapplied for ' + course_name
                send_mail(
               'Christian Industrial Training Centre (CICT) Mombasa ',
                msg,
                settings.EMAIL_HOST_USER,
                [user],
                fail_silently=False,
                )
                send_mail(
               'Christian Industrial Training Centre (CICT) Mombasa  ',
                msg_for_admin,
                settings.EMAIL_HOST_USER,
                ['kamirijames11@gmail.com','info@citcmombasa.co.ke'],
                fail_silently=False,
                )
                messages.info( request,'Your application Has been successfully submitted and will be processed within 24Hrs for more information email us on info@citcmombasa.co.ke or call us Tel:+254 718 393 125 . thank you for choosing us !')
                
    else:
        return redirect('dashboard')
    return render (request,'accounts/online_applications.html',{'form':form})




@login_required(login_url='loginuser')
def add_course_unit(request):
    if request.user.is_superuser:
        count=CourseUnit.objects.all().count()
        form=CourseUnitForm()
        if request.method=="POST":
            form=CourseUnitForm(request.POST)
            if form.is_valid():
                form.save()
                unit_name=str(form.cleaned_data.get('unit_name'))
                course=str(form.cleaned_data.get('course'))
                module=str(form.cleaned_data.get('module'))
                messages.info(request, unit_name + ' Unit ' + ' added for  ' +  course + module)
                print('woo')
                return redirect('view_course_unit_admin')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_course_unit.html',{'form':form,'count':count})


@login_required(login_url='loginuser')
def update_course_unit(request,pk):
    if request.user.is_superuser:
        i=CourseUnit.objects.get(id=pk)
        count=CourseUnit.objects.all().count()
        form=CourseUnitForm(instance=i)
        if request.method=="POST":
            form=CourseUnitForm(request.POST,instance=i)
            if form.is_valid():
                form.save()
                unit_name=str(form.cleaned_data.get('unit_name'))
                course=str(form.cleaned_data.get('course'))
                module=str(form.cleaned_data.get('module'))
                messages.info(request, unit_name + ' Unit ' + ' Updated for  ' +  course + module)
                print('woo')
                return redirect('view_course_unit_admin')
    else:
        return redirect("dashboard")

    return render (request,'accounts/add_course_unit.html',{'form':form,'count':count})


@login_required(login_url='loginuser')
def view_course_unit_admin(request):
    if request.user.is_superuser:
        units=CourseUnit.objects.all()
        form=CourseUnitFilterForm(request.GET,queryset=units)
        units=form.qs
        count=units.count()
    else:
        return redirect("dashboard")

    return render (request,'accounts/view_course_unit_admin.html',{'units':units,'count':count,'form':form})




@login_required(login_url='loginuser')
def delete_course_unit(request,pk):
    if request.user.is_superuser:
        i=CourseUnit.objects.get(id=pk)
        if request.method=="POST":
            i.delete()
            messages.info(request,'Unit deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=i
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,i,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_course_unit_admin')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_course_unit.html',{'i':i})



def about(request):
    a=AboutPage.objects.all()
    return render (request,'frontend/about.html',{'a':a})
def courses(request):
    c=Courses.objects.all()
    form=Course_filter(request.GET,queryset=c)
    c=form.qs
    count=c.count()
    return render (request,'frontend/courses.html',{'c':c,'form':form,'count':count})
def accredition(request):
    a=Accreditation.objects.all()
    return render (request,'frontend/accredition.html',{'a':a})


def news_events(request):
    o=NewsEvents.objects.all()   
    return render (request,'frontend/news_events.html',{'o':o})
def admission(request):
    a=Admission.objects.all()
    return render (request,'frontend/admission.html',{'a':a})
def alumni(request):
    form=Alumniform()
    if request.method=="POST":
        form=Alumniform(request.POST)
        if form.is_valid():
            form.save()
            i=form.cleaned_data.get('name')
            messages.info(request,'Dear , ' + i + ' You have been registered successfully')
    return render (request,'frontend/alumni.html',{'form':form})


# @login_required(login_url='loginuser')
# def delete_assignment_adm_lec(request,pk):
#     if request.user.is_superuser or request.user.is_lecturer:
#         s=Assignment.objects.get(id=pk)
#         if request.method=="POST":
#             s.delete()
#             messages.warning(request,'Assignment deleted succesfully')
#             return redirect('view_assignment_adm_lec')
#     else:
#         return redirect("dashboard")
#     return render (request,'accounts/delete_assignment_student.html',{'s':s})

@login_required(login_url='loginuser')
def delete_assignment_adm_lec_std_upload(request,pk):
    if request.user.is_superuser or request.user.is_lecturer:
        s=UploadedAssignments.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.warning(request,'Assignment deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=s
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,s,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('adm_lec_view_std_uploads')
    else:
        return redirect("dashboard")
    return render (request,'accounts/delete_assignment_student_upload.html',{'s':s})

@login_required(login_url='loginuser')
def delete_upload_student_own_assignment(request,pk):
    if request.user.is_student:
        s=UploadedAssignments.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.warning(request,'Assignment deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=s
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,s,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_assignment_student')
    else:
        return redirect("dashboard")
    return render (request,'accounts/delete_upload_student_own_assignment.html',{'s':s})




@login_required(login_url='loginuser')
def adm_lec_view_std_uploads(request):
    if request.user.is_superuser or request.user.is_lecturer:
        data=UploadedAssignments.objects.filter(assignment_code=request.user.registration_number)
        form=UploadedAssignmentsFilter(request.GET,queryset=data)
        data=form.qs
        count=data.count()
    else:
        return redirect("dashboard")

    return render (request,'accounts/adm_lec_view_std_uploads.html',{'data':data,'count':count,'form':form})


def languages(request):
    return render (request,'frontend/cert_early_edu.html')



def computer_studies(request):
    return render (request,'frontend/ict.html')



def business(request):
    return render (request,'frontend/business.html')


def music(request):
    return render (request,'frontend/cert_BA.html')


def hospitality(request):
    return render (request,'frontend/dhfo.html')


def engineering(request):
    return render (request,'frontend/eng.html')

def education(request):
    return render (request,'frontend/edu.html')


@login_required(login_url='loginuser')
def lec_announcement(request):
    if request.user.is_lecturer:
        o=AllLecturersAnnouncements.objects.all()
        return render (request,'accounts/lec_announcement.html',{'o':o})
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def admin_view_online_aplications(request):
    if request.user.is_superuser:
        applications =OnlineApplication.objects.all()
        count=applications.count()
        approved_count=OnlineApplication.objects.filter(approved=True).count()
        not_approved= count - approved_count
        return render (request,'accounts/view_online_aplications_admin.html',{'applications':applications,'count':count,'approved_count':approved_count,'not_approved':not_approved})
    else:
        return redirect('dashboard')


  
@login_required(login_url='loginuser')
def pdf_export_online_application(request,pk):
    if request.user.is_superuser:
        data=OnlineApplication.objects.get(id=pk)
        get_date=datetime.now()
        u=request.user
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="Online Application"

        # Rendered
        html_string = render_to_string('accounts/pdf_export_online_application.html', {'u':u,'get_date':get_date,'school_name':school_name,'data':data})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; application.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response



@login_required(login_url='loginuser')
def register_parent(request):
    if request.user.is_superuser:
        form=parent_creation_form()
        if request.method=='POST':
            form=parent_creation_form(request.POST)
            if form.is_valid():
                form.save()
                user=str(form.cleaned_data.get('email'))
                reg_no=str(form.cleaned_data.get('registration_number'))
                p=str(form.cleaned_data.get('password1'))
                print(user)
                msg='Dear ' + user + 'Registration Was Successfully  You can login using Registration Number : ' + reg_no + 'Password : ' + p
                send_mail(
               'PARENT REGISTRATION',
                msg,
                settings.EMAIL_HOST_USER,
                [user],
                fail_silently=False,
                )
                inf='Mambo Jay Another Student was registered , you programmed me'
                send_mail(
               'HELLO JAMES_SVG',
                inf,
                settings.EMAIL_HOST_USER,
                ['kamirijames11@gmail.com'],
                fail_silently=False,
                )
                
                u=form.cleaned_data.get('registration_number')
                s=form.cleaned_data.get('student_number')
                messages.info(request,"Parent With Registration Number " +  u + " Registered Successfully . parent/guardian to " +  s)
                user=request.user
                action=' Parent Registration'
                date=datetime.now()
                item=str(form.cleaned_data.get('registration_number'))
                page=request.META.get('HTTP_REFERER')
                description= ("User {} REGISTERED  {}  On Page {} ".format(user,item,request.META.get('HTTP_REFERER')))
                obj=AuditTrail.objects.create(
                user=user,
                action=action,
                page=page,
                description=description,
                date=date,
                )
                obj.save()

        return render (request,'accounts/register_parent.html',{'form':form})
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def view_parents(request):
    if request.user.is_superuser:
        obj=User.objects.filter(is_parent=True)
        form=parent_filter_form(request.GET,queryset=obj)
        obj=form.qs
        count=obj.count()
        paginator=Paginator(obj,100)
        page=request.GET.get('page')
        obj=paginator.get_page(page)
        
        return render (request,'accounts/view_parents.html',{'obj':obj,'count':count,'form':form})
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def parent_update_form(request):
    if request.user.is_superuser:
        form=update_parent_form()
        return render (request,'accounts/update__parent_form.html',{'form':form})
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def update_parent(request,pk):
    if request.user.is_superuser:
        i=User.objects.get(id=pk)
        form=update_parent_form(instance=i)
        if request.method == 'POST':
            form=update_parent_form(request.POST ,instance=i)
            if form.is_valid():
                form.save()
                messages.info(request , "Parent Information updated successfully ")
                user=request.user
                action=' Parent Update'
                date=datetime.now()
                item=str(form.cleaned_data.get('registration_number'))
                page=request.META.get('HTTP_REFERER')
                description= ("User {}  updated {}  On Page {} ".format(user,item,request.META.get('HTTP_REFERER')))
                obj=AuditTrail.objects.create(
                user=user,
                action=action,
                page=page,
                description=description,
                date=date,
                item=item,
                )
                obj.save()
                return redirect('view_parents')


        return render (request,'accounts/update__parent_form.html',{'form':form})
    else:
        return redirect('dashboard')



@login_required(login_url='loginuser')
def delete_parent(request,pk):
    if request.user.is_superuser:
        s=User.objects.get(id=pk)
        if request.method=="POST":
            s.delete()
            messages.info(request,'Parent deleted succesfully')
            user=request.user
            action='Deleted'
            date=datetime.now()
            item=s
            page=request.META.get('HTTP_REFERER')
            description= ("User {} Deleted  {} On Page {} ".format(request.user.registration_number,s,request.META.get('HTTP_REFERER')))
            obj=AuditTrail.objects.create(
            user=user,
            action=action,
            page=page,
            description=description,
            date=date,
            )
            obj.save()
            return redirect('view_parents')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_parent.html',{'s':s})

 
@login_required(login_url='loginuser')
def pdf_export_parents(request):
    if request.user.is_superuser:
        data=User.objects.filter(is_parent=True)
        get_date=datetime.now()
        u=request.user
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="Online Application"

        # Rendered
        html_string = render_to_string('accounts/pdf_export_parents.html', {'u':u,'get_date':get_date,'school_name':school_name,'data':data})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; parents.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response







@login_required(login_url='loginuser')
def pdf_export_single_student(request,pk):
    if request.user.is_superuser:
        data=User.objects.get(id=pk)
        get_date=datetime.now()
        u=request.user
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="Student Details "

        # Rendered
        html_string = render_to_string('accounts/pdf_export_single_student.html',{'data':data,'u':u,'get_date':get_date,'school_name':school_name})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; single_student.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response


@login_required(login_url='loginuser')
def online_application_approval(request):
    if request.user.is_superuser:
      form=approve_online_applications_form()
    else:
        return redirect("dashboard")

    return render (request,'accounts/online_application_approval_form.html',{'form':form})




@login_required(login_url='loginuser')
def update_online_application_approval(request,pk):
    if request.user.is_superuser:
      i=OnlineApplication.objects.get(id=pk)
      form=approve_online_applications_form(instance=i)
      if request.method=="POST":
        form=approve_online_applications_form(request.POST,instance=i)
        if form.is_valid():
            form.save()
            return redirect('admin_view_online_aplications')
    else:
        return redirect("dashboard")

    return render (request,'accounts/online_application_approval_form.html',{'form':form})


@login_required(login_url='loginuser')
def adm_fee(request):
    if request.user.is_superuser:
        form=EnrollmentFeeForm()
        if request.method=="POST":
            form=EnrollmentFeeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('vw_en_fee')
    else:
        return redirect("dashboard")

    return render (request,'accounts/adm_fee.html',{'form':form})



@login_required(login_url='loginuser')
def edt_adm_fee(request , pk):
    if request.user.is_superuser:
        a=EnrollmentFee.objects.get(id=pk)
        form=EnrollmentFeeForm(instance=a)
        if request.method=="POST":
            form=EnrollmentFeeForm(request.POST , instance=a)
            if form.is_valid():
                form.save()
                return redirect('vw_en_fee')
    else:
        return redirect("dashboard")

    return render (request,'accounts/adm_fee.html',{'form':form})




@login_required(login_url='loginuser')
def vw_en_fee(request):
    if request.user.is_superuser:
        d=EnrollmentFee.objects.all()
    else:
        return redirect("dashboard")

    return render (request,'accounts/vw_en_fee.html',{'d':d})






 
@login_required(login_url='loginuser')
def pdf_adm_fee(request, pk):
    if request.user.is_superuser:
        data=EnrollmentFee.objects.get(id=pk)
        get_date=datetime.now()
        u=request.user
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="ADM FEE"

        # Rendered
        html_string = render_to_string('accounts/pdf_adm_fee.html', {'u':u,'get_date':get_date,'school_name':school_name,'data':data})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; parents.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response
