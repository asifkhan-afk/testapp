from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from datetime import date

currentdate = date.today()
#authrntications
class Usercreationformadm(UserCreationForm):
    # username=forms.CharField(validators=[validate_user])
    class Meta:
        model=Useradmin
        fields=['username','password1',]

class EduCenterformadm(forms.ModelForm):
    class Meta:
        model=Educenter
        exclude=['is_deleted','delete']




        
UsereduForm=inlineformset_factory(
    Useradmin,
    Educenter,
    EduCenterformadm,
    extra=1
    
)
    

class Empform(forms.ModelForm):
 class Meta:
    model=Muqtadi
    fields=["name","phone","fee","address","cnic","educenter"]
MONTH_CHOICES=(
    (1,"january"),
(2,"feb"),
(3,"March"),
(4,"April"),

)
class donershow(forms.Form):
    month=forms.ChoiceField(choices=MONTH_CHOICES)
    year=forms.DateTimeField(initial=currentdate.year)

    

        
    
class Imamform(forms.ModelForm):
    is_imam=forms.BooleanField(initial=True)

    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for myField in self.fields:
    #         self.fields[myField].widget.attrs['class'] = 'form-control'
         
    class Meta:
            model=Teacher
            fields= ["name","phone","salary",'is_teacher','courses',"is_imam","educenter","address","cnic","qualification"]
            exclude=['is_deleted']
   
        
            

class Teacherform(forms.ModelForm): 
    is_teacher=forms.BooleanField(initial=True)
    class Meta:
            model=Teacher
            fields= ["name","phone",'is_imam',"is_teacher","salary",'courses',"address","cnic","qualification","educenter"]
            exclude=['is_deleted']

   
            
class Stuform(forms.ModelForm):
    class Meta:
        model=Student
        fields=["name","f_name","father_cnic","address","birthdate",'fee',"educenter","admission_date",'adm_month','adm_year',"courses","grade"]
        
        
class Courseform(forms.ModelForm):    
    class Meta:
        model=Courses
        fields = ("name","educenter")


class Sidefundform(forms.ModelForm):
    class Meta:
        model=Sidefund
        fields = ["doner","name","foreigner","title","educenter","description",'amount','date','month','year']


class Expenseform(forms.ModelForm):
    class Meta:
        model=Expenses
        fields = ["title", "educenter", "description", 'amount', 'date', 'month', 'year']

        
class DonerForm(forms.ModelForm):
    class Meta:
        model=Doners
        fields="__all__"

    

