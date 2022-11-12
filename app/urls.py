from turtle import home
from django.urls import URLPattern, path
from .views import *
urlpatterns=[
    path("",home,name="home"),
    path("paytmentmenue",TemplateView.as_view(template_name='paymentmenue.html'),name='paytmentmenue'),
    # show revenue of muqtadi
    path('showrevenue/<int:month>/<int:year>', Showrevenue.as_view(), name="showrevenue"),
    path('totalrevenue', Totalrevenue.as_view(), name="totalrevenue"),

    
    #user admin
    path("createuser",createuser,name="createuser"),
    path("updateuser/<int:id>",updateuser,name='updateuser'),
   path("userdetail/<pk>",Userdetail.as_view(),name='userdetail'),
    path("adminuserlist",Adminuserlist.as_view(),name="adminuserlist"),
    #conform del
    path("conformdel",conformdel,name="conformdel"),
    # admin edu form
    path('adminedu/<pk>/educhange',Admineducenter.as_view(),name='adminedu'),
    path('imamedu/<pk>',imameducenter,name='adimamedu'),

    
    #Edu center crud
    path('createeducen/<pk>', EducenterCV.as_view(), name='create_educenter'),
    path('educenlist',Educenlist.as_view(),name="educenlist"),
    path('educendetail/<pk>',Educendetail.as_view(),name="educendetail"),
    path('educenupdate/<pk>',Educenupdate.as_view(),name='educenupdate'),
    path('educendelete/<pk>',Educendelete.as_view(),name='educendelete'),
    # path('films/<int:pk>/update/', views.FilmUpdateView.as_view(), name='film_update'),
    
    #employ/Muqtadi
    path('admcreateemp/', Admempcv.as_view(), name='admcreateemp'),
    path('createemp/<pk>', empCV, name='create_emp'),
    path('employlist',Emplist.as_view(),name="emplist"),
    path('empupdate/<pk>',Empupdate.as_view(),name='empupdate'),
    path('empdelete/<pk>',Empdelete.as_view(),name='empdelete'),
   path('empdetail/<pk>',Empdetail.as_view(),name='empdetail'),
    #Doner
    path('muqdonerlist/<int:month>/<int:year>',Muqdonerlist.as_view(),name='muqdonerlist'),
    # path('showmuqdoner/',showmuqdoner,name='showmuqdonerlist'),
    # path('muqdondeposit/<int:id>',muqdepositCV,name='muqdondeposit'),
    path('muqdonerpaid/<int:pk>/<int:amount>', muqdonerpaid, name='muqdonerpaid'),
    path('muqdonerdetail/<int:pk>', Muqdonerdetail.as_view(), name='muqdonerdetail'),
    path('muqdonupdate/<int:pk>', Muqdonupdate.as_view(), name='muqdonupdate'),

    
    #Imam
     path('createimam',Admcreateimam.as_view(),name="admcreateimam"),
    path('createimam/<pk>', imamcv, name='createimam'),
    path('imamlist',Imamlist.as_view(),name="imamlist"),
    path('updateimam/<pk>',Imamupdate.as_view(),name='updateimam'),
    path('deleteimam/<pk>',Imamdelete.as_view(),name='deleteimam'),
     path('imamdetail/<pk>',Imamdetail.as_view(),name='imamdetail'),
    
    #teacher
    path("createteacher",Createteacher.as_view(),name="admcreateteacher"),
   path('createteacher/<pk>', teachercv, name='createteacher'),
    path('teacherlist',Teacherlist.as_view(),name="teacherlist"),
    path('updateteacher/<pk>',Teacherupdate.as_view(),name='updateteacher'),
    path('deleteteacher/<pk>',Teacherdelete.as_view(),name='deleteteacher'),
     path('teacherdetail/<pk>',Teacherdetail.as_view(),name='teacherdetail'),

    #doner
    path('teachdonerlist/<int:month>/<int:year>', Teachdonerlist.as_view(), name='teachdonerlist'),
    path('teachdonerdetail/<int:pk>', Teachdonerdetail.as_view(), name='teachdonerdetail'),
    path('teachdonerpaid/<int:pk>/<int:amount>', teachdonerpaid, name='teachdonerpaid'),
    path('teachdonerupdate/<int:pk>', Teachdonerupdate.as_view(), name='teachdonerupdate'),

    
    
    
    #Student
      path('createstu',Createstu.as_view(),name="admcreatestu"),
    path('createstu/<pk>', stucv, name='createstu'),
    path('stulist',Stulist.as_view(),name="stulist"),
    path('updatestu/<pk>',Stuupdate.as_view(),name='updatestu'),
    path('studetail/<pk>',Studetail.as_view(),name='studentdetail'),
    path('deletestu/<pk>',Studelete.as_view(),name='deletestu'),
    #doner
    path('studonerlist/<int:month>/<int:year>',Studonerlist.as_view(),name='studonerlist'),
    path('studonerdetail/<int:pk>',Studonerdetail.as_view(),name='studonerdetail'),
    path('studonerpaid/<int:pk>/<int:amount>',studonerpaid,name='studonerpaid'),
    path('studonerupdate/<int:pk>',Studonerupdate.as_view(),name='studonerupdate'),
       #Stu deposit

    #Courses
    path('createcourses', Createcourses.as_view(), name='admcreatecourses'),
    path('createourses/<pk>',coursecv, name='createCourses'),
    path('courseslist',Courselist.as_view(),name="courseslist"),
    path('updateCourses/<pk>',Courseupdate.as_view(),name='updateCourses'),
    path('deleteCourses/<pk>',Coursedelete.as_view(),name='deleteCourses'),


 #Side fund
    path('createsidefund', Createsidefund.as_view(), name='createsidefund'),
    path('createsidefund/<pk>',sidefundcv, name='createsidefund'),
    path('sidefundlist',Sidefundlist.as_view(),name="sidefundlist"),
    path('updatesidefund/<pk>',Sidefundupdate.as_view(),name='updatesidefund'),
    path('deletesidefund/<pk>',Sidefunddelete.as_view(),name='deletesidefund'),

 # Expenses
 path('createexpense', Createexpense.as_view(), name='createexpense'),
 path('createexpense/<pk>', createexpensecv, name='createexpense'),
 path('expenselist', Expenselist.as_view(), name="expenselist"),
 path('updateexpense/<pk>', Expenseupdate.as_view(), name='updateexpense'),
 path('deleteexpense/<pk>', Expensedelete.as_view(), name='deleteexpense'),


    
    
    
    ]