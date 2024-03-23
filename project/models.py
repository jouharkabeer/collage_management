from operator import mod
from django.db import models
from django.contrib.auth.models import User



class Student(models.Model):
    sid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    gender = models.CharField(max_length=10)
    year = models.CharField(max_length=15)
    department = models.CharField(max_length=15)
    aadhaar_number = models.CharField(max_length=16, unique=True)
    status = models.CharField(max_length=20,null=True,blank=True)
    type = models.CharField(max_length=15)
    

    def _str_(self):
        return self.user.first_name
    
class Alumni(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=15)
    year_of_passout = models.IntegerField(null=True)
    image = models.ImageField(upload_to="")
    type = models.CharField(max_length=15)
    phone = models.IntegerField()
    aadhaar_number = models.CharField(max_length=16, unique=True)
    status = models.CharField(max_length=20,null=True,blank=True)



    def _str_(self):
            return self.user.first_name

class Hod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=15)
    image = models.ImageField(upload_to="")
    status = models.CharField(max_length=20,null=True,blank=True)
    type = models.CharField(max_length=15)
    phone = models.IntegerField()
    aadhaar_number = models.CharField(max_length=16, unique=True)

    

class Faculty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=15)
    image = models.ImageField(upload_to="")
    status = models.CharField(max_length=20,null=True,blank=True)
    type = models.CharField(max_length=15)
    phone = models.IntegerField()
    aadhaar_number = models.CharField(max_length=16, unique=True)


class Mark(models.Model):
    name = models.ForeignKey(Student, on_delete=models.CASCADE)
    sub1 = models.IntegerField(null=True)
    sub2 = models.IntegerField(null=True)
    sub3 = models.IntegerField(null=True)
    sub4 = models.IntegerField(null=True)
    sub5 = models.IntegerField(null=True)
    attendence = models.FloatField()

class Alumnipost(models.Model):
    name = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    link = models.URLField(null=True)
    discription = models.CharField(max_length = 30)
