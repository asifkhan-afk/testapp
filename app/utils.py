import  datetime
from .models import *



today = datetime.date.today()
currentmonth = today.month
currentyear = today.year

def create_revenue():
    educen = Educenter.objects.all()
    for i in educen:
        print("*************")
        print(i)
        revenue = Revenue.objects.get(educenter=i)

        educenrev = 0
        doners = Doners.objects.filter(educen=i)
        studoners = StuDoners.objects.filter(educen=i)
        teachrecever = Teachdoner.objects.filter(educen=i)
        additionalfunds=Sidefund.objects.filter(educenter=i)
        expenses=Expenses.objects.filter(educenter=i)
        for j in studoners:
            educenrev += j.amount
            print("student ))",j.name)
            print("student fee", j.amount)
            print("revenue",educenrev)
        for j in doners:
            print("muqtadi", j.name)
            print("muqtadi fee", j.amount)
            educenrev += j.amount
            print("revenue",educenrev)
        for h in additionalfunds:

            print("addittion fund fee", h.amount)
            educenrev += h.amount
            print("revenue",educenrev)
        for j in teachrecever:

            print("teacher salary",j.amount)
            educenrev -= j.amount
            print("revenue after teacher ", educenrev)
        for j in expenses:

            print("teacher salary",j.amount)
            educenrev -= j.amount
            print("revenue after teacher ", educenrev)
        revenue.balance = educenrev
        revenue.save()
        print("this is the last total revenue ",educenrev)
        print("this is revenue of current masjid",i.name,revenue.balance)


#calculate montlhy revenue amount
def calculate_mrevenue(month,year):
    educen = Educenter.objects.all()
    for i in educen:
        print("*************")
        print(i)
        revenue = Monthrevenue.objects.filter(educenter=i).get(month=month,year=year)
        educenrev = 0
        doners = Doners.objects.filter(educen=i)
        doners=doners.filter(month=month,year=year)
        studoners = StuDoners.objects.filter(educen=i)
        studoners=studoners.filter(month=month,year=year)
        teachrecever = Teachdoner.objects.filter(educen=i)
        teachrecever=teachrecever.filter(month=month,year=year)
        additionalfunds=Sidefund.objects.filter(educenter=i)
        additionalfunds=additionalfunds.filter(month=month,year=year)
        expenses=Expenses.objects.filter(educenter=i)
        expenses=expenses.filter(month=month,year=year)
        for j in studoners:
            educenrev += j.amount
            print("student ))",j.name)
            print("student fee", j.amount)
            print("revenue",educenrev)
        for j in doners:
            print("muqtadi", j.name)
            print("muqtadi fee", j.amount)
            educenrev += j.amount
            print("revenue",educenrev)
        for h in additionalfunds:

            print("addittion fund fee", h.amount)
            educenrev += h.amount
            print("revenue",educenrev)
        for j in teachrecever:
            print("teacher ",j.name)
            print("teacher salary",j.amount)
            educenrev -= j.amount
            print("revenue after teacher ", educenrev)
        for j in expenses:

            print("teacher salary",j.amount)
            educenrev -= j.amount
            print("revenue after teacher ", educenrev)
        revenue.balance = educenrev
        revenue.save()
        print("this is the last total Monthly revenue ",educenrev)
        print("this is Monthly revenue of current masjid",i.name,revenue.balance)



#create monthly revenue objects
def create_monthlyrev():
    mrevenue=Monthrevenue.objects.all()
    educen=Educenter.objects.all()
    current_revenue=Monthrevenue.objects.filter(month=currentmonth)
    if current_revenue.count() < educen.count():
        for i in educen:

            mrevenue = Monthrevenue()

            mrevenue.balance = 0
            mrevenue.month = currentmonth
            mrevenue.year = currentyear
            mrevenue.educenter = i
            mrevenue.educenter_id=str(i.id)
            print("monthly revenue is about to try")
            try:
                mrevenue.save()
                print("monthly revenue is saved from utils")
            except:
                print("montly revenue is already exists")


def create_muqdoner():
    muqtadidoners = Doners.objects.all()
    muqdoner = StuDoners.objects.filter(month=currentmonth, year=currentyear)
    muqtadi = Muqtadi.objects.all()
    print("this are students", muqtadi)
    print("these are current date doners", muqdoner)
    if muqdoner.count() < muqtadi.count():
        print("in the yes section of if")
        for i in muqtadi:

            mdoner = Doners()
            name = Muqtadi.objects.get(pk=i.pk)
            mdoner.name = name
            mdoner.educen = Educenter.objects.get(pk=i.educenter.pk)
            mdoner.name_id = str(name.id)
            mdoner.month = currentmonth
            mdoner.year = currentyear
            mdoner.paid = False
            print("Muqtadi doenr is created")
            print("name of created Muqtadi doner", mdoner.month)
            if mdoner not in muqdoner:
                try:
                    mdoner.save()
                    print("Muqtadi doner is saved")
                except:
                    print("Muqtadi already exvept")
            else:
                print("already exixst")
            print("create Muqtadi doenr fun from utils peroformed")













def create_teachdoner():
    allteachdoner = StuDoners.objects.all()
    currentdoner = StuDoners.objects.filter(month=currentmonth, year=currentyear)
    allteacher = Teacher.objects.all()
    print("this are students", allteacher)
    print("these are current date doners", currentdoner)
    if currentdoner.count() < allteacher.count():
        print("in the yes section of if")
        for i in allteacher:
            teachdoner = Teachdoner()
            name = Teacher.objects.get(pk=i.pk)
            teachdoner.name = name
            teachdoner.educen = Educenter.objects.get(pk=i.educenter.pk)
            teachdoner.name_id = str(name.id)
            teachdoner.month = currentmonth
            teachdoner.year = currentyear
            teachdoner.paid = False
            print("teacher doenr is created")
            print("name of created  teacher doner", teachdoner.month)
            if teachdoner not in currentdoner:
                try:
                    teachdoner.save()
                    print("teacher doner is saved")
                except:
                    print("teacher doenrr already exvept Except!")
            else:
                print("already exixst")
            print("create teach doenr fun from utils peroformed")






def create_studoner():
    studentdoners = StuDoners.objects.all()
    studoner = StuDoners.objects.filter(month=currentmonth, year=currentyear)
    student = Student.objects.all()
    print("this are students", student)
    print("these are current date doners", studoner)
    if studoner.count() < student.count():
        print("in the yes section of if")
        for i in student:

            stdoner = StuDoners()
            name = Student.objects.get(pk=i.pk)
            stdoner.name = name
            stdoner.educen = Educenter.objects.get(pk=i.educenter.pk)
            stdoner.name_id = str(name.id)
            stdoner.month = currentmonth
            stdoner.year = currentyear
            stdoner.paid = False
            print("student doenr is created")
            print("name of created doner", stdoner.month)
            if stdoner not in studentdoners:
                try:
                    stdoner.save()
                    print("student doner is saved")
                except:
                    print("already exvept")
            else:
                print("already exixst")
            print("create Student doenr fun from utils peroformed")

