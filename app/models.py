from distutils.archive_util import make_zipfile
from django.contrib.auth.models import User,AbstractUser,BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from logging import PlaceHolder
from os import error
from pyexpat import model
from django.urls import reverse
from django.utils.dates import MONTHS
from .validators import *
from django.db import models
import datetime
import calendar
from django.utils import timezone
from .cusmanager import Softdeletemanager
from numpy import datetime64

#getting today date
today = datetime.date.today()



    

# abstract Model of custom manager
class Cusmanager(models.Model):
    is_deleted=models.BooleanField(default=False)   
    objects=Softdeletemanager()
    allobjects=models.Manager()
    
    
    def sdelete(self):
        raise error()
    
    def restore(self):
        self.is_deleted=False
        self.save()

    def alldelete(self):
        self.delete()

    def delete(self):
        self.is_deleted=True
        print("this is delted from the given list of the edu centers")
        self.save()
    
    class Meta:
        abstract=True

from django.contrib.auth.validators import ASCIIUsernameValidator

class MyValidator(ASCIIUsernameValidator):
    regex = r'^[\w.@+-\s]+$'

  #USer
class Useradmin(User):
    def get_absolute_url(self):
            return reverse("userdetail", kwargs={"pk": self.pk})




        
# Create your models here.
#Masjid
class Educenter(Cusmanager):
    useradmin = models.OneToOneField(Useradmin, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    
    address=models.CharField(max_length=60)
    def showdeltedcen(self):
        a=Educenter.allobjects.all().order_by('name')
        return a
   
    
    
    def __str__(self):
        return self.name
    

        
                
        
            
    #who will receve salry    
class SalReciver(Cusmanager):
    name=models.ForeignKey("Teacher",on_delete=models.CASCADE)
    month=models.IntegerField(default=today.month)
    year=models.IntegerField(default=today.year)
    
    def __str__(self):
         return str(self.name)
    #paid salary
class SalPaid(Cusmanager):
    salreciever=models.OneToOneField(SalReciver,on_delete=models.CASCADE)
    amount=models.IntegerField(default=0)
    paid=models.BooleanField(default=False)
    def __str__(self):
         return f'{str(self.salreciever.name)} {self.salreciever.month},{self.paid}'
  

class Muqtadi(Cusmanager):
        name=models.CharField(max_length=30)
        address=models.CharField(max_length=60,blank=True, null=True)
        cnic=models.CharField(blank=True, null=True,max_length=15,validators=[validate_cnic])
        phone=models.IntegerField(validators=[validate_phone],help_text="Enter phone number without zero")
        fee=models.IntegerField(validators=[validate_money])
        educenter=models.ForeignKey("Educenter",on_delete=models.CASCADE)
        admission_date=models.IntegerField(default=today.day,validators=[validate_date])
        adm_month=models.IntegerField(default=today.month)
        adm_year=models.IntegerField(default=today.year,validators=[validate_year])
        def __str__(self):
            return f'{ str(self.name)}'
        
        #doners  , employ,student 
class Doners(Cusmanager):
        educen = models.ForeignKey('Educenter', on_delete=models.CASCADE)
        name = models.ForeignKey("Muqtadi", on_delete=models.CASCADE)
        amount = models.PositiveIntegerField(default=0)
        paid = models.BooleanField(default=False)
        paiddate = models.PositiveIntegerField(null=True, blank=True, validators=[validate_date])
        paidmonth = models.PositiveIntegerField(null=True, blank=True, validators=[validate_date])
        paidyear = models.PositiveIntegerField(null=True, blank=True, validators=[validate_year])
        date = models.DateTimeField(null=True, blank=True)
        month = models.PositiveIntegerField(default=today.month, validators=[validate_date])
        year = models.PositiveIntegerField(default=today.year, validators=[validate_year])

        def __str__(self):
            return self.name.name

        class Meta:
            unique_together = ['name', "month", "year"]

    # def get_absolute_url(self):
    #     return reverse("muqdonerlist", kwargs={"month": self.doner.month,"year":self.doner.year})
    #
       



# YEAR_CHOICES = [(r,r) for r in range(20, datetime.date.today().year+1)]
# MONTH_CHOICES = [(r,r) for r in range(1984, datetime.date.today().month+1)]
Gradechoices=(("basic"))
class Teacher(Cusmanager):
        name=models.CharField(max_length=30)
        address=models.CharField(max_length=60,blank=True, null=True)
        is_imam=models.BooleanField(default=False)
        is_teacher=models.BooleanField(default=False)
        cnic=models.PositiveIntegerField(blank=True, null=True,validators=[validate_cnic])
        salary=models.PositiveIntegerField(validators=[validate_money])
        phone=models.IntegerField(validators=[validate_phone],help_text="Enter phone number without zero")
        courses=models.ManyToManyField('Courses' ,blank=True)
        educenter=models.ForeignKey("Educenter",on_delete=models.CASCADE)
        qualification=models.CharField(max_length=50,null=True,blank=True)
        admission_date= models.IntegerField(default=today.day, validators=[validate_date])
        adm_month= models.IntegerField(default=today.month,validators=[validate_date])
        adm_year= models.IntegerField(default=today.year, validators=[validate_year])
        def __str__(self):
            return f'{self.name}'


class Teachdoner(Cusmanager):
    educen=models.ForeignKey('Educenter',on_delete=models.CASCADE)
    name=models.ForeignKey("Teacher",on_delete=models.CASCADE)
    amount=models.PositiveIntegerField(default=0)
    paid=models.BooleanField(default=False)
    paiddate=models.PositiveIntegerField(null=True,blank=True,validators=[validate_date])
    paidmonth=models.PositiveIntegerField(null=True,blank=True,validators=[validate_date])
    paidyear=models.PositiveIntegerField(null=True,blank=True,validators=[validate_year])
    date=models.DateTimeField(null=True,blank=True)
    month=models.PositiveIntegerField(default=today.month,validators=[validate_date])
    year=models.PositiveIntegerField(default=today.year,validators=[validate_year])
    def __str__(self):
        return self.name.name
    class Meta:
        unique_together = ['name',"month", "year"]





class Student(Cusmanager):
        name=models.CharField(max_length=30)
        f_name=models.CharField(max_length=30)
        fee=models.IntegerField()
        father_cnic=models.CharField(blank=True, max_length=15,null=True,validators=[validate_cnic])
        # phone = models.IntegerField(validators=[validate_phone], help_text="Enter phone number without zero")
        address = models.CharField(max_length=50)
        educenter=models.ForeignKey(Educenter,on_delete=models.CASCADE)
        birthdate=models.DateField(help_text="add your birth date")
        admission_date=models.PositiveIntegerField(default=today.day, validators=[validate_date])
        courses=models.ManyToManyField("Courses")        
        grade=models.CharField(blank=True,null=True,max_length=30)
        adm_month = models.PositiveIntegerField(default=today.month, validators=[validate_date])
        adm_year = models.PositiveIntegerField(default=today.year, validators=[validate_year])
        def __str__(self):
            return self.name

 #student doners
class StuDoners(Cusmanager):
    educen=models.ForeignKey('Educenter',on_delete=models.CASCADE)
    name=models.ForeignKey("Student",on_delete=models.CASCADE,related_name="donerstudent")
    amount=models.PositiveIntegerField(default=0)
    paid=models.BooleanField(default=False)
    paiddate=models.PositiveIntegerField(null=True,blank=True,validators=[validate_date])
    paidmonth=models.PositiveIntegerField(null=True,blank=True,validators=[validate_date])
    paidyear=models.PositiveIntegerField(null=True,blank=True,validators=[validate_year])
    date=models.DateTimeField(null=True,blank=True)
    month=models.PositiveIntegerField(default=today.month,validators=[validate_date])
    year=models.PositiveIntegerField(default=today.year,validators=[validate_year])
    
    def __str__(self):
         return str(self.name)
    class Meta:
        unique_together = ['name',"month", "year"]


class Sidefund(Cusmanager):
    educenter=models.ForeignKey(Educenter,on_delete=models.CASCADE)
    doner=models.ForeignKey(Muqtadi,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=35,blank=True,null=True)
    foreigner=models.BooleanField(default=False)
    title=models.CharField(max_length=50)
    amount = models.PositiveIntegerField(default=0)
    description=models.TextField(max_length=300,blank=True,null=True)
    date = models.PositiveIntegerField(default=today.day,null=True, blank=True)
    month = models.PositiveIntegerField(default=today.month,null=True, blank=True, validators=[validate_date])
    year = models.PositiveIntegerField(default=today.year,null=True, blank=True,validators=[validate_year])

    def __str__(self):
        return self.title





class Expenses(Cusmanager):
    educenter=models.ForeignKey(Educenter,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    amount = models.PositiveIntegerField(default=0)
    description=models.TextField(max_length=300)
    date = models.PositiveIntegerField(default=today.day,null=True, blank=True)
    month = models.PositiveIntegerField(default=today.month, validators=[validate_date])
    year = models.PositiveIntegerField(default=today.year, validators=[validate_year])
    def __str__(self):
        return self.title


#Revenue
class Revenue(Cusmanager):
    balance=models.IntegerField(default=0)
    educenter=models.OneToOneField("Educenter",on_delete=models.SET_NULL,default=None,null=True,blank=True,related_name="reveducen")
    def __str__(self):
        return self.educenter.name

class Monthrevenue(Cusmanager):
    balance = models.IntegerField(default=0)
    educenter = models.ForeignKey("Educenter", on_delete=models.SET_NULL, default=None, null=True, blank=True)
    month = models.PositiveIntegerField(default=today.month, validators=[validate_date])
    year = models.PositiveIntegerField(default=today.year, validators=[validate_year])
    def __str__(self):
        return self.educenter.name
    class Meta:
        unique_together=["educenter","month","year"]







class Courses(Cusmanager):
        name = models.CharField(max_length=30)
        educenter = models.ForeignKey("Educenter", on_delete=models.CASCADE)

        def __str__(self):
            return self.name

        






    

class Fundtype(Cusmanager):
    name=models.CharField(max_length=50)

    

# class RevenueGoal(Cusmanager):
#     month = models.PositiveSmallIntegerField(choices=MONTHS.items())
#     year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
#     goal = models.DecimalField('Revenue Goal', max_digits=8, decimal_places=2)
#     class Meta:
#         db_table = ''
#         managed = True
#         unique_together=["month","year"]