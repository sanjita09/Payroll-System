from django.db import models
from django.utils import timezone


# Create your models here.
class Employee(models.Model):
    EmpId = models.IntegerField(primary_key=True)
    EmpName = models.CharField(max_length=64)
    Role= models.CharField(max_length=20)
    Department= models.CharField(max_length=20)
    Username= models.CharField(max_length=30)
    Password= models.CharField(max_length=30)
    Manager_ID= models.IntegerField()
    Phone_No= models.CharField(max_length=10)
    Email_ID= models.CharField(max_length=30)
    IFSC_code= models.CharField(max_length=15)
    Door_No= models.IntegerField()
    Street= models.CharField(max_length=20)
    City= models.CharField(max_length=20)
    State= models.CharField(max_length=20)
    Country= models.CharField(max_length=20)
    Pin_code= models.IntegerField()
    DOB =  models.DateField()
    DOJ =  models.DateField()
    PAN_No= models.CharField(max_length=10)
    Acc_No=models.IntegerField()
    Loan_taken=models.BooleanField()
    Max_no_of_leaves=models.IntegerField()

    def __str__(self):
        return f"{self.EmpId}: {self.EmpName}"

class Progress(models.Model):
    EmpId = models.CharField(max_length=12)
    EffectiveDate =  models.DateField()
    Grade = models.CharField(max_length=64)
    Salary = models.FloatField()
    PFTax = models.FloatField()
    IncomeTax = models.FloatField()
    BasicPay = models.FloatField()
    HRA = models.FloatField()
    Conveyance = models.FloatField()
    Allowance = models.FloatField()

    def __str__(self):
        return f"{self.EmpId}:  with salary of {self.Salary}. in Grade:{self.Grade}  from:{self.EffectiveDate}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['EmpId', 'EffectiveDate'], name='unique_progress')
        ]

    
class Leave(models.Model):
    EmpId = models.CharField(max_length=12)
    LeaveFrom =  models.DateField()
    LeaveTo =  models.DateField()
    
    def __str__(self):
        return f"{self.EmpId}:  has taken leave from {self.LeaveFrom} to {self.LeaveTo}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['EmpId', 'LeaveFrom'], name='unique_leave')
        ]

    
class Loan(models.Model):
    EmpId = models.CharField(max_length=12)
    AvailDate = models.DateField(primary_key=True)
    TotalLoanAmount = models.FloatField(null=False)
    Tenor = models.IntegerField(null=False)
    AmountPaid = models.FloatField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['EmpId', 'AvailDate'], name='unique_loan')
        ]


class PayHistory(models.Model):
    EmpId = models.CharField(max_length=12)
    #month_year = models.DateField()
    PFTax = models.FloatField()
    IncomeTax = models.FloatField()
    BasicPay = models.FloatField()
    HRA = models.FloatField()
    Conveyance = models.FloatField()
    Allowance = models.FloatField()
    LossOfPay = models.FloatField()
    LoanDeduction = models.FloatField()
    FinalSalary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('EmpId', 'created_at')

   

    # def save(self, *args, **kwargs):
    #     #if not self.id:
    #     #    self.month_year = self.created_at.replace(day=1)
    #     super().save(*args, **kwargs)
