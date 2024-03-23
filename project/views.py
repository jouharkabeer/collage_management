from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages, auth
import re
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "index.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/admin_home')
        else:
            messages.info(request, "!!!Invalid credentials")
            return redirect('/admin_login')
    return render(request, "admin_login.html")



def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    students = Student.objects.count()
    hod = Hod.objects.count()
    faculty = Faculty.objects.count()
    alumni = Alumni.objects.count()
    pending_hod = Hod.objects.filter(status='pending').count()
    return render(request, "admin_home.html",{'students':students, 'pending_hod':pending_hod, 'hod':hod, 'faculty':faculty, 'alumni':alumni})

def all_students(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    students = Student.objects.all()
    return render(request, "all_students.html", {'students':students})

def pending_students(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    pending_students = Student.objects.filter(status="pending")
    return render(request, "pending_students.html", {'pending_students': pending_students})

def rejected_students(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    rejected_students = Student.objects.filter(status="Rejected")
    return render(request, "rejected_students.html", {'rejected_students': rejected_students})

def accepted_students(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    accepted_students = Student.objects.filter(status="Accepted")
    return render(request, "accepted_students.html", {'accepted_students': accepted_students})

def delete_student(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    student = Student.objects.get(sid=myid)
    student.delete()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page or '/all_students')

def delete_hod(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    hod = Hod.objects.get(id=myid)
    hod.delete()
    return redirect( '/all_hod')


def all_hod(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    hod = Hod.objects.all()
    return render(request, "all_hod.html", {'hod':hod})

def change_hod_status(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    hod = Hod.objects.get(id=myid)
    if request.method == "POST":
        status = request.POST['status']
        hod.status=status
        hod.save()
        alert = True
        return redirect("/all_hod")
    return render(request, "change_hod_status.html", {'hod':hod})


def student_login(request):
    if request.user.is_authenticated:
            return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Student.objects.get(user=user)
                if user1.type == "student":
                    if user1.status == "pending":
                        return render(request,"student_login.html",{"msg":"You need to be wait undil HOD approval"})
                    elif user1.status=='Rejected':
                        return render(request,"student_login.html",{"msg":"You account is HOD by admin"})
                    else:
                        login(request, user)
                        return redirect("/student_home")
            else:
                
                return render(request,"student_login.html",{"msg":"invalid"})
    return render(request, "student_login.html")


def student_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        aadhar_number = request.POST.get('aadhar_id')
        year = request.POST.get('year')
        department = request.POST.get('department')

        if username and first_name and last_name and password1 and password2 and phone and gender and image:
            # Validate phone number
            pattern = re.compile("(0|91)?[7-9][0-9]{9}")
            if not pattern.match(phone):
                return render(request, "student_signup.html", {"msg": "Invalid mobile number"})

            # Validate Aadhar number
            if not len(aadhar_number) == 12:
                return render(request, "student_signup.html", {"msg": "Invalid Aadhar number"})

            # Check if passwords match
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('/student_signup')

            # Validate username format
            if not re.match(r'^UCE\d{2}[A-Z]{2}\d{3}$', username):
                return render(request, "student_signup.html", {"msg": "Invalid username format. Example: UCE00AA000"})

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return render(request, "student_signup.html", {"msg": "Username already exists"})

            # Create user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=username, password=password1)

            # Create student
            student = Student.objects.create(user=user, phone=phone, gender=gender, image=image, type="student", aadhaar_number=aadhar_number,year=year, department=department, status="pending")
            
            student.save()
            user.save()
            # Redirect to login page
            return redirect("/student_login")
        else:
            return render(request, "student_signup.html", {"msg": "Please fill all fields"})

    return render(request, "student_signup.html")



def change_status_student(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    student = Student.objects.get(sid=myid)
    if request.method == "POST":
        status = request.POST['status']
        student.status=status
        student.save()
        alert = True
        return redirect("/all_students")
    return render(request, "change_status_student.html", {'company':student})


def student_home(request):
    if not request.user.is_authenticated:
        return redirect('/student_login')
    return render(request, "student_home.html")


def hod_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Hod.objects.get(user=user)
                if user1.type == "hod":
                    if user1.status == "pending":
                        return render(request,"hod_login.html",{"msg":"You need to be wait undil admin approval"})
                    elif user1.status=='Rejected':
                        return render(request,"hod_login.html",{"msg":"You account is blocked by admin"})
                    else:
                        login(request, user)
                        return redirect("/hod_home")
            else:
                
                return render(request,"hod_login.html",{"msg":"invalid"})
    return render(request, "hod_login.html")

def hod_signup(request):
    if request.method == "POST":
        username = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        aadhar_number = request.POST.get('aadhar_id')
        department = request.POST.get('department')

        if username and first_name and last_name and password1 and password2 and phone and image:
            # Validate phone number
            pattern = re.compile("(0|91)?[7-9][0-9]{9}")
            if not pattern.match(phone):
                return render(request, "hod_signup.html", {"msg": "Invalid mobile number"})

            # Validate Aadhar number
            if not len(aadhar_number) == 12:
                return render(request, "hod_signup.html", {"msg": "Invalid Aadhar number"})
            if Hod.objects.filter(aadhaar_number=aadhar_number).exists():
                return render(request, "hod_signup.html", {"msg": "adhaar already exists"})


            # Check if passwords match
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('/hod_signup')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return render(request, "hod_signup.html", {"msg": "Username already exists"})

            # Create user
            hod = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=username, password=password1)

            # Create hod
            hod = Hod.objects.create(user=hod, phone=phone, image=image, type="hod", aadhaar_number=aadhar_number, department=department, status="pending")
            
            hod.save()
            hod.save()
            # Redirect to login page
            return redirect("/hod_login")
        else:
            return render(request, "hod_signup.html", {"msg": "Please fill all fields"})

    return render(request, "hod_signup.html")

@login_required
def hod_home(request):
    try:
        hod = Hod.objects.get(user=request.user)
        department_students = Student.objects.filter(department=hod.department)
        return render(request, "hod_home.html", {'department_students': department_students})
    except Hod.DoesNotExist:
        return redirect("/hod_login")



def faculty_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Faculty.objects.get(user=user)
                if user1.type == "faculty":
                    if user1.status == "pending":
                        return render(request,"faculty_login.html",{"msg":"You need to be wait undil hod approval"})
                    elif user1.status=='Rejected':
                        return render(request,"faculty_login.html",{"msg":"You account is blocked by hod"})
                    else:
                        login(request, user)
                        return redirect("/faculty_home")
            else:
                return render(request,"faculty_login.html",{"msg":"invalid"})
    return render(request, "faculty_login.html")


def faculty_signup(request):
    if request.method == "POST":
        username = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        aadhar_number = request.POST.get('aadhar_id')
        department = request.POST.get('department')

        if username and first_name and last_name and password1 and password2 and phone and image:
            # Validate phone number
            pattern = re.compile("(0|91)?[7-9][0-9]{9}")
            if not pattern.match(phone):
                return render(request, "faculty_signup.html", {"msg": "Invalid mobile number"})

            # Validate Aadhar number
            if not len(aadhar_number) == 12:
                return render(request, "faculty_signup.html", {"msg": "Invalid Aadhar number"})
            if Faculty.objects.filter(aadhaar_number=aadhar_number).exists():
                return render(request, "faculty_signup.html", {"msg": "adhaar already exists"})


            # Check if passwords match
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('/faculty_signup')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return render(request, "faculty_signup.html", {"msg": "Username already exists"})

            faculty = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=username, password=password1)

            faculty = Faculty.objects.create(user=faculty, phone=phone, image=image, type="faculty", aadhaar_number=aadhar_number, department=department, status="pending")
            
            faculty.save()
            faculty.save()
            # Redirect to login page
            return redirect("/faculty_login")
        else:
            return render(request, "faculty_signup.html", {"msg": "Please fill all fields"})

    return render(request, "faculty_signup.html")


def alumni_login(request):
    if request.user.is_authenticated:
            return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Alumni.objects.get(user=user)
                if user1.type == "alumni":
                    if user1.status == "pending":
                        return render(request,"alumni_login.html",{"msg":"You need to be wait undil HOD approval"})
                    elif user1.status=='Rejected':
                        return render(request,"alumni_login.html",{"msg":"You account is HOD by admin"})
                    else:
                        login(request, user)
                        return redirect("/alumni_home")
            else:
                
                return render(request,"alumni_login.html",{"msg":"invalid"})
    return render(request, "alumni_login.html")

def alumni_signup(request):
    if request.method == "POST":
        username = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        aadhar_number = request.POST.get('aadhar_id')
        department = request.POST.get('department')
        year = request.POST.get('year_of_passout')

        if username and first_name and last_name and password1 and password2 and phone and image:
            # Validate phone number
            pattern = re.compile("(0|91)?[7-9][0-9]{9}")
            if not pattern.match(phone):
                return render(request, "alumni_signup.html", {"msg": "Invalid mobile number"})

            # Validate Aadhar number
            if not len(aadhar_number) == 12:
                return render(request, "alumni_signup.html", {"msg": "Invalid Aadhar number"})
            if Alumni.objects.filter(aadhaar_number=aadhar_number).exists():
                return render(request, "alumni_signup.html", {"msg": "adhaar already exists"})
            year = int(year)  # Convert year to integer

            if not (1995 <= year <= 2019):
                return render(request, "alumni_signup.html", {"msg": "The assosiated year is not valid for alumni"})
            

            # Check if passwords match
            if password1 != password2:
                return render(request, "alumni_signup.html", {"msg": "Password deosn't match"})


            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return render(request, "alumni_signup.html", {"msg": "Username already exists"})

            # Create user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=username, password=password1)

            # Create alumni
            alumni = Alumni.objects.create(user=user, phone=phone, image=image, type="alumni", year_of_passout= year, aadhaar_number=aadhar_number, department=department, status="pending")
            
            alumni.save()
            user.save()
            # Redirect to login page
            return redirect("/alumni_login")
        else:
            return render(request, "alumni_signup.html", {"msg": "Please fill all fields"})

    return render(request, "alumni_signup.html")


def Logout(request):
    logout(request)
    return redirect('/') 



def delete_all_data(request):
    Student.objects.all().delete()
    Faculty.objects.all().delete()
    Hod.objects.all().delete()
    Alumni.objects.all().delete()
    return redirect('/admin_home')
