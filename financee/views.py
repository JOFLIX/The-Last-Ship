from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Settings,User
from . models import FeesParticulars,FeePayment
from .forms import FeePaymentForm
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
import tempfile
from django.http import HttpResponse
from .models import FeePayment,AuditTrailFinance
from .filters import FeePaymentfilter,StudentFilter
from django.core.paginator import Paginator 

@login_required(login_url='loginuser')
def myfee(request):
    if request.user.is_student:
        student_course=request.user.course_assigned
        settings=Settings.objects.all()
        for obj in settings:
            current_term=obj.term
            current_year=obj.session_year
        fees_particular=FeesParticulars.objects.filter(course=student_course , year=current_year  , term=current_term )
        amount_payable=0
        for x in fees_particular:
            amount_payable=amount_payable + x.amount
        my_fee=FeePayment.objects.filter(registration_number=request.user.registration_number).order_by('-date_paid')
        return render(request,'finance/myfee.html',{'fees_particular':fees_particular,'amount_payable':amount_payable,'my_fee':my_fee})
    else:
        return redirect('dashboard')



@login_required(login_url='loginuser')
def addfee(request):
    if request.user.is_superuser:
        reg_no=request.POST.get('reg_search')
        student_exist=User.objects.filter(registration_number=reg_no,is_student=False)
        if  student_exist and  not reg_no==None :
            messages.info(request,'That Registration Number Belongs to a staff not a student  ')
        student_result=User.objects.filter(registration_number=reg_no)
        pm=request.POST.get('pm')
        code=request.POST.get('code')
        print(pm,'payment method')
        print(code ,'code wamocho')
        fees_obj = FeePayment.objects.filter(registration_number = reg_no)
        i=0
        for x in fees_obj:
            i = x.id
            if x.id > i:
                i = x.id
        payment_data_on_search = FeePayment.objects.filter(id = i)
        current_arrears_on_search=0
        for x in payment_data_on_search:
            current_arrears_on_search=x.current_arrears

        value_reg=0
        for x in student_result:
            value_reg=x.registration_number
        if reg_no and  not student_result:
            messages.info(request,'Student With That Registration Number Does NOT Exist')
        print(student_result)
        reg_no=request.POST.get('reg')
        amount_paid=request.POST.get('amount')
        student_data = User.objects.filter(registration_number=reg_no)
        if reg_no and not student_data :
            messages.info(request,'A Student with that registration number does not exist')

        #Check whether the student reg_no entered exists in the database
        settings=Settings.objects.all()
        fees_payment_data = {}
        for obj in settings:
            current_year=obj.session_year
            current_term=obj.term
            print(current_term)
            print(current_year)
        for data in student_data:
            student_course=data.course_assigned
            student_module=data.module
            first_name=data.first_name
            last_name=data.last_name

            fees_particular=FeesParticulars.objects.filter(course=student_course , year=current_year  , term=current_term )
            
            this_term_amount_payable=0
            for x in fees_particular:
                this_term_amount_payable=this_term_amount_payable + x.amount
                print(this_term_amount_payable,'hii term lipa hii')

            fees_payment_data = FeePayment.objects.filter(registration_number = reg_no)
            print("Checking if the student exists in the Fee Payment Records")
            if fees_payment_data:
                print("Students is not a new student payment data exists ")
                i = -1
                #Looking for latest payment for the student given
                print("Checking if student Has Ever Paid")
                for x in fees_payment_data:
                    i = x.id
                    if x.id > i:
                        i = x.id
                #Extract the Record for the latest payment
                print("Extracting Records of the latest payments")
                extracted_record = FeePayment.objects.filter(id = i)
                prev_arrear = 0
                #Looking for previous balance
                print("Checking Previous Balance")
                for x in extracted_record:
                    #If the latest payment was this term
                    if (x.year == current_year) and (x.term == current_term):
                        print("The Student's latest payment was this term")
                        prev_arrear = x.current_arrears
                    #If the latest payment was last term
                    else:
                        print("The Student's latest payment was last term")
                        prev_arrear = this_term_amount_payable + x.current_arrears 
                 
                current_arrear = prev_arrear - float(amount_paid) 
                fee_payment=FeePayment.objects.create(
                    registration_number=reg_no,student_name=first_name ,course=student_course,module=student_module,year=current_year,term=current_term,prev_arrears=prev_arrear,amount_paid=amount_paid,current_arrears=current_arrear,payment_mthd=pm,reference_number_or_mpesa_code=code
                )
                fee_payment.save()
                user=request.user
                action='Fee Payment '
                date=datetime.now()
                item=f'Paid KES {amount_paid} For Student Reg no {reg_no}'
                page=request.META.get('HTTP_REFERER')
                description= ("User {} Added Fee for   {} On Page {} ".format(request.user.registration_number,reg_no,request.META.get('HTTP_REFERER')))
                obj=AuditTrailFinance.objects.create(
                    user=user,
                    action=action,
                    page=page,
                    description=description,
                    date=date,
                    item=item,
                    )
                obj.save()
                return redirect('viewfee')
            else:
                print("The Student is a NEW One")
                prev_arrear = this_term_amount_payable
                current_arrear = prev_arrear - float(amount_paid)
                fee_payment=FeePayment.objects.create(
                    registration_number=reg_no,student_name=first_name ,course=student_course,module=student_module,year=current_year,term=current_term,prev_arrears=prev_arrear,amount_paid=amount_paid,current_arrears=current_arrear,payment_mthd=pm,reference_number_or_mpesa_code=code
                )
                fee_payment.save()
                user=request.user
                action='Fee Payment '
                date=datetime.now()
                item=f'Paid KES {amount_paid} For Student Reg no {reg_no}'
                page=request.META.get('HTTP_REFERER')
                description= ("User {} Added Fee for   {} On Page {} ".format(request.user.registration_number,reg_no,request.META.get('HTTP_REFERER')))
                obj=AuditTrailFinance.objects.create(
                    user=user,
                    action=action,
                    page=page,
                    description=description,
                    date=date,
                    item=item,
                    )
                obj.save()
                return redirect('viewfee')
        #print(fee_payment)
        form=FeePaymentForm()

        return render(request,'finance/addfee.html',{'form':form,'fees_payment_data':fees_payment_data,'reg_no':reg_no,'student_result':student_result,'value_reg':value_reg,'current_arrears_on_search':current_arrears_on_search,'student_exist':student_exist})
    else:
        return redirect('dashboard')



# @login_required(login_url='loginuser')
# def viewfee(request):
#     if request.user.is_superuser:
#         fees_payment_data = FeePayment.objects.all().order_by('-date_paid')
#         return render(request,'finance/viewfee.html',{'fees_payment_data':fees_payment_data})
#     else:
#         return redirect('dashboard')



  
@login_required(login_url='loginuser')
def studentfeestructure(request):
    if request.user.is_student:
        get_date=datetime.now()
        first_name=request.user.first_name
        last_name=request.user.last_name
        u=request.user
        class_a=request.user.class_assigned
        get_programme=request.user.course_assigned
        get_department=request.user.department
        
        student_course=request.user.course_assigned
        settings=Settings.objects.all()
        for obj in settings:
            current_term=obj.term
            current_year=obj.session_year
        fees_particular=FeesParticulars.objects.filter(course=student_course , year=current_year  , term=current_term )
        amount_payable=0
        for x in fees_particular:
            amount_payable=amount_payable + x.amount
        my_fee=FeePayment.objects.filter(registration_number=request.user.registration_number)

        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="FEES STRUCTURE"

        # Rendered
        html_string = render_to_string('finance/pdfstudentfeestructure.html', {'u':u,'get_date':get_date,'first_name':first_name,'last_name':last_name,'class_a':class_a,'get_programme':get_programme,'get_department':get_department,'school_name':school_name,'my_fee':my_fee,'current_term':current_term,'current_year':current_year,'fees_particular':fees_particular,'amount_payable':amount_payable})
        html = HTML(string=html_string ,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; fees structure.pdf'
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
def viewfee(request):
    if request.user.is_superuser:
        fees_payment_data = FeePayment.objects.all().order_by('-date_paid')
        form=FeePaymentfilter(request.GET,queryset=fees_payment_data)
        fees_payment_data=form.qs
        paginator=Paginator(fees_payment_data,100)
        page=request.GET.get('page')
        fees_payment_data=paginator.get_page(page)
        return render(request,'finance/viewfee.html',{'fees_payment_data':fees_payment_data,'form':form})
    else:
        return redirect('dashboard')



  
@login_required(login_url='loginuser')
def studentfeestatement(request):
    if request.user.is_student:
        get_date=datetime.now()
        first_name=request.user.first_name
        last_name=request.user.last_name
        u=request.user
        class_a=request.user.class_assigned
        get_programme=request.user.course_assigned
        get_department=request.user.department
        
        student_course=request.user.course_assigned
        settings=Settings.objects.all()
        for obj in settings:
            current_term=obj.term
            current_year=obj.session_year
        fees_particular=FeesParticulars.objects.filter(course=student_course , year=current_year  , term=current_term )
        amount_payable=0
        for x in fees_particular:
            amount_payable=amount_payable + x.amount
        my_fee=FeePayment.objects.filter(registration_number=request.user.registration_number)

        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="FEES STRUCTURE"

        # Rendered
        html_string = render_to_string('finance/studentfeestructure.html', {'u':u,'get_date':get_date,'first_name':first_name,'last_name':last_name,'class_a':class_a,'get_programme':get_programme,'get_department':get_department,'school_name':school_name,'my_fee':my_fee,'current_term':current_term,'current_year':current_year,'fees_particular':fees_particular,'amount_payable':amount_payable})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; fees structure.pdf'
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
def paymentformview(request):
    if request.user.is_superuser:
        form=FeePaymentForm()
        return render(request,'finance/paymentformview.html',{'form':form})
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def updatepayment(request,pk):
    if request.user.is_superuser:
        i=FeePayment.objects.get(id=pk)
        form=FeePaymentForm(instance=i)
        if request.method=="POST":
             form=FeePaymentForm(request.POST,instance=i)
             if form.is_valid():
                form.save()
                messages.info(request,'Transaction Updated')
                user=request.user
                action='Change Fees '
                date=datetime.now()
                item=f"user {user} Changed Fees for Student Registration Number {i.registration_number} Fees Status Was Like This Previous Arrears : KES{i.prev_arrears} , Amount Paid : KES{i.amount_paid} , Current Arrears : KES{i.current_arrears} "
                page=request.META.get('HTTP_REFERER')
                reg_no=i.registration_number
                description= f'This Event Happend On {date} performed by user Registration Number {user} , ref no # {i.reference_number_or_mpesa_code}'
                obj=AuditTrailFinance.objects.create(
                    user=user,
                    action=action,
                    page=page,
                    description=description,
                    date=date,
                    item=item,
                    )
                obj.save()
                return redirect('viewfee')
        return render(request,'finance/paymentformview.html',{'form':form})
    else:
        return redirect('dashboard')

@login_required(login_url='loginuser')
def PrintPaymentReceipt(request,pk):
    if request.user.is_superuser:
        data=FeePayment.objects.get(id=pk)
        student_reg=data.registration_number
        print(student_reg)
        obj=User.objects.filter(registration_number=student_reg)
        for x in obj:
            first_name=x.first_name
            last_name=x.last_name
            programme=x.course_assigned
            class_name=x.class_assigned
            programme=x.course_assigned
        get_date=datetime.now()
    
        settings=Settings.objects.all()
        for obj in settings:
            current_term=obj.term
            current_year=obj.session_year
      
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="FEES STRUCTURE"

        # Rendered
        html_string = render_to_string('finance/PdfFeeReceipt.html', {'student_reg':student_reg,'first_name':first_name,'last_name':last_name,'programme':programme,'class_name':class_name,'get_date':get_date,'school_name':school_name,'current_term':current_term,'current_year':current_year,'data':data,'obj':obj})
        html = HTML(string=html_string ,base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; Receipt.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response
