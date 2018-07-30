# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import datetime,timedelta
# Create your models here.

class User(models.Model):                           #inheritance class a(b)   models is
	Name = models.CharField(max_length=50)
	username=models.CharField(max_length=50, blank = False)
	password=models.CharField(max_length=50)
	contact = models.CharField(max_length=50)
	STATUSES = (
       # (u'E', u'Expected'),
        ('student', 'student'),
        ('librarian', 'librarian'),
       # key gets stored in models fields and valiue is displayed on the admin page for the user
    )

	type = models.CharField(max_length=15, null=True, choices=STATUSES)
	def __str__(self):
		return self.username+" "+self.password

class Books(models.Model):

	name = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	subject = models.CharField(max_length=50)
	rating = models.CharField(max_length=50)
	summary = models.TextField(max_length=5000)
	copies_avl=models.IntegerField(default=10)
	ISSUE_STATUSES = (
       # (u'E', u'Expected'),
       	('available', 'available'),
       	('unavailable', 'unavailable')
        
        ,
       # key gets stored in models fields and value is displayed on the admin page for the user
    )

	status = models.CharField(max_length=20, null=True, choices=ISSUE_STATUSES, default="available")


	def __str__(self):
		return self.name


class BookIssue(models.Model):
	student_name= models.CharField(max_length=50)
	#rollno = models.IntegerField(max_length=50)
	Book= models.ForeignKey(Books,on_delete=models.CASCADE)
	issue_date=models.DateTimeField()
	return_date=models.DateTimeField()

	ISSUE_STATUSES = (
       # (u'E', u'Expected'),
       	('booked', 'booked'),
       	('issued', 'issued'),
       	('returned','returned'),
       	('deadline_crossed','deadline_crossed'),
        
        
       # key gets stored in models fields and value is displayed on the admin page for the user
    )
	status = models.CharField(max_length=20, null=True, choices=ISSUE_STATUSES, default="booked")
	#issue_time=models.TimeField(auto_now=False, auto_now_add=True)
	fine=models.IntegerField(default=0)
	

	def __str__(self):
		return self.student_name;








