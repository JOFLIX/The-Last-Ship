from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from fees.models import Payment
from accounts.models import Settings
from .models import Expenses, Revenue,Taxrate,Liabilities,Assets
# FOR WEASY PRINT pdf zote
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
import tempfile
from django.http import HttpResponse
from fees.models import Payment 
# Create your views here.
@login_required(login_url='loginuser')
def view_income_statement_report(request):
    if request.user.is_superuser:
        year_searched=request.POST.get('year')
        if year_searched:
            year_searched=int(year_searched)
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
                current_year=x.session_year
        else:
            current_year=0000
        print(current_year,'wooowwwwwwwwwwwwwwwwwwwwwwwwwwww')

        fee_object=Payment.objects.filter(year=current_year)
        print(fee_object,'zzzzzzzzzzzzzzz')
        amount_paid=0
        for x in fee_object:
                amount_paid=amount_paid + x.amount_paid 
                print(amount_paid,'xxxxxxxxxxxxxxx')
        print(amount_paid,'paid per yr')
        print(type(year_searched))
        print(type(amount_paid))
    
        revenue_object=Revenue.objects.filter(year=year_searched)
        revenue_amount=0
        for x in revenue_object:
            revenue_amount=revenue_amount + x.revenue_amount 

        expenses_object=Expenses.objects.filter(year=year_searched)
        tota_expenses=0
        for x in expenses_object:
            tota_expenses= tota_expenses + x.expenses_amount
        net_revenue=amount_paid+revenue_amount


        tax_rate=Taxrate.objects.filter(year=year_searched)
        if tax_rate:
            for x in tax_rate:
                tax_rate=x.tax_rate

                tax =  tax_rate * net_revenue
        else:
            tax=0
            tax_rate=0

        net_profit= net_revenue - (tota_expenses + tax )
        
        assets_object=Assets.objects.filter(year=year_searched)
        asset_amount=0
        for x in assets_object:
            asset_amount=asset_amount + x.asset_amount 
        
        liabilties_object=Liabilities.objects.filter(year=year_searched)
        Liabilities_amount=0
        for x in liabilties_object:
            Liabilities_amount= Liabilities_amount + x.Liabilities_amount 
        trading_balance=asset_amount - Liabilities_amount
    else:
        return redirect('dashboard')
    return render (request,'incomestatement/view_income_statement_report.html',{'amount_paid':amount_paid,'revenue_amount':revenue_amount,'net_revenue':net_revenue,'tota_expenses':tota_expenses,'tax':tax,'tax_rate':tax_rate,'net_profit':net_profit,'asset_amount':asset_amount,'Liabilities_amount':Liabilities_amount,'trading_balance':trading_balance,'year_searched':year_searched,'current_year':current_year})




 
@login_required(login_url='loginuser')
def pdf_full__finantial_report(request):
    if request.user.is_superuser:
        fee_object=FeePayment.objects.all()
        amount_paid=0
        for x in fee_object:
            amount_paid=amount_paid + x.amount_paid 
    
        revenue_object=Revenue.objects.all()
        revenue_amount=0
        for x in revenue_object:
            revenue_amount=revenue_amount + x.revenue_amount 
        expenses_object=Expenses.objects.all()
        tota_expenses=0
        for x in expenses_object:
            tota_expenses= tota_expenses + x.expenses_amount
        net_revenue=amount_paid+revenue_amount

        tax_rate=Taxrate.objects.all()
        for x in tax_rate:
            tax_rate=x.tax_rate
        tax =  tax_rate * net_revenue

        net_profit= net_revenue - (tota_expenses + tax )
        
        assets_object=Assets.objects.all()
        asset_amount=0
        for x in assets_object:
            asset_amount=asset_amount + x.asset_amount 
        
        liabilties_object=Liabilities.objects.all()
        Liabilities_amount=0
        for x in liabilties_object:
            Liabilities_amount= Liabilities_amount + x.Liabilities_amount 
        trading_balance=asset_amount - Liabilities_amount
  
        get_date=datetime.now()
        sss=Settings.objects.all()
        if sss:
            for x in sss:
                school_name=x.School_name
             
                
        else:
            school_name="ALL STUDENTS"
        # Rendered
        html_string = render_to_string('incomestatement/pdf_finantial_report.html', {'get_date':get_date,'school_name':school_name,'amount_paid':amount_paid,'revenue_amount':revenue_amount,'tota_expenses':tota_expenses,'net_revenue':net_revenue,'net_profit':net_profit,'asset_amount':asset_amount,'Liabilities_amount':Liabilities_amount,'trading_balance':trading_balance})
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
