from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from .models import FeesParticular,Payment,AuditTrailFinance
from . filters import Paymentfilter
# Create your views here.
from accounts.models import Settings
from django.core.paginator import Paginator 
from datetime import datetime
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.http import HttpResponse


@login_required(login_url='loginuser')
def add_fee(request):
    if request.user.is_superuser:
        reg_number=request.POST.get('reg_no')
        student_c_term=0
        us=User.objects.filter(is_student=True,registration_number=reg_number)
        if not us and not reg_number == None:
            messages.info(request,'Registration number not found Kindly Confirm and Key in Again ')
        if us and not reg_number==None:
            for x in us:
                student_c_term=x.student_term 
                course=x.course_assigned
        else:
            pass
        print(student_c_term,'the term is this ')
        #...............................

        #...............................
        query_current_arrears=0
        aa_payable_this_term=0
        if reg_number and us :
            pp=FeesParticular.objects.filter(course_name=course)
            for x in pp:
                aa_payable_this_term=x.amount_payable
            fees_obj=Payment.objects.filter(registration_number=reg_number)
            print(fees_obj,'stratng .................')
            i=0
            for x in fees_obj:
                i = x.id
                if x.id > i:
                    i = x.id
            print(i,'ndex')
            latest_payment=Payment.objects.filter(id=i)
            if latest_payment:
                for x in latest_payment:
                    if x.term == student_c_term:
                        query_current_arrears=x.current_arrears
                    else:
                        query_current_arrears=x.current_arrears + aa_payable_this_term
            else:
                query_current_arrears=aa_payable_this_term

        else:
            query_current_arrears=0
      
        #................................
        if not reg_number and not reg_number == None:
            messages.info(request,'Regisreation number not found')
        else:
            info=User.objects.filter(is_student=True,registration_number=reg_number)
            print(info)
        s=Settings.objects.all()
        year=2021
        for x in s:
            year=x.session_year
        print(year,'ddddddddddddddddddddddddddddddddddddd')
        reg=request.POST.get('registration_no')
        pm=request.POST.get('pm')
        code=request.POST.get('code')
        amount_paid=request.POST.get('amount')
        print(reg,'reg')
        print(pm,'payment method')
        print(code ,'code ')
        print(amount_paid,'paid amount ')
       # get_p=Payment.objects.filter(registration_number=reg)

        student_exist=User.objects.filter(registration_number=reg,is_student=False)
        if not student_exist :
            student_data=User.objects.filter(registration_number=reg)
            current_arrears=0
            for x in student_data:
                student_course=x.course_assigned
                print('course ', student_course)
                student_term=x.student_term 
                print(student_term,'term for the student ')
                first_name=x.first_name
                last_name=x.last_name
                name= str(first_name)  + '  ' +  str(last_name)
                print(name)
                amount_payable_this_term=0
                fees_particular_for_student_term=FeesParticular.objects.filter(course_name=student_course,term=student_term)
                for x in fees_particular_for_student_term:
                    amount_payable_this_term=x.amount_payable
                    print('amount payable is ',amount_payable_this_term)
                payment_history=Payment.objects.filter(registration_number=reg)
                print('amount paid as per now',amount_paid)
                    
                #checking if any payment ever made 
                if payment_history:
                    fees_obj=Payment.objects.filter(registration_number=reg)
                    i=0
                    for x in fees_obj:
                        i = x.id
                        if x.id > i:
                            i = x.id
                    latest_payment=Payment.objects.filter(id=i)
                    print('latest payment found ')
                    for x in latest_payment:
                        term=x.term
                        if term == student_term: 
                            previous_arrears=x.current_arrears 
                            current_arrear=previous_arrears - float(amount_paid)
                        else:
                            previous_arrears=x.current_arrears + amount_payable_this_term
                            current_arrear=previous_arrears - float(amount_paid)
                        pay=Payment.objects.create(
                                registration_number=reg,
                                term=student_term,
                                previous_arrears=previous_arrears,
                                amount_paid=amount_paid,
                                payment_method=pm,
                                reference_code=code,
                                current_arrears=current_arrear,
                                course_name=student_course,
                                student_name=name,
                                year=year,

                    )
                    
                    user=request.user
                    action='Fee Payment '
                    date=datetime.now()
                    item=f'Paid KES {amount_paid} For Student Reg no {reg}'
                    page=request.META.get('HTTP_REFERER')
                    description= ("User {} Added Fee for   {} On Page {} ".format(request.user.registration_number,reg,request.META.get('HTTP_REFERER')))
                    obj=AuditTrailFinance.objects.create(
                        user=user,
                        action=action,
                        page=page,
                        description=description,
                        date=date,
                        item=item,
                        )
                    obj.save()
                    return redirect('view_fee')

                else:
                    prev_arrear=amount_payable_this_term
                    print('Previos Arreas',prev_arrear)
                    current_arrear=prev_arrear - float(amount_paid)
                    print('current arreas ', current_arrear)
                    # saving first traansaction
                    pay=Payment.objects.create(
                        registration_number=reg,
                        term=student_term,
                        previous_arrears=prev_arrear,
                        amount_paid=amount_paid,
                        payment_method=pm,
                        reference_code=code,
                        current_arrears=current_arrear,
                        course_name=student_course,
                        student_name=name,
                        year=year,


                    )
                    user=request.user
                    action='Fee Payment '
                    date=datetime.now()
                    item=f'Paid KES {amount_paid} For Student Reg no {reg}'
                    page=request.META.get('HTTP_REFERER')
                    description= ("User {} Added Fee for   {} On Page {} ".format(request.user.registration_number,reg,request.META.get('HTTP_REFERER')))
                    obj=AuditTrailFinance.objects.create(
                        user=user,
                        action=action,
                        page=page,
                        description=description,
                        date=date,
                        item=item,
                        )
                    obj.save()
                    return redirect('view_fee')
                
        else:

            messages.info(request,'REGISTRATION NUMBER DOES NOT EXIS')
    else:
        return redirect('dashboard')
    return render(request,'fees/add_fee.html',{'info':info,'reg':reg,'reg_number':reg_number,'query_current_arrears':query_current_arrears,'query_current_arrears':query_current_arrears,'us':us})




@login_required(login_url='loginuser')
def view_fee(request):
    if request.user.is_superuser:
        fees_payment_data=Payment.objects.all().order_by('-date_added')
        form=Paymentfilter(request.GET,queryset=fees_payment_data)
        fees_payment_data=form.qs
        paginator=Paginator(fees_payment_data,100)
        page=request.GET.get('page')
        fees_payment_data=paginator.get_page(page)
    else:
        return redirect('dashboard')
    return render(request,'fees/view_fee.html',{'fees_payment_data':fees_payment_data,'form':form})

@login_required(login_url='loginuser')
def view_my_fee(request):
    if request.user.is_student or  request.user.is_parent:
        if request.user.is_parent:
              reg=request.user.student_number
              s=User.objects.filter(registration_number=reg)
              for x in s:
                  student_term=x.student_term
                  course=x.course_assigned
              this_term_fee=FeesParticular.objects.filter(term=student_term,course_name=course)
              for x in this_term_fee:
                    amount=x.amount_payable
              print(this_term_fee)
              my_fee=Payment.objects.filter(registration_number=reg,course_name=course)
              print(my_fee,'dddddddddbbbbbbbb')
              return render(request,'fees/view_my_fee.html',{'amount':amount,'my_fee':my_fee})
        else:
            this_term_fee=FeesParticular.objects.filter(term=request.user.student_term,course_name=request.user.course_assigned)
        print(this_term_fee)
        amount=0
        for x in this_term_fee:
            amount=x.amount_payable
            print(amount)
        my_fee=Payment.objects.filter(registration_number=request.user.registration_number)
    return render(request,'fees/view_my_fee.html',{'amount':amount,'my_fee':my_fee})



 



@login_required(login_url='loginuser')
def pdfstudentfeesstatement(request):
    if request.user.is_student:
        reg=request.user.registration_number
        s=User.objects.filter(registration_number=reg)
        date=datetime.now()
        for x in s:
            student_term=x.student_term
            course=x.course_assigned
            first_name=x.first_name
            last_name=x.last_name
            class_name=x.class_assigned
            student_term=x.student_term
            student_course=x.course_assigned
            this_term_fee=FeesParticular.objects.filter(term=student_term,course_name=course)
            for x in this_term_fee:
                amount=x.amount_payable
            print(this_term_fee)
            my_fee=Payment.objects.filter(registration_number=reg,course_name=course)
            print(my_fee,'dddddddddbbbbbbbb')
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
        else:
            school_name="Fees statement"
            # Rendered
        html_string = render_to_string('fees/pdfstudentfeesstatement.html', {'date':date,'reg':reg,'my_fee':my_fee,'student_term':student_term,'first_name':first_name,'last_name':last_name,'class_name':class_name,'student_course':student_course,'date':date,'school_name':school_name})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

            # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; receipt.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    
        

    return response



@login_required(login_url='loginuser')
def print_receipt(request,pk):
    if request.user.is_superuser:
        i=Payment.objects.get(id=pk)
        # sss=Settings.objects.all()
        # if sss:
        #     for x in sss:
        #         school_name=x.School_name
        # else:
        #     school_name="Fees Receipt"
        student_reg=i.registration_number
        u=User.objects.filter(registration_number=student_reg)
        for x in u:
            first_name=x.first_name
            last_name=x.last_name
            class_name=x.class_assigned
            course=x.course_assigned
            student_term=x.student_term
            print(student_term,'jjjjjjjjjjjjjjjjjjjjjjjj')
        date=datetime.now()
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
                year=x.session_year
        else:
            school_name="Fees statement"
            
            # Rendered
        html_string = render_to_string('fees/PdfFeeReceipt.html', {'date':date,'school_name':school_name,'student_reg':student_reg,'i':i,'first_name':first_name,'last_name':last_name,'class_name':class_name,'course':course,'student_term':student_term,'year':year})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()

            # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; receipt.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    
        

        return response

