from django.contrib import admin

# Register your models here.
from dataclasses import field
from django.contrib import admin
from.models import *

from django.contrib.auth.models import User
#get form overriding for exculding fields for non_superuser edit



class Educentermodeladmin(admin.TabularInline):
    model=Educenter
    fields=["useradmin","name","address",]
    
    


class Customuseradmin(admin.ModelAdmin):
    fields=['username','password',]
    inlines=[Educentermodeladmin]


admin.site.register(Useradmin,Customuseradmin)

   
@admin.register(Teacher)
class Imammodeladmin(admin.ModelAdmin):
   fields= ["name","phone","is_imam",'is_teacher','courses',"salary","address","cnic","qualification","educenter"]
   
@admin.register(Teachdoner)
class Teachdoneradminadmin(admin.ModelAdmin):
   fields=['name','educen','paid','amount','paiddate','paidmonth','paidyear','date','month','year']
   
   
@admin.register(Student)
class Studentmodeladmin(admin.ModelAdmin):
    fields=["name","f_name","educenter","admission_date","birthdate","courses","grade"]
@admin.register(StuDoners)
class StuDonersAdmin(admin.ModelAdmin):
    fields=['name','educen','paid','amount','paiddate','paidmonth','paidyear','date','month','year']

@admin.register(Muqtadi)
class Muqmodeladmin(admin.ModelAdmin):
   fields= ["name","phone","fee","address","cnic","educenter"]

    

@admin.register(Courses)
class Coursesmodeladmin(admin.ModelAdmin):
    fields=["name","educenter"]


@admin.register(Revenue)
class Coursesmodeladmin(admin.ModelAdmin):
    fields = ["balance", "educenter"]

@admin.register(Monthrevenue)
class Coursesmodeladmin(admin.ModelAdmin):
    fields = ["balance", "educenter","month","year"]

@admin.register(Sidefund)
class Sidefundadmin(admin.ModelAdmin):
    fields = ["doner","name","foreigner","title", "educenter", "description", 'amount', 'date', 'month', 'year']

@admin.register(Expenses)
class Expenseadmin(admin.ModelAdmin):
    fields = ["title", "educenter", "description", 'amount', 'date', 'month', 'year']

#employ muqtadi doner
@admin.register(Doners)
class Donermodeladmin(admin.ModelAdmin):
    fields = ['name', 'educen', 'paid', 'amount', 'paiddate', 'paidmonth', 'paidyear', 'date', 'month', 'year']



    