
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from requests import request
import random
from .models import *
import datetime
from .forms import DonerForm
 
 #getting today's date
today=datetime.date.today()


#d2 = today.strftime("%B")  --> current month full name
#Muqtadi doner 
d2 = today.strftime("%B")



@receiver(post_save,sender=Educenter)
def create_revenue(sender,instance,created,**kwargs):
    if created:
        revenue=Revenue()
        educen=Educenter.objects.get(pk=instance.pk)
        print("Educen  is created",instance.name)
        revenue.balance=0
        revenue.educenter=educen
        revenue.save()
        #Monthly revenue
        mrevenue=Monthrevenue()
        meducen = Educenter.objects.get(pk=instance.pk)
        mrevenue.balance = 0
        mrevenue.month = today.month
        mrevenue.year = today.year
        mrevenue.educenter = meducen
        print("monthly revenue is created from signals")
        mrevenue.save()
        print("monthly revenue is saved from signals")




@receiver(post_save, sender=Muqtadi)
def create_doner(sender, instance, created, **kwargs):
    if created:
        doners=Doners()
        mname=Muqtadi.objects.get(id=instance.id)
        meducen = Educenter.objects.get(id=instance.educenter.id)
        doners.name=mname
        doners.educen_id=str(meducen.id)
        print("**********",meducen)
        doners.name_id=str(mname.id)
        doners.month=today.month
        doners.year=today.year
        doners.paid=False
        print("Muqtadi doenr is created")
        doners.save()
        print("Muqtadi doner is dsaved")
        

    
@receiver(post_save, sender=Student)
def create_stdoner(sender, instance, created, **kwargs):
    if created:
        doners=StuDoners()
        dname=Student.objects.get(id=instance.id)
        doners.name=dname
        doners.educen= Educenter.objects.get(id=instance.educenter.id)
        doners.name_id=str(dname.id)
        doners.month=today.month
        doners.year=today.year
        doners.paid=False
        print("student doenr is created")
        doners.save()
        print("student doner is saved")


@receiver(post_save, sender=Teacher)
def create_teachdoner(sender, instance, created, **kwargs):
    if created:
        doners = Teachdoner()
        dname = Teacher.objects.get(id=instance.id)
        doners.name = dname
        doners.educen = Educenter.objects.get(id=instance.educenter.id)
        doners.name_id = str(dname.id)
        doners.month = today.month
        doners.year = today.year
        doners.paid = False
        print("Teacher doenr is created")
        doners.save()
        print("Teaacaher doner is saved")

