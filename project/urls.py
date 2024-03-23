from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("logout", views.Logout, name="logout"),

    
    #Admin Urls
    path('admin_login/', views.admin_login, name='admin login' ),
    path('admin_home', views.admin_home, name='admin home' ),
    path('all_students', views.all_students, name='all students'),
    path('pending_students', views.pending_students, name='pending students'),
    path('change_status_student/<int:myid>', views.change_status_student, name = 'change stauts'),
    path('rejected_students', views.rejected_students, name = 'rejected students'),
    path('accepted_students', views.accepted_students, name='accepted accepted'),
    path('delete_student/<int:myid>', views.delete_student , name='delete student'),
    path('all_hod', views.all_hod, name='all hod'),
    path('change_hod_status/<int:myid>', views.change_hod_status, name = 'change stauts'),
    path('delete_hod/<int:myid>', views.delete_hod , name='delete hod'),
    path('delete_all_data', views.delete_all_data, name = 'dalete data'),


    #Student Urls
    path('student_login', views.student_login, name='student login' ),
    path('student_signup', views.student_signup, name= 'student signup'),
    path('student_home', views.student_home, name= 'student home'),

    #hod urls
    path('hod_login', views.hod_login, name= 'hod login'),
    path('hod_signup', views.hod_signup, name= 'hod signup'),
    path('hod_home', views.hod_home, name= 'hod home'),


    #Faculty Urls
    path('faculty_login/', views.faculty_login, name='faculty login' ),
    path('faculty_signup/', views.faculty_signup, name='faculty signup' ),

    #Alumni Urls
    path('alumni_login', views.alumni_login, name='alumni login'),
    path('alumni_signup/', views.alumni_signup, name='alumni signup' ),

]