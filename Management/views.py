from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.urls import reverse
from .models import Employee,Loan,Leave,Progress,PayHistory
from .models import Progress, Leave
from django.template import loader
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from Management.models import Employee
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django import forms
from datetime import datetime
from django.utils.safestring import mark_safe
import openpyxl
from django.core import serializers
from decimal import Decimal
import json
from datetime import datetime

#Adding Favorite List
favorites = []

#Adding Complaint List
complaint_author = []
complaint_email = []
complaint_type = []
complaint_subject = []
complaint_message = []

class NewFavForm(forms.Form):
    new_favorite = forms.CharField(label="New Favorite", required="True")

class NewComplaintForm(forms.Form):
    name = forms.CharField(label="Your name:", max_length=100, required="True")
    sender = forms.EmailField(label="Your Email:", required="True")
    c_type = forms.CharField(label="Complaint Type:", required="True")
    subject = forms.CharField(label="Subject:", min_length=10, required="True")
    message = forms.CharField(label="Message:", max_length=300, required="True")

class NewSearchForm(forms.Form):
    query = forms.CharField(label="Employee ID:", max_length=100, required="True")

class NewSignupForm(forms.Form):
    Name = forms.CharField(label="Your Name:",max_length=64)
    Email = forms.EmailField(label="Your Email:",max_length=64)
    Password = forms.CharField(label="Password",max_length=64)
    Position = forms.CharField(label="Your Position",max_length=64)
    Salary = forms.IntegerField(label="Your Salary:")


#PROGRESS TABLE 
class Progresstable(forms.Form):
    EmpId = forms.CharField(label="Employee ID",max_length=12)
    EffectiveDate =  forms.DateField(label="Effective Date")
    Grade = forms.CharField(label="Grade",max_length=64)
    PFTax = forms.FloatField(label="PF Tax ")
    IncomeTax = forms.FloatField(label="Income Tax")
    BasicPay = forms.FloatField(label="Basic Pay")
    HRA = forms.FloatField(label="HR allowance")
    Conveyance = forms.FloatField(label="Conveyance")
    Allowance = forms.FloatField(label="Allowance")

class AddEmployee(forms.Form):
    EmpId = forms.IntegerField(label=mark_safe("<br />Employee_ID"))
    EmpName = forms.CharField(label=mark_safe("<br />Employee Name"),max_length=30)
    Role= forms.CharField(label=mark_safe("<br />Role"),max_length=20)
    Department= forms.CharField(label=mark_safe("<br />Department"),max_length=20)
    Username= forms.CharField(label=mark_safe("<br />Username"),max_length=30)
    Password= forms.CharField(label=mark_safe("<br />Password"),max_length=30)
    Manager_ID= forms.IntegerField(label=mark_safe("<br />Manager ID"))
    Phone_No= forms.CharField(label=mark_safe("<br />Phone number"),max_length=10)
    Email_ID= forms.CharField(label=mark_safe("<br />Email ID"),max_length=30)
    IFSC_code= forms.CharField(label=mark_safe("<br />IFSC Code"),max_length=15)
    Door_No= forms.IntegerField(label=mark_safe("<br />Door number"))
    Street= forms.CharField(label=mark_safe("<br />Street"),max_length=20)
    City= forms.CharField(label=mark_safe("<br />City"),max_length=20)
    State= forms.CharField(label=mark_safe("<br />State"),max_length=20)
    Country= forms.CharField(label=mark_safe("<br />Country"),max_length=20)
    Pin_code= forms.IntegerField(label=mark_safe("<br />Pincode"))
    DOB =  forms.DateField(label=mark_safe("<br />Date of birth "))
    DOJ =  forms.DateField(label=mark_safe("<br />Date of joining"))
    PAN_No=forms.CharField(label=mark_safe("<br />Pancard Number"),max_length=10)
    Acc_No=forms.IntegerField(label=mark_safe("<br />Account number"))
    Loan_taken=forms.BooleanField(label=mark_safe("<br />Loan taken<br />"), required=False)
    Max_no_of_leaves=forms.IntegerField(label=mark_safe("<br />Max no of leaves "))

class ModifyEmployee(forms.Form):
    EmpId = forms.IntegerField(label="Employee_ID")
    EmpName = forms.CharField(label="Employee_Name",max_length=64)
    Role= forms.CharField(label="Role",max_length=20)
    Department= forms.CharField(label="Department",max_length=20)
    Username= forms.CharField(label="Username",max_length=30)
    Password= forms.CharField(label="Password",max_length=30)
    Manager_ID= forms.IntegerField(label="Manager_ID")
    Phone_No= forms.CharField(label="Phone_number",max_length=10)
    Email_ID= forms.CharField(label="Email_ID",max_length=30)
    IFSC_code= forms.CharField(label="IFSC_code",max_length=15)
    Door_No= forms.IntegerField(label="Door_number")
    Street= forms.CharField(label="Street",max_length=20)
    City= forms.CharField(label="City",max_length=20)
    State= forms.CharField(label="State",max_length=20)
    Country= forms.CharField(label="Country",max_length=20)
    Pin_code= forms.IntegerField(label="Pin_code")
    DOB =  forms.DateField(label="Date_of_birth")
    DOJ =  forms.DateField(label="Date_of_joining")
    PAN_No=forms.CharField(label="Pancard_number",max_length=10)
    Acc_No=forms.IntegerField(label="Account_number",)
    Loan_taken=forms.BooleanField(label="Loan_taken")
    Max_no_of_leaves=forms.IntegerField(label="Maximum_number_of_leaves")


# class AddEmployee(forms.Form):
#     EmpId = forms.IntegerField(label="Employee_ID")
#     EmpName = forms.CharField(label="Employee_Name",max_length=64)
    # Role= forms.CharField(label="Role",max_length=20)
    # Department= forms.CharField(label="Department",max_length=20)
    # Username= forms.CharField(label="Username",max_length=30)
    # Password= forms.CharField(label="Password",max_length=30)
    # Manager_ID= forms.IntegerField(label="Manager_ID")
    # Phone_No= forms.CharField(label="Phone_number",max_length=10)
    # Email_ID= forms.CharField(label="Email_ID",max_length=30)
    # IFSC_code= forms.CharField(label="IFSC_code",max_length=15)
    # Door_No= forms.IntegerField(label="Door_number")
    # Street= forms.CharField(label="Street",max_length=20)
    # City= forms.CharField(label="City",max_length=20)
    # State= forms.CharField(label="State",max_length=20)
    # Country= forms.CharField(label="Country",max_length=20)
    # Pin_code= forms.IntegerField(label="Pin_code")
    # DOB =  forms.DateField(label="Date_of_birth")
    # DOJ =  forms.DateField(label="Date_of_joining")
    # PAN_No=forms.CharField(label="Pancard_number",max_length=10)
    # Acc_No=forms.IntegerField(label="Account_number",)
    # Loan_taken=forms.BooleanField(label="Loan_taken")
    # Max_no_of_leaves=forms.IntegerField(label="Maximum_number_of_leaves")

# def Add_employee(request):
#     if request.method == "POST":
#         form = AddEmployee(request.POST)
#         if form.is_valid():
#             empID = form.cleaned_data['EmpId']
#             empName = form.cleaned_data['EmpName']
#             # role= form.cleaned_data['Role']
#             # department= form.cleaned_data['Department']
#             # username= form.cleaned_data['Username']
#             # password= form.cleaned_data['Password']
#             # manager_ID= form.cleaned_data['Manager_ID']
#             # phone_No= form.cleaned_data['Phone_No']
#             # email_ID= form.cleaned_data['Email_ID']
#             # iFSC_code= form.cleaned_data['IFSC_code']
#             # door_No= form.cleaned_data['Door_No']
#             # street= form.cleaned_data['Street']
#             # city= form.cleaned_data['City']
#             # state= form.cleaned_data['State']
#             # country= form.cleaned_data['Country']
#             # pin_code= form.cleaned_data['Pin_code']
#             # dOB =  form.cleaned_data['DOB']
#             # dOJ =  form.cleaned_data['DOJ']
#             # pAN_No=form.cleaned_data['PAN_No']
#             # acc_No=form.cleaned_data['Acc_No']
#             # loan_taken=form.cleaned_data['Loan_taken']
#             # max_no_of_leaves=form.cleaned_data['Max_no_of_leaves']
#             # add_employee = Employee(EmpId=empID,EmpName= empName, Role= role, Department= department, Username= username, Password=password, Manager_ID=manager_ID, Phone_No=phone_No, Email_ID=email_ID, IFSC_code=iFSC_code, Door_No=door_No, Street=street, City=city, State=state, Country=country, Pin_code=pin_code, DOB=dOB, DOJ=dOJ, PAN_No=pAN_No, Acc_No=acc_No, Loan_taken=loan_taken, Max_no_of_leaves=max_no_of_leaves )
#             add_employee = Employee(EmpId = empID,EmpName = empName)
#             add_employee.save()
#             return HttpResponseRedirect(reverse("Management:Add_employee"))
#         else:
#             return render(request, "Management/Add_employee.html", {
#                 "form": form,
#             })
    
#     return render(request, "Management/Add_employee.html", {
#         "form": AddEmployee(),
#     })

#------------------------------------------------------------------------------------------------

class Applyleave(forms.Form):
    EmpId = forms.IntegerField(label="Employee ID")
    LeaveFrom=forms.DateField(label = "Leave From  Date")
    LeaveTo=forms.DateField(label="Leave To Date")

class Applyloan(forms.Form):
    EmpId = forms.IntegerField(label="Employee ID")
    AvailDate=forms.DateField(label= "Date")
    TotalLoanAmount = forms.FloatField(label = "Loan amount ")
    Tenor = forms.IntegerField(label = "Tenor")    

class Getpayslip(forms.Form):
    EmpId = forms.IntegerField(label="Employee ID")
    month = forms.IntegerField(label="Month")
    year =  forms.IntegerField(label="Year")

# Create your views here.
def indexEMP(request):
    return render(request, "Management/indexEMP.html", {
        "favorites": favorites
    })

def index(request):
    return render(request, "Management/index.html", {
        "favorites": favorites
    })

def view_fav(request):
    return render(request, "Management/favourite.html", {
        "favorites": favorites
    })

def add_fav(request):
    if request.method == "POST":
        form = NewFavForm(request.POST)
        if form.is_valid():
            new_favorite = form.cleaned_data["new_favorite"]
            favorites.append(new_favorite)
            return HttpResponseRedirect(reverse("Management:Add_Favourite"))
        else:
            return render(request, "Management/add_favourite.html", {
                "form": form,
                "favorites": favorites
            })
    
    return render(request, "Management/add_favourite.html", {
        "form": NewFavForm(),
        "favorites": favorites
    })

def add_complaint(request):
    if request.method == "POST":
        form = NewComplaintForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            sender=form.cleaned_data["sender"]
            c_type=form.cleaned_data["c_type"]
            subject=form.cleaned_data["subject"]
            message=form.cleaned_data["message"]
            complaint_author.append(name)
            complaint_email.append(sender)
            complaint_type.append(c_type)
            complaint_subject.append(subject)
            complaint_message.append(message)
            return HttpResponseRedirect(reverse("Management:Add_Complaint"))
        else:
            return render(request, "Management/add_complaint.html", {
                "form": form,
                "favorites": favorites
            })
    
    return render(request, "Management/add_complaint.html", {
        "form": NewComplaintForm(),
        "favorites": favorites
    })

def view_complaint(request):
    return render(request, "Management/complaint.html", {
        "Complaint": zip(complaint_author, complaint_email, complaint_type, complaint_subject, complaint_message),
        "favorites": favorites
    })

def searchemp(request):
    result = "NONE"
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            result = Employee.objects.filter(EmpId=query)
            return render(request, "Management/searchEMP.html", {
                "form": form,
                "result": result,
                "method": request.method,
                "favorites": favorites
            })
        else:
            return render(request, "Management/searchEMP.html", {
                "result": result,
                "form": form,
                "method": request.method,
                "favorites": favorites
            })
    
    return render(request, "Management/searchEMP.html", {
        "result": result,
        "form": NewSearchForm(),
        "method": request.method,
        "favorites": favorites
    })

def sign_up(request):
    if request.method == "POST":
        form = NewSignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["Name"]
            email = form.cleaned_data["Email"]
            password = form.cleaned_data["Password"]
            position = form.cleaned_data["Position"]
            salary = form.cleaned_data["Salary"]
            new_employee = Employee(Name= name, Email= email, Password= password, Position= position, Salary= salary)
            new_employee.save()
            return HttpResponseRedirect(reverse("Management:Sign_Up"))
        else:
            return render(request, "Management/signup.html", {
                "form": form,
                "favorites": favorites
            })
    
    return render(request, "Management/signup.html", {
        "form": NewSignupForm(),
        "favorites": favorites
    })


def testing(request):
  mydata =  PayHistory.objects.values_list()
  template = loader.get_template('template.html')
  context = {
    'mymembers': mydata,
  }
  return HttpResponse(template.render(context, request))

def Apply_leave(request):
    if request.method == "POST":
        form=Applyleave(request.POST)

        if form.is_valid():
            empId = form.cleaned_data['EmpId']
            leaveFrom =  form.cleaned_data['LeaveFrom']
            leaveTo = form.cleaned_data['LeaveTo']
            employee = Employee.objects.get(EmpId=empId)
            maxLeave = employee.Max_no_of_leaves
            duration= leaveTo - leaveFrom
            days = duration.days
            if employee and leaveFrom and leaveTo and leaveTo > leaveFrom:
                new_leave = Leave(EmpId= empId, LeaveFrom=leaveFrom, LeaveTo=leaveTo)
                new_leave.save()
                messages.info(request,"Leave successfully applied !")
                if days > maxLeave:
                    messages.info(request, 'You have exceeded the no.of paid leaves. Loss of pay will be deducted from the salary')
                employee.Max_no_of_leaves=maxLeave-days
                print(employee.Max_no_of_leaves)
                employee.save()
                return HttpResponseRedirect(reverse("Management:leave"))
            
            else:
                form.add_error(None, 'Invalid leave application')
        else:
            return render(request, "Management/applyleave.html", {
                "form": form                
            })
    
    return render(request, "Management/applyleave.html", {
        "form": Applyleave(),

    })

def Apply_loan(request):
    if request.method == "POST":
        form=Applyloan(request.POST)

        if form.is_valid():
            empId = form.cleaned_data['EmpId']
            availDate =  form.cleaned_data['AvailDate']
            totalLoanAmount = form.cleaned_data['TotalLoanAmount']
            tenor = form.cleaned_data['Tenor']
            print("valid fun")
            employee = Employee.objects.get(EmpId=empId)
            salary = Progress.objects.get(EmpId=empId)

            if employee :
                print("inside if emp")
                if availDate and totalLoanAmount and tenor:
                    print("req field")
                    if employee.Loan_taken==False:
                        print("inside loan taken")
                        if totalLoanAmount <= 5 * salary.BasicPay:
                            print("tot loan amt")
                            if tenor <= 10:
                                print("tenor")
                                new_loan = Loan(EmpId= empId, AvailDate=availDate, TotalLoanAmount=totalLoanAmount,Tenor=tenor,AmountPaid = 0)
                                print(new_loan)
                                new_loan.save()
                                messages.info(request,"Loan successfully applied !")
                                employee.Loan_taken==True
                                employee.save()
                                return HttpResponseRedirect(reverse("Management:loan"))
                            else:
                                form.add_error('Tenor', 'Tenor should be less than 10 months') 
                        else:
                            form.add_error('TotalLoanAmount', 'Loan amount should be less than five times your basic pay') 
                    else:
                        form.add_error(None, 'Loan already taken')                     
                else:
                   form.add_error(None, 'Fill all required fields') 
            
            else:
                form.add_error(None, 'Employee id does not exist')
        else:
            return render(request, "Management/applyloan.html", {
                "form": form                
            })
    
    return render(request, "Management/applyloan.html", {
        "form": Applyloan(),

    })

def view_payslip(request):
    if request.method == "POST":
        form=Getpayslip(request.POST)

        if form.is_valid():
            empId = form.cleaned_data['EmpId']
            month =  form.cleaned_data['month']
            year = form.cleaned_data['year']
            employee = Employee.objects.get(EmpId=empId)
            joinYear = employee.DOJ.year
            print(joinYear)
            print(year)
            if month>0 and month<=12 and year<=2023 and year>=joinYear:
                if year == 2023:
                    if month<=datetime.now().month:    
                        print("third if ", employee)
                        pay_history = PayHistory.objects.filter(EmpId = empId,created_at__year = year,created_at__month = str(month))
                        # Convert QuerySet to list of dictionaries
                        pay_history_data = serializers.serialize('python', pay_history)
                        pay_history_list = [item['fields'] for item in pay_history_data]

                        # Convert Decimal to float
                        for item in pay_history_list:
                            for key, value in item.items():
                                if isinstance(value, Decimal):
                                    item[key] = float(value)
                                if isinstance(value, datetime):
                                    item[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                        pay_history_dict=pay_history_list[0]
                        
                        #pay_history_obj = PayHistory(**pay_history_dict)
                        request.session['pay_history'] = pay_history_dict
                        
                        if pay_history_dict:
                            print(pay_history_dict)
                            #pay_history_list = [pay_history_list.values()]
                            return render(request, 'Management/displaypayslip.html', {"payhistory": pay_history_dict})
                        else:
                            form.add_error(None,'No payhistory found for specified month.') 
                    else:
                        form.add_error(None,'Invalid month value')    

                       
                else:
                    print("year not 2023 ", employee)
                    pay_history = PayHistory.objects.filter(EmpId = empId,created_at__year = year,created_at__month = str(month))
                        # Convert QuerySet to list of dictionaries
                    pay_history_data = serializers.serialize('python', pay_history)
                    pay_history_list = [item['fields'] for item in pay_history_data]

                    # Convert Decimal to float
                    for item in pay_history_list:
                        for key, value in item.items():
                            if isinstance(value, Decimal):
                                item[key] = float(value)
                            if isinstance(value, datetime):
                                item[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                    pay_history_dict=pay_history_list[0]
                    
                    #pay_history_obj = PayHistory(**pay_history_dict)
                    request.session['pay_history'] = pay_history_dict
                    
                    if pay_history_dict:
                        print(pay_history_dict)
                        #pay_history_list = [pay_history_list.values()]
                        return render(request, 'Management/displaypayslip.html', {"payhistory": pay_history_dict})
                    else:
                        form.add_error(None,'No payhistory found for specified month.') 
            else:
                form.add_error(None, 'Invalid values')
        else:
            form.add_error(None, 'Invalid values')
            return render(request, "Management/getpayslip.html", {
                "form": form                
            })
   
    #messages.info(request,"Invalid values")
    return render(request, "Management/getpayslip.html", {
        "form": Getpayslip(),

    })



def download_payslip(request):
    pay_history=request.session['pay_history']  
    print(pay_history['EmpId'])
    #request.session['pay_history'] = pay_history_list
    # Create a new workbook
    wb = openpyxl.Workbook()
    # Select the active worksheet
    ws = wb.active
    # Set the values for the first row
    ws.append(['Employee Id', 'PFTax', 'IncomeTax','BasicPay','HRA','Conveyance','Allowance','LossOfPay','LoanDeduction','FinalSalary'])
    # Add the object data to the worksheet    
    ws.append([pay_history['EmpId'], pay_history['PFTax'],pay_history['IncomeTax'],pay_history['BasicPay'],pay_history['HRA'],pay_history['Conveyance'],pay_history['Allowance'],pay_history['LossOfPay'],pay_history['LoanDeduction'],pay_history['FinalSalary']])
    # Create a response object with the Excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=pay_history.xlsx'
    wb.save(response)
    return response

#Progress table 
def Progress_table(request):
    if request.method == "POST":
        form = Progresstable(request.POST)
        if form.is_valid():
            empId = form.cleaned_data['EmpId']
            effectiveDate =  form.cleaned_data['EffectiveDate']
            grade = form.cleaned_data['Grade']
            pfTax = form.cleaned_data['PFTax']
            incomeTax = form.cleaned_data["IncomeTax"]
            basicPay = form.cleaned_data["BasicPay"]
            hRA = form.cleaned_data["HRA"]
            conveyance = form.cleaned_data["Conveyance"]
            allowance = form.cleaned_data["Allowance"]
            new_progress = Progress(EmpId= empId, EffectiveDate= effectiveDate, Grade= grade, Salary= basicPay + allowance + conveyance + hRA - incomeTax - pfTax, PFTax= pfTax, IncomeTax=incomeTax, BasicPay=basicPay, HRA=hRA, Conveyance=conveyance, Allowance=allowance)
            new_progress.save()
            return HttpResponseRedirect(reverse("Management:Progress_table"))
        else:
            return render(request, "Management/progresstable.html", {
                "form": form,
                "favorites": favorites
            })
    
    return render(request, "Management/progresstable.html", {
        "form": Progresstable(),

    })

def Add_employee(request):
    if request.method == "POST":
        form = AddEmployee(request.POST)
        if form.is_valid():
            empId = form.cleaned_data['EmpId']
            empName =  form.cleaned_data['EmpName']
            role= form.cleaned_data['Role']
            department= form.cleaned_data['Department']
            username= form.cleaned_data['Username']
            password= form.cleaned_data['Password']
            manager_ID= form.cleaned_data['Manager_ID']
            phone_No= form.cleaned_data['Phone_No']
            email_ID= form.cleaned_data['Email_ID']
            iFSC_code= form.cleaned_data['IFSC_code']
            door_No= form.cleaned_data['Door_No']
            street= form.cleaned_data['Street']
            city= form.cleaned_data['City']
            state= form.cleaned_data['State']
            country= form.cleaned_data['Country']
            pin_code= form.cleaned_data['Pin_code']
            dOB =  form.cleaned_data['DOB']
            dOJ =  form.cleaned_data['DOJ']
            pAN_No=form.cleaned_data['PAN_No']
            acc_No=form.cleaned_data['Acc_No']
            loan_taken=form.cleaned_data['Loan_taken']
            max_no_of_leaves=form.cleaned_data['Max_no_of_leaves']

            add_employee = Employee(EmpId= empId, EmpName=empName, Role=role, Department=department,Username=username,Password=password,Manager_ID=manager_ID,Phone_No=phone_No,Email_ID=email_ID,
                                    IFSC_code=iFSC_code,Door_No=door_No,Street=street,City=city,State=state,Country=country,Pin_code=pin_code,DOB=dOB,DOJ=dOJ,PAN_No=pAN_No,
                                    Acc_No=acc_No,Loan_taken=loan_taken,Max_no_of_leaves=max_no_of_leaves)
            add_employee.save()
            return HttpResponseRedirect(reverse("Management:Add_employee"))
        else:
            return render(request, "Management/addemployee.html", {
                "form": form,
                "favorites": favorites
            })
    
    return render(request, "Management/addemployee.html", {
        "form": AddEmployee(),

    })

def Modify_employee(request):
    if request.method == "POST":
        form = ModifyEmployee(request.POST)
        if form.is_valid():
            EmpId = form.cleaned_data['EmpId']
            EmpName = form.cleaned_data['EmpName']
            Role= form.cleaned_data['Role']
            Department= form.cleaned_data['Department']
            Username= form.cleaned_data['Username']
            Password= form.cleaned_data['Password']
            Manager_ID= form.cleaned_data['Manager_ID']
            Phone_No= form.cleaned_data['Phone_No']
            Email_ID= form.cleaned_data['Email_ID']
            IFSC_code= form.cleaned_data['IFSC_code']
            Door_No= form.cleaned_data['Door_No']
            Street= form.cleaned_data['Street']
            City= form.cleaned_data['City']
            State= form.cleaned_data['State']
            Country= form.cleaned_data['Country']
            Pin_code= form.cleaned_data['Pin_code']
            DOB =  form.cleaned_data['DOB']
            DOJ =  form.cleaned_data['DOJ']
            PAN_No=form.cleaned_data['PAN_No']
            Acc_No=form.cleaned_data['Acc_No']
            Loan_taken=form.cleaned_data['Loan_taken']
            Max_no_of_leaves=form.cleaned_data['Max_no_of_leaves']
            modify_employee = Employee.objects.get(EmpId= EmpId) 
            #modify_employee=modify_employee( EmpName= EmpName, Role= Role, Department= Department, Username= Username, Password=Password, Manager_ID=Manager_ID, Phone_No=Phone_No, Email_ID=Email_ID, IFSC_code=IFSC_code, Door_No=Door_No, Street=Street, City=City, State=State, Country=Country, Pin_code=Pin_code, DOB=DOB, DOJ=DOJ, PAN_No=PAN_No, Acc_No=Acc_No, Loan_taken=Loan_taken, Max_no_of_leaves=Max_no_of_leaves )
            modify_employee.EmpName=EmpName
            modify_employee.Role=Role
            modify_employee.Department=Department
            modify_employee.Password=Password
            modify_employee.Manager_ID=Manager_ID
            modify_employee.Phone_No=Phone_No
            modify_employee.Email_ID=Email_ID
            modify_employee.IFSC_code=IFSC_code
            modify_employee.Door_No=Door_No
            modify_employee.Street=Street
            modify_employee.Country=Country
            modify_employee.Pin_code=Pin_code
            modify_employee.DOB=DOB
            modify_employee.DOJ=DOJ
            modify_employee.PAN_No=PAN_No
            modify_employee.Acc_No=Acc_No
            modify_employee.Loan_taken=Loan_taken
            modify_employee.Max_no_of_leaves=Max_no_of_leaves

            modify_employee.save()
            return HttpResponseRedirect(reverse("Management:Modify_employee"))
        else:
            return render(request, "Management/modifyemployee.html", {
                "form": form,
            })
    
    return render(request, "Management/modifyemployee.html", {
        "form": ModifyEmployee(),
    })


def searchhr(request):
    result = "NONE"
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            result = Progress.objects.filter(EmpId=query)
            #result2 = Progress.objects.filter(EmpId=query) 
            return render(request, "Management/searchhr.html", {
                "form": form,
                "result": result,
                "method": request.method,
                "favorites": favorites
            })
        else:
            return render(request, "Management/searchhr.html", {
                "result": result,
                "form": form,
                "method": request.method,
                "favorites": favorites
            })
    
    return render(request, "Management/searchhr.html", {
        "result": result,
        "form": NewSearchForm(),
        "method": request.method,
        "favorites": favorites
    })


# def view_payslip_HR(request):
#     if request.method == "POST":
#         form=GetpayslipHR(request.POST)

#         if form.is_valid():
#             month =  form.cleaned_data['month']
#             year = form.cleaned_data['year']

#             #curr_month =
#             if month>0 and month<=12 and year<=2023:
#                 #print(month,year)
#             #validation needed
#                 #print(.strftime('%Y'))
#                 pay_history = PayHistory.objects.filter(created_at__year = year,created_at__month = str(month))
#                 # Convert QuerySet to list of dictionaries
#                 pay_history_data = serializers.serialize('python', pay_history)
#                 pay_history_list = [item['fields'] for item in pay_history_data]

#                 # Convert Decimal to float
#                 for item in pay_history_list:
#                     for key, value in item.items():
#                         if isinstance(value, Decimal):
#                             item[key] = float(value)
#                         if isinstance(value, datetime):
#                             item[key] = value.strftime("%Y-%m-%d %H:%M:%S")
#                 #pay_history_dict=pay_history_list[0]
                
#                 #pay_history_obj = PayHistory(**pay_history_dict)
#                 request.session['pay_history'] = pay_history_list
                
#                 if pay_history_list:
#                      print(pay_history_list)
#                      #pay_history_list = [pay_history_list.values()]
#                      return render(request, 'Management/displaypayslipHR.html', {"payhistory": pay_history_list})

#                 else:
#                      form.add_error(None,'No payhistory found for specified month.')        
           
#             else:
#                 form.add_error(None, 'Invalid values')
#         else:
#             return render(request, "Management/getpayslipHR.html", {
#                 "form": form                
#             })
   
#     return render(request, "Management/getpayslipHR.html", {
#         "form": Getpayslip(),

#     })



def download_payslip_HR(request):
   
    month =datetime.now().month    
    year = datetime.now().year 
   
   
    pay_history = PayHistory.objects.filter(created_at__year = year,created_at__month = str(month))
    # Convert QuerySet to list of dictionaries
    pay_history_data = serializers.serialize('python', pay_history)
    pay_history_list = [item['fields'] for item in pay_history_data]

    # Convert Decimal to float
    for item in pay_history_list:
        for key, value in item.items():
            if isinstance(value, Decimal):
                item[key] = float(value)
            if isinstance(value, datetime):
                item[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    
    #payhistory=pay_history_list
    
    #request.session['pay_history'] = pay_history_list
    # Create a new workbook
    wb = openpyxl.Workbook()
    # Select the active worksheet
    ws = wb.active
    # Set the values for the first row
    ws.append(['Employee Id', 'PFTax', 'IncomeTax','BasicPay','HRA','Conveyance','Allowance','LossOfPay','LoanDeduction','FinalSalary'])
    # Add the object data to the worksheet   
    for pay_history in pay_history_list:
        ws.append([pay_history['EmpId'], pay_history['PFTax'],pay_history['IncomeTax'],pay_history['BasicPay'],pay_history['HRA'],pay_history['Conveyance'],pay_history['Allowance'],pay_history['LossOfPay'],pay_history['LoanDeduction'],pay_history['FinalSalary']])
    # Create a response object with the Excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=pay_history_hr.xlsx'
    wb.save(response)
    return response













def indexLogin(request):
    return render(request, 'Management/indexLogin.html')

class AddEmployeeRegister(forms.Form):
    EmpId = forms.IntegerField(label="Employee_ID")
    EmpName = forms.CharField(label="Employee_Name",max_length=64)
    # Role= forms.CharField(label="Role",max_length=20)
    Role = forms.CharField(initial='HR', label="Role", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    Department= forms.CharField(label="Department",max_length=20)
    Username= forms.CharField(label="Username",max_length=30)
    Password= forms.CharField(label="Password",max_length=30)
    Manager_ID= forms.IntegerField(label="Manager_ID")
    Phone_No= forms.CharField(label="Phone_number",max_length=10)
    Email_ID= forms.CharField(label="Email_ID",max_length=30)
    IFSC_code= forms.CharField(label="IFSC_code",max_length=15)
    Door_No= forms.IntegerField(label="Door_number")
    Street= forms.CharField(label="Street",max_length=20)
    City= forms.CharField(label="City",max_length=20)
    State= forms.CharField(label="State",max_length=20)
    Country= forms.CharField(label="Country",max_length=20)
    Pin_code= forms.IntegerField(label="Pin_code")
    DOB =  forms.DateField(label="Date_of_birth")
    DOJ =  forms.DateField(label="Date_of_joining")
    PAN_No=forms.CharField(label="Pancard_number",max_length=10)
    Acc_No=forms.IntegerField(label="Account_number",)
    Loan_taken=forms.BooleanField(label="Loan_taken", required=False)
    Max_no_of_leaves=forms.IntegerField(label="Maximum_number_of_leaves")

def register(request):
    if request.method == "POST":
        form = AddEmployeeRegister(request.POST)
        if form.is_valid():
            empId = form.cleaned_data['EmpId']
            empName =  form.cleaned_data['EmpName']
            role= form.cleaned_data['Role']
            department= form.cleaned_data['Department']
            username= form.cleaned_data['Username']
            password= form.cleaned_data['Password']
            manager_ID= form.cleaned_data['Manager_ID']
            phone_No= form.cleaned_data['Phone_No']
            email_ID= form.cleaned_data['Email_ID']
            iFSC_code= form.cleaned_data['IFSC_code']
            door_No= form.cleaned_data['Door_No']
            street= form.cleaned_data['Street']
            city= form.cleaned_data['City']
            state= form.cleaned_data['State']
            country= form.cleaned_data['Country']
            pin_code= form.cleaned_data['Pin_code']
            dOB =  form.cleaned_data['DOB']
            dOJ =  form.cleaned_data['DOJ']
            pAN_No=form.cleaned_data['PAN_No']
            acc_No=form.cleaned_data['Acc_No']
            loan_taken=form.cleaned_data['Loan_taken']
            max_no_of_leaves=form.cleaned_data['Max_no_of_leaves']

            add_employee = Employee(EmpId= empId, EmpName=empName, Role=role, Department=department,Username=username,Password=password,Manager_ID=manager_ID,Phone_No=phone_No,Email_ID=email_ID,
                                    IFSC_code=iFSC_code,Door_No=door_No,Street=street,City=city,State=state,Country=country,Pin_code=pin_code,DOB=dOB,DOJ=dOJ,PAN_No=pAN_No,
                                    Acc_No=acc_No,Loan_taken=loan_taken,Max_no_of_leaves=max_no_of_leaves)
            add_employee.save()
            return HttpResponseRedirect(reverse("Management:login_view"))
        else:
            return render(request, "Management/register.html", {
                "form": form,
            })
    
    return render(request, "Management/register.html", {
        "form": AddEmployeeRegister(),

    })

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            print('valid')
            Username = request.POST['Username']
            Password = request.POST['Password']
            try:
                employee = Employee.objects.get(Username=Username)
                print("employee: ", employee)
                # if check_password(Password, employee.Password):
                if employee.Password == Password:
                    print('checked password')
                    Role = employee.Role.lower()
                    print("role: ", Role)
                    if Role == 'hr':
                        return render(request, 'Management/index.html', {'employee': employee})
                    elif Role == 'employee':
                        return render(request, 'Management/indexEMP.html', {'employee': employee})
            except Employee.DoesNotExist:
                msg= 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'Management/login.html', {'form': form, 'msg': msg})

# def update_employee_salaries(request):
#     today = datetime.now()
#     # Only update salaries on the first day of the month
#     # print("O ", today)
#     # if today.day == 20 and today.hour == 14 and today.minute == 11: 
#     print("If ", today)
#     if request.method == 'POST':
#         print(Employee.objects.all())
#         for temp in Employee.objects.all():
#             employee_id = temp.EmpId
#             employee=Progress.objects.filter(EmpId=employee_id).latest('EffectiveDate')
#             emp= Employee.objects.filter(EmpId=employee_id).first()
#             salary=PayHistory()
#             loan = Loan.objects.filter(EmpId=employee_id).latest('AvailDate')
#             emp.EmpName="Mathu"
            
#             if loan.AmountPaid!=loan.TotalLoanAmount:
#                 salary.LoanDeduction=loan.TotalLoanAmount/loan.Tenor
#                 loan.AmountPaid+=salary.LoanDeduction
#                 if loan.AmountPaid==loan.TotalLoanAmount:
#                     emp.Loan_taken=False
#                 loan.save()

#             if emp.Max_no_of_leaves<0:
#                 salary.LossOfPay=(employee.BasicPay/30) * abs(emp.Max_no_leaves)
#                 emp.Max_no_of_leaves=2
#                 emp.save()

#             salary.FinalSalary = employee.BasicPay + employee.Allowance + employee.Conveyance + employee.HRA - salary.LossOfPay - salary.LoanDeduction -employee.IncomeTax-employee.PFTax
#             salary.save()
#             employee.Salary=salary.FinalSalary
#             employee.save()
#             return HttpResponseRedirect(reverse("Management:index"))
              

##

# def admin(request):
#     return render(request,'admin.html')

def update_employee_salaries(request):
        print(Employee.objects.all())
        for temp in Employee.objects.all():
            if temp.Role =='Employee':
                employee_id = temp.EmpId
                employee=Progress.objects.filter(EmpId=employee_id).latest('EffectiveDate')
                emp= Employee.objects.filter(EmpId=employee_id).first()
                salary=PayHistory()
                loan = Loan.objects.filter(EmpId=employee_id)
                
                if loan:
                    loan=loan.latest('AvailDate')
                    if loan.AmountPaid!=loan.TotalLoanAmount:
                        salary.LoanDeduction=loan.TotalLoanAmount/loan.Tenor
                        loan.AmountPaid+=salary.LoanDeduction
                        if loan.AmountPaid==loan.TotalLoanAmount:
                            emp.Loan_taken=False
                        loan.save()
                    else:
                        salary.LoanDeduction=0
                else:
                    salary.LoanDeduction=0


                if emp.Max_no_of_leaves<0:
                    salary.LossOfPay=(employee.BasicPay/30) * abs(emp.Max_no_of_leaves)
                    emp.Max_no_of_leaves=5
                    emp.save()
                else:
                    salary.LossOfPay=0    
                salary.FinalSalary = employee.BasicPay + employee.Allowance + employee.Conveyance + employee.HRA - salary.LossOfPay - salary.LoanDeduction -employee.IncomeTax-employee.PFTax
                salary.BasicPay=employee.BasicPay
                salary.Allowance=employee.Allowance
                salary.Conveyance=employee.Conveyance
                salary.HRA = employee.HRA 
                salary.PFTax=employee.PFTax
                salary.IncomeTax=employee.IncomeTax
                salary.EmpId=employee.EmpId
                salary.save()
                employee.Salary=salary.FinalSalary
                employee.save()            
    
        return render(request, 'Management/index.html')


def hr(request):
    employee = request.GET.get('employee')
    print(employee)
    return render(request, 'Management/index.html', {'employee': employee})


def employee(request):
    return render(request,'Management/indexEMP.html')


