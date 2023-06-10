from datetime import datetime
from .models import PayHistory
from .models import Progress
from .models import Loan
from .models import Employee

def update_employee_salaries():
    today = datetime.now()
    # Only update salaries on the first day of the month
    # print("O ", today)
    # if today.day == 20 and today.hour == 14 and today.minute == 11: 
    print("If ", today)
    print(Employee.objects.all())
    for temp in Employee.objects.all():
        employee_id = temp.EmpId
        employee=Progress.objects.filter(EmpId=employee_id).latest('EffectiveDate')
        emp= Employee.objects.filter(EmpId=employee_id).first()
        salary=PayHistory()
        loan = Loan.objects.filter(EmpId=employee_id).latest('AvailDate')
        
        if loan.AmountPaid!=loan.TotalLoanAmount:
            salary.LoanDeduction=loan.TotalLoanAmount/loan.Tenor
            loan.AmountPaid+=salary.LoanDeduction
            if loan.AmountPaid==loan.TotalLoanAmount:
                emp.Loan_taken=False
            loan.save()    
        if emp.Max_no_of_leaves<0:
            salary.LossOfPay=(employee.BasicPay/30) * abs(emp.Max_no_leaves)
            emp.Max_no_of_leaves=2
            emp.save()
        salary.FinalSalary = employee.BasicPay + employee.Allowance + employee.Conveyance + employee.HRA - salary.LossOfPay - salary.LoanDeduction -employee.IncomeTax-employee.PFTax
        salary.save()
        employee.salary=salary.FinalSalary
        employee.save()
        
