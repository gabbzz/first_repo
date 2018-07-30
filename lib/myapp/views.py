# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import models
from models import BookIssue
from django.http import HttpResponseRedirect 
from django.db.models import Q
from datetime import datetime
from datetime import timedelta
import pytz


from django.http import HttpResponse
from reportlab.pdfgen import canvas


def student_dashboard(request):
	if ("username" in request.session and request.session["type"]=="student"):
		context={}
		context["book_table"]= models.Books.objects.all()
		context["name"]=request.session["name"]
		context["username"]=request.session["username"]
		context["contact"]=request.session["contact"]
		#context["status"]=request.s
		context["book_history"] = models.BookIssue.objects.filter(student_name = request.session["name"])

		return render(request,'student_dashboard.html',context)
	else:
		return HttpResponseRedirect("/login/")



def lib_dashboard(request):
	if ("username" in request.session and request.session["type"]=="librarian"):
		context={}
		context["book_issue"]= models.BookIssue.objects.all()
		return render(request,'lib_dashboard.html',context)

	else:
		return HttpResponseRedirect("/login/")

@csrf_exempt
def register(request):
	
	""" take input
	    check if username exists
	    if not then add to database and redirect to login
	    if yes then render the register page again with a message to enter another username."""

	if(request.method=='GET'):
		return render(request,'register.html',{})

	elif(request.method=='POST'):
		context={}
		context['message'] = "User already exists.Use another username"
		Name=request.POST['Name']                        #its just an empty dictionary
		Username=request.POST['Username']
		Password=request.POST['Password']
		Type=request.POST['Type']
		Contact=request.POST['contact']


		if(models.User.objects.filter(username=Username).exists()):
			return render(request,"register.html",context)
		else:
			obj1 = models.User(username= Username,
			        password= Password,
			        contact=Contact,
			        Name = Name,
			        type=Type
			        )          #sequence does not matter in python in a parameterised constr.
			obj1.save()
	
	
			return HttpResponseRedirect("/login/")
	
@csrf_exempt
def login(request):

	""" take input
	check if username is in tabe
	if no -> user does not exist so render the register page along with message
	if yes check if password matches
	if not ... wrong password render the login page again with the wrong password message
	if yes -> check if student/librarian
	if student-> redirect to student.dashboard
	if librarrian -> riderct to librarian.dashboard"""

	if "username" in request.session:      #check if there is any data present in cookies(req.session).if yes then redirect to that particular dashboard

		if(request.session["type"]=="student"):
			return HttpResponseRedirect("/student_dashboard/")
		else:
			return HttpResponseRedirect("/lib_dashboard/")


	if (request.method == 'GET'):
		return render(request,'login.html',{})

	elif (request.method == 'POST'):

		Username=request.POST['Username']
		Password=request.POST['Password']

		if(models.User.objects.filter(username=Username).exists()):  # filter returns a list
		   #get()returns a single object  since our username is unique

			if(models.User.objects.filter(username=Username, password=Password).exists()):
				user_obj=models.User.objects.get(username=Username, password=Password)
				"""
				As soon as you login .. save the data of the logged in user in cookies ie request.session dict"""
				
				request.session["username"]=user_obj.username;
				request.session["name"]=user_obj.Name;
				#request.session["password"]=user_obj.password;  !!!!!!NEVER STORE PASSWORDS IN COOKIES!!!
				request.session["type"]=user_obj.type;
				request.session["contact"]=user_obj.contact;
				

				if (user_obj.type== 'student'):
					return HttpResponseRedirect("/student_dashboard/")
				elif (user_obj.type== 'librarian'):
					return HttpResponseRedirect("/lib_dashboard/")
					

			else:
				context={}
				context['message'] = "Password incorrect. Login again with corect password."
				return render(request,"login.html",context)

		else:
			context={}
			context['message'] = "You aren't registered. please register first"
			return render(request,"register.html",context)

@csrf_exempt
def logout(request):
	if "username" in request.session:
		del request.session["username"]
	return HttpResponseRedirect("/login/")


@csrf_exempt
def summary(request):
	id = request.GET["book_id"]
	book_obj=models.Books.objects.get(id=id)

	context={}
	context["name"]=book_obj.name;
	context["summary"]= book_obj.summary;
	context["author"]= book_obj.author;
	context["rating"]= book_obj.rating;
	context["subject"]= book_obj.subject;
	if book_obj.copies_avl>1:
		context["status"]= "Available";
	
		



	return render(request,"summary.html",context)


@csrf_exempt
def search(request):
	search=request.POST["search"]
	
	filtered_books=models.Books.objects.filter(Q(author=search)|Q(name=search)|Q(subject=search))
	context={}
		#context["author"]=request.POST["search_by_author"]
	context["book_table"]=filtered_books
	return render(request,"student_dashboard.html",context);

@csrf_exempt
def profile(request):
	context={}
	context["book_table"]= models.Books.objects.all()
	context["name"]=request.session["name"]
	context["username"]=request.session["username"]
	context["contact"]=request.session["contact"]

	return render(request,"profile.html",context);

@csrf_exempt
def home(request):
	if("username" in request.session and request.session["type"]=="student"):
		return HttpResponseRedirect("/student_dashboard/")

	elif("username" in request.session and request.session["type"]=="librarian"):

		return HttpResponseRedirect("/librarian_dashboard/")

	else:

		return HttpResponseRedirect("/login/")



@csrf_exempt
def issue(request):

	issued_book_id= request.GET["book_id"];
	#print "book_id ="+issued_book_id;
	issued_book=models.Books.objects.get(id = issued_book_id );
	#print issued_book.name;
	#print issued_book.copies_avl;

	issued_book.copies_avl = issued_book.copies_avl-1;
	if issued_book.copies_avl== 0:
		issued_book.status="unavailable"
	issued_book.save();
	
	# naive = datetime.replace(tzinfo=None)
	issue_model = BookIssue(student_name=request.session["name"],Book=issued_book,issue_date= datetime.now().replace(tzinfo=None),return_date=datetime.now().replace(tzinfo=None)+timedelta(days=7)).save();
	
	#BookIssue.objects.all().save();
	#print issue_model.Book_name
	# print issued_book.copies_avl;


	return HttpResponseRedirect("/student_dashboard/")


@csrf_exempt
def book_is_issued(request):
	issued_book_id = request.GET["issued_id"];

	entry = models.BookIssue.objects.get(id =issued_book_id);
	entry.status="issued"
	entry.save()
	return HttpResponseRedirect("/lib_dashboard/")

@csrf_exempt
def return_book(request):
	returned_book_id = request.GET["return_id"]

	entry = models.BookIssue.objects.get(id =returned_book_id)
	entry.status="returned"
	entry.save()
	return HttpResponseRedirect("/lib_dashboard/")

def delete_book(request):
	deleted_book_name = request.GET["deleted_name"]
	deleted_book_id = request.GET["delete_id"]
	entry = models.BookIssue.objects.get(id = deleted_book_id)
	entry.delete()
	deleted_book = models.Books.objects.get(name=deleted_book_name)
	deleted_book.copies_avl = deleted_book.copies_avl+1
	deleted_book.save()

	return HttpResponseRedirect("/shelf_books/")

@csrf_exempt
def shelf_books(request):
	context= {}
	context["shelf_books"] = models.Books.objects.filter(status="available")
	return render(request,'shelf_books.html',context)

@csrf_exempt
def table_books(request):
	context= {}
	context["table_books"] = models.BookIssue.objects.filter(status="booked")
	return render(request,'table_books.html',context)

@csrf_exempt
def returned_books(request):
	context= {}
	context["returned_books"] = models.BookIssue.objects.filter(status="returned")
	return render(request,'returned_books.html',context)



@csrf_exempt
def move_all_to_shelf(request):
	returned_books = models.BookIssue.objects.filter(status="returned")

	for i in returned_books:
		deleted_book = models.Books.objects.get(id = i.id)
		deleted_book.copies_avl = deleted_book.copies_avl-1
		deleted_book.save()


	returned_books.delete()	
	return HttpResponseRedirect("/shelf_books/")

@csrf_exempt
def issued_books(request):
	context= {}
	issued_books=models.BookIssue.objects.filter(status="issued")
	# naive = datetime.replace(tzinfo=None)
	for i in issued_books:
		#time_delta = datetime.now().replace(tzinfo=None) - i.issue_date
		now_aware = pytz.utc.localize(datetime.now())
		time_delta = now_aware - i.issue_date

		if time_delta.days > 0:
			i.fine = 50*(time_delta.days)


	context["issued_books"] = issued_books
	


	return render(request,'issued_books.html',context)


@csrf_exempt
def reciept(request):
	# Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="FineReciept.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)


    student_name= request.GET["student_name"]
    book_name= request.GET["book_name"]
    issue_date=request.GET["issue_date"]
    return_date=request.GET["return_date"]
    fine=request.GET["fine"]
    current_date = str(datetime.now())




    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(150, 800, "PUNE INSTITUTE OF COMPUTER TECHNOLOGY")
    p.drawString(225, 770, "STUDENT LIBRARY")
    p.drawString(240, 740, "FINE-RECIEPT")
    p.drawString(150,690,"Student Name :     "+student_name)
    p.drawString(150,660,"Issued Book :     "+book_name)
    p.drawString(150,630,"Issue Date :     "+issue_date)
    p.drawString(150,600,"Return Date :     "+return_date)
    # p.drawString(150,600,"Current Date :     "+current_date)
    p.drawString(150,570,"Total Fine :     Rs."+fine)
    # p.drawString(150,690,"Student Name :     "+student_name)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response






	
