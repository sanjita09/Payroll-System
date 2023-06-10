from django.urls import path
from . import views


app_name = "Management"
urlpatterns=[
    #path("", views.index, name="Home"),
    path('', views.indexLogin, name= 'indexLogin'),
    path('temp/', views.update_employee_salaries, name='update'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    # path('adminpage/', views.admin, name='adminpage'),
    path('index/', views.index, name='hr'),
    path('indexEMP/', views.indexEMP, name='employee'),

    path("fav/", views.view_fav, name="View_Favourite"),
    path("addfav/", views.add_fav, name="Add_Favourite"),
    path("addcompl/", views.add_complaint, name="Add_Complaint"),
    path("compl/", views.view_complaint, name="View_Complaint"),
    path("searchEMP/", views.searchemp, name="searchEMP"),
    path("signup/", views.sign_up, name="Sign_Up"),
    path("progresstable/", views.Progress_table, name="Progress_table"),
    path("template/", views.testing, name="testing"),
    path('addemployee/', views.Add_employee, name='Add_employee'),
    path('modifyemployee/', views.Modify_employee, name='Modify_employee'),
    path('applyleave/', views.Apply_leave, name='leave'),
    path('applyloan/', views.Apply_loan, name='loan'),
    path('getpayslip/',views.view_payslip, name='payslip'),
    path('download/',views.download_payslip,name='download_payslip'),
    path('downloadHR/',views.download_payslip_HR,name='downloadHR'),
    path("searchhr/", views.searchhr, name="SearchHR"),
    

        ] 