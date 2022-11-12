import imp
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import *
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin, UserPassesTestMixin
from requests import request
from.models import *
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponseRedirect 
from django.contrib.auth.forms import *
from .forms import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import get_user_model
from .utils import *

today = datetime.date.today()

        
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        educen = Educenter.objects.get(id=2)
        print("these are educenters ", educen)

        educen.reveducen.balance +=1
        re=Revenue.objects.get(educenter=educen)
        re.balance+=2
        re.save()
        print(re.balance,re.educenter)


        return render(request,"home.html")
    else:
            return redirect('accounts/login')


class SuperUserRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(
                request,
                'Permission required to perform the '
                'requested operation.')
            return redirect(settings.LOGIN_URL)
        return super(SuperUserRequiredMixin, self).dispatch(request,
            *args, **kwargs)
        

    
def createuser(request):
 if request.user.is_superuser:
    
    if request.method=='POST':
        form=Usercreationformadm(request.POST)
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBB")
        if form.is_valid():
            print("before save")
            obj=form.save()
            pk=str(obj.id)
            print("after save")
            url = reverse('userdetail', kwargs={'pk': pk})
            request.session['id']=obj.id
            return redirect(reverse('adminedu', kwargs={'pk': obj.id}))

        else:
            print("MMMMMMMMMMMMMMMMM")
            form=Usercreationformadm(request.POST)
            return render(request,"user/createuser.html",{'form':form})
    else:
        form=Usercreationformadm()
        return render(request,"user/createuser.html",{'form':form})
 else:
     raise Http404 
#admin User 
# class CreateUser(SuperUserRequiredMixin,CreateView):
#     template_name = 'user/createuser.html'
#     model=Useradmin
#     form_class = Usercreationformadm
#     fields=['username','password','password confirmation']    
#     success_url = "/"
    	
class Userdetail(SuperUserRequiredMixin,DetailView):
    model=Useradmin
    context_object_name="adminuser"
    template_name="user/userdetail.html"


def updateuser(request,id):
    if request.user.is_superuser:
        if request.method=='POST':
            print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
            use=User.objects.get(pk=id)
            form=Usercreationformadm(request.POST,instance=use)
            if form.is_valid():
                form.save()
                return redirect('adminuserlist')
            else:
                return render(request, "user/createuser.html", {"form": form})
        else:
            print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
            use=User.objects.get(pk=id)
            form=Usercreationformadm(instance=use)
            return render(request,"user/createuser.html",{"form":form})
    else:
        raise Http404 
        
            

# class updateuser(LoginRequiredMixin,UpdateView):
#     form_class = UserChangeForm
#     model = User
#     success_url = "/"
#     template_name = 'user/updateuser.html'
    


    
    
class Adminuserlist(LoginRequiredMixin,ListView):
    model=Useradmin 
    template_name='user/userlist.html'
    
    context_object_name="educenlist"
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Useradmin.objects.all()
        else:
            return HttpResponse("Permitted only for super user")



#conform del 
def conformdel(request):
    
    return render(request,"conformdel.html")
#######################################################3
class Admineducenter(LoginRequiredMixin,SingleObjectMixin,FormView):
    model= Useradmin
    template_name='admineducent.html'
    fields=['name','address']

    def get(self, request, *args, **kwargs) :
        self.object=self.get_object(queryset=Useradmin.objects.all())
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs) :
        self.object=self.get_object(queryset=Useradmin.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return UsereduForm(**self.get_form_kwargs(),instance=self.object)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request,messages.SUCCESS,"Changes were saveddd")
        return HttpResponseRedirect(self.get_success_url())
    def get_success_url(self):
        return reverse("adminuserlist")


###Masjid IMAM
@login_required
def imameducenter(request,pk):
    educenter = Educenter.objects.all().filter(pk=pk)
    n = educenter[0]
    if request.method == 'POST':
        form = Imamform(request.POST)
        if form.is_valid():
            print('____________________enp saved', form.cleaned_data['educenter'])
            form.save()
            return redirect('emplist')
        else:
            form = Imamform(request.POST, initial={'educenter': n})
        return render(request, "imam/createimam.html", {'form': form})
    else:

        form = Imamform(initial={'educenter': n, 'name': n})
        return render(request, "Imam/createimam.html", {'form': form})


    
    
    
    
    
    
# Edu center 
class EducenterCV(SuperUserRequiredMixin,CreateView):
    template_name="educenter/create_educenter.html"
    model=Educenter
    
    context_object_name="createeducenter"
    fields=['useradmin','address']
    
    success_url='/educenlist'
    # def get_initial(self):
    #     ad=self.request.session.get('id')
    #     useradmin=Useradmin.objects.get(id=ad)
    #     print(useradmin)
    #     return {'useradmin':useradmin,'name':'kolal',}

    
    
class Educenlist(SuperUserRequiredMixin,ListView):
    template_name="educenter/educenlist.html"
    model=Educenter
    
    context_object_name="educenlist"
    fields=['useradmin','name','address']
    def get_queryset(self):
        qs =Educenter.objects.all().order_by('name')
        return qs



class Educenupdate(SuperUserRequiredMixin,UpdateView):
    kwargs=id
    template_name="educenter/educenupdate.html"
    model=Educenter
    context_object_name="educen"
    fields=['name','address']
    success_url="/"
    
class Educendelete(SuperUserRequiredMixin,DeleteView):
    kwargs=id
    template_name="conformdel.html"
    model=Educenter
    
    fields='__all__'
    success_url="/"

class Educendetail(SuperUserRequiredMixin,DetailView):
    kwargs=id
    template_name="educenter/educendetail.html"
    model=Educenter
    context_object_name="educen"
    fields=['name','address']
    

#************************************************#
#Employ/Muqtadi
@login_required
def empCV(request,pk ):

        educenter=Educenter.objects.all().filter(pk=pk)
        n=educenter[0]
        if request.method=='POST':
            form=Empform(request.POST)
            if form.is_valid():
                print('____________________enp saved',form.cleaned_data['educenter'])
                form.save()
                return redirect('emplist')
            else:
                form=Empform(request.POST,initial={'educenter':n})
            return render(request,"employ/createemp.html",{'form':form})
        else:
           
            form=Empform(initial={'educenter':n,'name':n})
            return render(request,"employ/createemp.html",{'form':form})
 
   


    
class Emplist(LoginRequiredMixin,ListView):
    template_name="employ/emplist.html"
    model=Muqtadi
    context_object_name="emplist"
    fields=['name','address']

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs=Muqtadi.objects.all().order_by('educenter')
            return qs
        else:
            try:
                edu=self.request.user.useradmin
                educenter=Educenter.objects.get(useradmin=edu)
                return Muqtadi.objects.all().filter(educenter=educenter).order_by('educenter')
            except:
                 pass

        

class Admempcv(LoginRequiredMixin,CreateView):
    model = Muqtadi
    template_name = "employ/createemp.html"
    fields =  fields=["name","phone","fee","address","cnic","educenter"]
    success_url = '/employlist'

    
class Empupdate(LoginRequiredMixin,UpdateView):
    kwargs=id
    template_name="employ/empupdate.html"
    model=Muqtadi
    context_object_name="educen"
    fields='__all__'
    success_url="/employlist"

class Empdetail(LoginRequiredMixin,DetailView):
    kwargs=id
    template_name="employ/empdetail.html"
    model=Muqtadi
    context_object_name="educen"
    
    
class Empdelete(LoginRequiredMixin,DeleteView):
    template_name="conformdel.html"
    model=Muqtadi
    context_object_name="educen"
    fields='__all__'
    success_url="/employlist"
    
    #MUQ Doner
class Muqdonerlist(LoginRequiredMixin,ListView):
    model=Doners
    context_object_name="muqdonlist"
    template_name="employ/doner/muqdonerlist.html"
    fields=['name','month','year']
    def get_queryset(self):
        month = self.kwargs['month']
        year = self.kwargs['year']
        create_muqdoner()
        create_monthlyrev()
        try:
            calculate_mrevenue(month, year)
        except:
            pass
        create_revenue()


        if self.request.user.is_superuser:
            muql=Doners.objects.all().order_by('name').filter(month=month ,year=year)
            return muql
        else:
            try:
                educenter = self.request.user.useradmin.educenter.id
                doners=Doners.objects.all().filter(educen=educenter)
                muql = doners.filter(month=month, year=year)
                return muql
            except:
                pass

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        month = self.kwargs['month']
        year = self.kwargs['year']
        if self.request.user.is_superuser:
            currentmonth_muq = Doners.objects.all().order_by('name').filter(month=month, year=year)
            print("this is super user if true")
            paidamount = 0
            for i in currentmonth_muq:
                paidamount += i.amount
            unpaidamount = 0
            for i in currentmonth_muq:
                unpaidamount += i.name.fee
            context['unpaidamount'] = unpaidamount
            context['paidamount'] = paidamount
            return context

        if not self.request.user.is_superuser:
            try:
                educenter = self.request.user.useradmin.educenter.id
                doners = Doners.objects.all().filter(educen=educenter)
                currentmonth_muq=doners.filter(month=month, year=year)
                print("this is not  muqdoner super user true codition ")
                paidamount = 0
                for i in currentmonth_muq:
                    paidamount += i.amount
                unpaidamount = 0
                for i in currentmonth_muq:
                    unpaidamount += i.name.fee
                context['unpaidamount'] = unpaidamount
                context['paidamount'] = paidamount
                return context
            except:
                pass



#

class Showrevenue(LoginRequiredMixin,ListView):
    model=Monthrevenue
    template_name = "showrevenue.html"
    context_object_name = 'mr'
    def get_context_data(self,**kwargs):
        month=self.kwargs['month']
        year=self.kwargs['year']
        context=super().get_context_data(**kwargs)
        try:
            calculate_mrevenue(month, year)
        except:
            pass
        if self.request.user.is_superuser:
            mr=Monthrevenue.objects.filter(month=month,year=year)
            context['mr']=mr
            return context

        else:
            try:
                educenter = self.request.user.useradmin.educenter
                mr=Monthrevenue.objects.filter(educenter=educenter)
                educen = self.request.user.useradmin.educenter
                totalrev = Revenue.objects.get(educenter=educen)
                context['mr']=mr
                context['totalrev']=totalrev
                return context
            except:
                pass


class Totalrevenue(SuperUserRequiredMixin,ListView):
    template_name = "totalrevenue.html"
    modal=Revenue
    context_object_name = "rev"
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Revenue.objects.all()
        else:
            pass



def showmuqdoner(request):
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",data)
    return HttpResponse("this si srun")
        
    #MUQ Deposit to fund
@login_required
def muqdonerpaid(request,pk,amount):
        if request.method == "POST":
            st = Teachdoner.objects.get(pk=pk)
            print("this si student doner", st)
            return HttpResponse("this is doner", st)
        else:

            doner = Doners.objects.get(pk=pk)
            print(doner.name.name)
            doner.amount += amount
            doner.paiddate = today.day
            doner.paidmonth = today.month
            doner.paidyear = today.year
            print("Muqtadi doenr about to dave", doner.paidyear, doner.paid)
            doner.save()
            print("Muqtadi doner saved")
            return HttpResponse("this si student doner Get", doner.name)



class Muqdonerdetail(LoginRequiredMixin,DetailView):
    model= Doners
    template_name = "employ/doner/muqdondetail.html"
    context_object_name = "muqdoner"
    fields="__all__"


class Muqdonupdate(LoginRequiredMixin,UpdateView):
    model= Doners
    template_name = "employ/doner/muqdonupdate.html"
    context_object_name = "muqdoner"
    fields=['amount']

    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('muqdonerdetail', kwargs={'pk': id})
    
    
    
    
    
#*********************************************#
#Imam
class Admcreateimam(SuperUserRequiredMixin,CreateView):
    template_name='imam/createimam.html'
    model=Teacher
    form=Imamform
    fields= ["name","phone","is_imam","is_teacher","courses","salary","address","cnic","qualification","educenter"]
    success_url='/imamlist'
    initial={'is_imam':True}

    def form_valid(self, form):
        form.save(commit=False)
        if self.request.user.is_superuser:
            if form.cleaned_data['is_imam'] is False and form.cleaned_data['is_teacher'] is False:
                print("both are emptyyyyyyy")
                messages.error(self.request, 'select iamam or teacher or both')
                return HttpResponseRedirect("createimam")
            form.save()
        return super().form_valid(form)





@login_required
def imamcv(request,pk):
        if not request.user.is_superuser:
            educenter=Educenter.objects.all().filter(pk=pk)
            n=educenter[0]
            if request.method=='POST':
                form=Imamform(request.POST)
                if form.is_valid():
                   form.save()
                   return redirect('imamlist')
                else:
                   form=Imamform(request.POST,initial={'educenter':n})          
                   return render(request,"Imam/createimam.html",{'form':form})
            else:
              form=Imamform(initial={'educenter':n,'name':n})
              return render(request,"Imam/createimam.html",{'form':form})
 


    
class Imamlist(LoginRequiredMixin,ListView):
    template_name="Imam/imamlist.html"
    model=Teacher
    
    context_object_name="imamlist"
    fields=['name','salary','is_imam','address']
    def get_queryset(self):
        if self.request.user.is_superuser:
            qs=Teacher.objects.filter(is_imam=True)
            return qs
        else:
            try:
                qs=Teacher.objects.filter(is_imam=True)
                educenter=self.request.user.useradmin.educenter
                imamlist=qs.filter(educenter=educenter)
                print(imamlist)
                return imamlist
            except:
                pass
    
    
class Imamupdate(LoginRequiredMixin,UpdateView):
    kwargs=id
    template_name="Imam/createimam.html"
    model=Teacher
    context_object_name="educen"
    fields= ["name","phone","salary",'is_imam','is_teacher','courses',"address","cnic","qualification","educenter"]
    success_url="/imamlist"
    
class Imamdelete(LoginRequiredMixin,DeleteView):
    kwargs=id
    template_name="conformdel.html"
    model=Teacher
    context_object_name="educen"
    fields='__all__'
    success_url="/imamlist"
    
    
class Imamdetail(LoginRequiredMixin,DetailView):
    kwargs=id
    template_name="imam/imamdetail.html"
    model=Teacher
    context_object_name="educen"
    fields='__all__'
    
    
    
#**********************************************
#Teaacher
#Imam
@login_required
def teachercv(request,pk):
        if not request.user.is_superuser:
            educenter=Educenter.objects.all().filter(pk=pk)
            n=educenter[0]
            if request.method=='POST':
                form=Teacherform(request.POST)
                print("this is before if valid")
                if form.is_valid():
                   form.cleaned_data['name']='888888888888888888000905'
                   print('____________________',form.cleaned_data['educenter'])
                   form.save()
                   messages.success(request,'teacher has been save')
                   return redirect('teacherlist')
                else:
                   print("this is not valid")
                   messages.warning(request,'this is get req')
                   form=Teacherform(request.POST,initial={'educenter':n,'is_teacher':True})
                   return render(request,"teacher/createteacher.html",{'form':form})
            else:
              print("this is get req")
              form=Teacherform(initial={'educenter':n,'name':n})
              return render(request,"teacher/createteacher.html",{'form':form})
 
    
    
    
class Createteacher(LoginRequiredMixin,CreateView):
    template_name="teacher/createteacher.html"
    model=Teacher
    initial={'is_teacher':True}
    fields= ["name","phone",'is_imam',"is_teacher","salary",'courses',"address","cnic","qualification","educenter"]
    success_url="teacherlist"

    
class Teacherlist(LoginRequiredMixin,ListView):
    template_name="teacher/teacherlist.html"
    model=Teacher
    context_object_name="teacherlist"
    fields=['name','salary','address']
    def get_queryset(self):
        if self.request.user.is_superuser:
            qs=Teacher.objects.filter(is_teacher=True).order_by('educenter')
            return qs
        else:
            try:
                qs = Teacher.objects.filter(is_teacher=True)
                educenter=self.request.user.useradmin.educenter.id
                qs=qs.filter(educenter=educenter).order_by('educenter')
                return qs
            except:
                pass
    
class Teacherupdate(LoginRequiredMixin,UpdateView):
    kwargs=id
    template_name="teacher/updateteacher.html"
    model=Teacher
    context_object_name="educen"
    fields= ["name","phone",'is_imam',"salary",'courses','admission_date','adm_month','adm_year',"address","cnic","qualification","educenter"]
    success_url="/teacherlist"

    
class Teacherdelete(LoginRequiredMixin,DeleteView):
    kwargs=id
    template_name="conformdel.html"
    model=Teacher
    context_object_name="educen"
    fields='__all__'
    success_url="teacherlist"    
    
    
class Teacherdetail(LoginRequiredMixin,DetailView):
    kwargs=id
    template_name="teacher/teacherdetail.html"
    model=Teacher
    context_object_name="educen"
    fields='__all__'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id=self.kwargs['pk']
        teacher=Teacher.objects.get(id=id)
        courses=teacher.courses.all()

        context['courses']=courses
        return context
#TEACHER DONER

class Teachdonerlist(LoginRequiredMixin,ListView):
    model=Teachdoner
    context_object_name="teachdonlist"
    template_name="teacher/teachdonerlist.html"
    fields=['name','month','year']
    def get_queryset(self):
        month = self.kwargs['month']
        year = self.kwargs['year']
        #function for creatind teacerh every month fromm utils
        create_teachdoner()
        create_monthlyrev()
        try:
             calculate_mrevenue(month, year)
        except:
            pass
        create_revenue()


        if self.request.user.is_superuser:
            teachdoner=Teachdoner.objects.all().order_by('name').filter(month=month ,year=year)
            print('this is query kwargs', self.kwargs)
            return teachdoner
        else:
            try:
                educenter = self.request.user.useradmin.educenter.id
                teachdoner=Teachdoner.objects.all().filter(educen=educenter)
                teachdoner = teachdoner.filter(month=month, year=year)
                return teachdoner
            except:
                pass

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        month = self.kwargs['month']
        year = self.kwargs['year']
        if self.request.user.is_superuser:
            currentmonth_muq = Teachdoner.objects.all().order_by('name').filter(month=month, year=year)
            print("this is super user if true")
            paidamount = 0
            for i in currentmonth_muq:
                paidamount += i.amount
            unpaidamount = 0
            for i in currentmonth_muq:
                unpaidamount += i.name.salary
            context['unpaidamount'] = unpaidamount
            context['paidamount'] = paidamount
            return context

        if not self.request.user.is_superuser:
            try:
                educenter = self.request.user.useradmin.educenter.id
                doners = Teachdoner.objects.all().filter(educen=educenter)
                currentmonth_muq = doners.filter(month=month, year=year)
                print("this is not  muqdoner super user true codition ")
                paidamount = 0
                for i in currentmonth_muq:
                    paidamount += i.amount
                unpaidamount = 0
                for i in currentmonth_muq:
                    unpaidamount += i.name.salary
                context['unpaidamount'] = unpaidamount
                context['paidamount'] = paidamount
                return context
            except:
                pass







class Teachdonerdetail(LoginRequiredMixin,DetailView):
    model=Teachdoner
    context_object_name="teachdoner"
    template_name="teacher/teachdondetail.html"
    fields="__all__"

class Teachdonerupdate(LoginRequiredMixin,UpdateView):
    model=Teachdoner
    template_name ="teacher/teachdonupdate.html"
    fields=['amount']
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('teachdonerdetail', kwargs = {'pk': pk})

@login_required
def teachdonerpaid(request,pk,amount):
    if request.method=="POST":
        st=Teachdoner.objects.get(pk=pk)
        print("this si student doner", st)
        return HttpResponse("this is doner",st)
    else:
        st = Teachdoner.objects.get(pk=pk)
        teacher_fee=Teacher.objects.get(pk=st.name.id).salary
        teacher_name = Teacher.objects.get(pk=st.name.id).name
        print("Student name ",teacher_fee)

        print(st.name.name)
        st.amount+=amount
        if st.amount >= teacher_fee:
            print("st.amount",st.amount,"teacher fee",teacher_fee,"OOOOO",teacher_name)
            st.paid=True
        else:
            st.paid=False
        print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",st.paid,st.name)

        st.paiddate=today.day
        st.paidmonth=today.month
        st.paidyear=today.year
        print("Teachdoenr about to dave",st.paidyear,st.paid)
        st.save()
        print("Teachdoenr saved")
        return HttpResponse("this si student doner Get", st.name)








#**************************************************#

#Student

@login_required
def stucv(request,pk):
        if not request.user.is_superuser:
            educenter=Educenter.objects.all().filter(pk=pk)
            n=educenter[0]
            if request.method=='POST':
                form=Stuform(request.POST)
                if form.is_valid():
                   form.save()
                   return redirect('stulist')
                else:
                   form=Stuform(request.POST,initial={'educenter':n})
                   return render(request,"stu/createstu.html",{'form':form})
            else:
              form=Stuform(initial={'educenter':n})
              return render(request,"stu/createstu.html",{'form':form})
        else:
            return redirect('admcreatestu')




class Createstu(SuperUserRequiredMixin,CreateView):
    template_name = "stu/createstu.html"
    model = Student
    success_url="stulist"
    fields = "__all__"




class Stulist(LoginRequiredMixin,ListView):
    template_name="stu/stulist.html"
    model=Student
    context_object_name="studentlist"
    fields="__all__"
    def get_queryset(self):
        if self.request.user.is_superuser:
            qs=Student.objects.filter(is_deleted=False).order_by('educenter')
            return qs
        else:
            try:
                qs = Student.objects.filter(is_deleted=False)
                educenter=self.request.user.useradmin.educenter.id
                qs=qs.filter(educenter=educenter).order_by('id')
                return qs
            except:
                pass

class Studetail(LoginRequiredMixin,DetailView):
    kwargs = id
    template_name = "stu/studentdetal.html"
    model = Student
    context_object_name = "student"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        stu = Student.objects.get(id=id)
        courses = stu.courses.all()

        context['courses'] = courses
        return context

    
    
class Stuupdate(LoginRequiredMixin,UpdateView):
    kwargs=id
    template_name="stu/updatestu.html"
    model=Student
    context_object_name="educen"
    fields="__all__"
    success_url="/"
    
class Studelete(LoginRequiredMixin,DeleteView):
    kwargs=id
    template_name="conformdel.html"
    model=Student
    context_object_name="student"
    fields='__all__'
    success_url="/"
    
    
    
#STUDONERSStuDoners
class Studonerdetail(LoginRequiredMixin,DetailView):
    model=StuDoners
    context_object_name="studoner"
    template_name="stu/studondetail.html"
    fields="__all__"





class Studonerlist(LoginRequiredMixin,ListView):
    model=StuDoners
    context_object_name="muqdonlist"
    template_name="stu/donerlist.html"
    fields=['name','month','year']
    def get_queryset(self):
        month = self.kwargs['month']
        year = self.kwargs['year']
        #function for creatind doners every month from utils
        create_studoner()
        create_monthlyrev()
        try:
            calculate_mrevenue(month, year)
        except:
            pass
        create_revenue()

        if self.request.user.is_superuser:
            studoner=StuDoners.objects.all().order_by('educen').filter(month=month ,year=year)
            print('this is query kwargs', self.kwargs)
            return studoner
        else:
            try:
                educenter = self.request.user.useradmin.educenter.id
                studoners=StuDoners.objects.all().filter(educen=educenter)
                studoner = studoners.filter(month=month, year=year)
                return studoner
            except:
                pass

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        month = self.kwargs['month']
        year = self.kwargs['year']
        if self.request.user.is_superuser:
            currentmonth_muq = StuDoners.objects.all().order_by('name').filter(month=month, year=year)
            print("this is super user if true")
            paidamount = 0
            for i in currentmonth_muq:
                paidamount += i.amount
            unpaidamount = 0
            for i in currentmonth_muq:
                unpaidamount += i.name.fee
            context['unpaidamount'] = unpaidamount
            context['paidamount'] = paidamount
            return context

        if not self.request.user.is_superuser:
            try:
                educenter = self.request.user.useradmin.educenter.id
                doners = StuDoners.objects.all().filter(educen=educenter)
                currentmonth_muq = doners.filter(month=month, year=year)
                print("this is not  muqdoner super user true codition ")
                paidamount = 0
                for i in currentmonth_muq:
                    paidamount += i.amount
                unpaidamount = 0
                for i in currentmonth_muq:
                    unpaidamount += i.name.fee
                context['unpaidamount'] = unpaidamount
                context['paidamount'] = paidamount
                return context
            except:
                pass




class Studonerupdate(LoginRequiredMixin,UpdateView):
    model=StuDoners
    template_name ="stu/studonupdate.html"
    fields=['amount']

    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('studonerdetail', kwargs = {'pk': id})

@login_required
def studonerpaid(request,pk,amount):
    if request.method=="POST":
        st=StuDoners.objects.get(id=pk)
        print("this si student doner", st)
        return HttpResponse("this is doner",st)
    else:
        st = StuDoners.objects.get(id=pk)
        student_fee=Student.objects.get(id=st.name.id).fee
        print("Student name ",student_fee)

        st.amount+=amount
        if st.amount< student_fee:
            st.paid=False
        else:
            st.paid=True

        st.paiddate=today.day
        st.paidmonth=today.month
        st.paidyear=today.year
        print("st about to dave",st.paidyear,"this is status",st.paid)
        st.save()
        print("st saved")

        return HttpResponse("this si student doner Get", st.name)




#*****************************************#
#Courses
@login_required
def coursecv(request,pk):
        if not request.user.is_superuser:
            educenter=Educenter.objects.all().filter(pk=pk)
            n=educenter[0]
            if request.method=='POST':
                form=Courseform(request.POST)
                if form.is_valid():
                   form.cleaned_data['name']='888888888888888888000905'
                   print('____________________',form.cleaned_data['educenter'])
                   form.save()
                   return redirect('courseslist')
                else:
                   form=Courseform(request.POST,initial={'educenter':n})
                   return render(request,"Courses/createCourses.html",{'form':form})
            else:
              form=Courseform(initial={'educenter':n,'name':n})
              return render(request,"Courses/createCourses.html",{'form':form})





class Createcourses(LoginRequiredMixin,CreateView):
    template_name="Courses/createCourses.html"
    model=Courses

    fields="__all__"
    success_url="/courseslist"



class Courselist(LoginRequiredMixin,ListView):
    template_name="Courses/Courselist.html"
    model=Courses
    context_object_name="courses"
    fields="__all__"
    def get_queryset(self):
        if self.request.user.is_superuser:
            qs=Courses.objects.filter(is_deleted=False).order_by('educenter')
            return qs
        else:
            try:
                qs = Courses.objects.filter(is_deleted=False)
                educenter=self.request.user.useradmin.educenter.id
                qs=qs.filter(educenter=educenter).order_by('name')
                return qs
            except:
                pass
    




class Courseupdate(LoginRequiredMixin,UpdateView):
    kwargs=id
    template_name="Courses/updateCourse.html"
    model=Courses
    context_object_name="educen"
    fields="__all__"
    success_url="/courseslist"
    
class Coursedelete(LoginRequiredMixin,DeleteView):
    kwargs=id
    template_name="conformdel.html"
    model=Courses
    context_object_name="educen"
    success_url="/courseslist"
    
#################################################################################
#side fund

def sidefundcv(request, pk):
        if not request.user.is_superuser:
            educenter = Educenter.objects.all().filter(pk=pk)
            n = educenter[0]
            if request.method == 'POST':
                form = Sidefundform(request.POST)
                if form.is_valid():
                    print('____________________', form.cleaned_data['educenter'])
                    form.save()
                    return redirect('sidefundlist')
                else:
                    userr = request.user.useradmin
                    educenterr = get_object_or_404(Educenter, useradmin=userr)
                    edudoners = Muqtadi.objects.all().filter(educenter=educenterr)
                    form = Sidefundform(request.POST,initial={'educenter': n})
                    return render(request, "sidefund/createsidefund.html", {'form': form, 'doners': edudoners})
            else:
                userr = request.user.useradmin
                educenterr = get_object_or_404(Educenter, useradmin=userr)
                edudoners = Muqtadi.objects.all().filter(educenter=educenterr)
                form = Sidefundform(initial={'educenter': n})
                return render(request, "sidefund/createsidefund.html", {'form': form,'doners':edudoners})


class Createsidefund(LoginRequiredMixin,CreateView):
    template_name = "sidefund/createsidefund.html"
    model = Sidefund
    fields = ["title","name","doner","foreigner", "educenter", "description", 'amount', 'date', 'month', 'year']
    success_url = "/sidefundlist"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if  self.request.user.is_superuser:
            return context
        else:
            userr = self.request.user.useradmin
            educenterr = get_object_or_404(Educenter,useradmin=userr)
            edudoners=Muqtadi.objects.all().filter(educenter=educenterr)
            context['doners'] = edudoners
            return context


class Sidefundlist(LoginRequiredMixin,ListView):
    template_name = "sidefund/sidefundlist.html"
    model = Sidefund
    fields = "__all__"

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Sidefund.objects.filter(is_deleted=False).order_by('educenter')
            return qs
        else:
            try:
                qs = Sidefund.objects.filter(is_deleted=False)
                educenter = self.request.user.useradmin.educenter.id
                qs = qs.filter(educenter=educenter).order_by('title')
                return qs
            except:
                pass


class Sidefundupdate(LoginRequiredMixin,UpdateView):
    kwargs = id
    template_name = "sidefund/createsidefund.html"
    model = Sidefund
    context_object_name = "educen"
    fields = "__all__"
    success_url = "/sidefundlist"


class Sidefunddelete(LoginRequiredMixin,DeleteView):
    kwargs = id
    template_name = "conformdel.html"
    model = Sidefund
    context_object_name = "educen"
    success_url = "/sidefundlist"



#################################################################################
#Expenses

def createexpensecv(request, pk):
        if not request.user.is_superuser:
            educenter = Educenter.objects.all().filter(pk=pk)
            n = educenter[0]
            if request.method == 'POST':
                form = Expenseform(request.POST)
                if form.is_valid():
                    print('____________________', form.cleaned_data['educenter'])
                    form.save()
                    return redirect('sidefundlist')
                else:
                    userr = request.user.useradmin
                    educenterr = get_object_or_404(Educenter, useradmin=userr)
                    edudoners = Muqtadi.objects.all().filter(educenter=educenterr)
                    form = Expenseform(request.POST,initial={'educenter': n})
                    return render(request, "expenses/createexpense.html", {'form': form, 'doners': edudoners})
            else:
                userr = request.user.useradmin
                educenterr = get_object_or_404(Educenter, useradmin=userr)
                edudoners = Muqtadi.objects.all().filter(educenter=educenterr)
                form = Expenseform(initial={'educenter': n})
                return render(request, "expenses/createexpense.html", {'form': form,'doners':edudoners})


class Createexpense(LoginRequiredMixin,CreateView):
    template_name = "expenses/createexpense.html"
    model = Expenses
    fields = ["title", "educenter", "description", 'amount', 'date', 'month', 'year']
    success_url = "/expenselist"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if  self.request.user.is_superuser:
            return context
        else:
            userr = self.request.user.useradmin
            educenterr = get_object_or_404(Educenter,useradmin=userr)
            edudoners=Muqtadi.objects.all().filter(educenter=educenterr)
            context['doners'] = edudoners
            return context


class Expenselist(LoginRequiredMixin,ListView):
    template_name = "expenses/expenselist.html"
    model = Sidefund
    fields = "__all__"

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Expenses.objects.filter(is_deleted=False).order_by('educenter')
            return qs
        else:
            try:
                qs = Expenses.objects.filter(is_deleted=False)
                educenter = self.request.user.useradmin.educenter.id
                qs = qs.filter(educenter=educenter).order_by('title')
                return qs
            except:
                pass


class Expenseupdate(LoginRequiredMixin,UpdateView):
    kwargs = id
    template_name = "expenses/createexpense.html"
    model = Expenses
    context_object_name = "educen"
    fields = "__all__"
    success_url = "/expenselist"


class Expensedelete(LoginRequiredMixin,DeleteView):
    kwargs = id
    template_name = "conformdel.html"
    model = Expenses
    context_object_name = "educen"
    success_url = "/expenselist"






