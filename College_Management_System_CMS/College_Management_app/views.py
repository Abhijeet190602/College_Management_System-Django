from typing import assert_type
from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import C_User, Staffs, Students, AdminHOD, SessionYearModel
from django.contrib import messages

def home(request):
	return render(request, 'home.html')


def contact(request):
	return render(request, 'contact.html')


def loginUser(request):
	return render(request, 'login_page.html')

def doLogin(request):
	
	print("here")
	email_id = request.GET.get('email')
	password = request.GET.get('password')
	user_type = request.GET.get('user_type')
	print(email_id)
	print(password)
	print(request.user)
	print(user_type)
	if not (email_id and password):
		messages.error(request, "Please provide all the details!!")
		return render(request, 'login_page.html')

	user = C_User.objects.filter(email=email_id, password=password).last()
	if not user:
		messages.error(request, 'Invalid Login Credentials!!')
		return render(request, 'login_page.html')

	login(request, user)
	

	if user.user_type == C_User.STUDENT:
		return redirect('student_home/')
	elif user.user_type == C_User.STAFF:
		return redirect('staff_home/')
	elif user.user_type == C_User.HOD:
		return redirect('admin_home/')

	return render(request, 'home.html')

	
def registration(request):
	return render(request, 'registration.html')
	

def doRegistration(request):
	first_name = request.GET.get('first_name')
	last_name = request.GET.get('last_name')
	email_id = request.GET.get('email')
	password = request.GET.get('password')
	confirm_password = request.GET.get('confirmPassword')
	#user_type = request.GET.get('user_type')
	print(email_id)
	print(password)
	print(confirm_password)
	print(first_name)
	print(last_name)
	#print(user_type)
	if not (email_id and password and confirm_password):
		messages.error(request, 'Please provide all the details!!')
		return render(request, 'registration.html')
	
	if password != confirm_password:
		messages.error(request, 'Both passwords should match!!')
		return render(request, 'registration.html')

	is_user_exists = C_User.objects.filter(email=email_id).exists()

	if is_user_exists:
		messages.error(request, 'User with this email id already exists. Please proceed to login!!')
		return render(request, 'registration.html')

	user_type = get_user_type_from_email(email_id)

	if user_type is None:
		messages.error(request, "Please use valid format for the email id: '<username>.<staff|student|hod>@<college_domain>'")
		return render(request, 'registration.html')

	username = email_id.split('@')[0].split('.')[0]

	if C_User.objects.filter(username=username).exists():
		messages.error(request, 'User with this username already exists. Please use different username')
		return render(request, 'registration.html')

	user = C_User()
	user.username = C_User.username
	user.email = C_User.email_id
	user.password = C_User.password
	user.user_type = C_User.user_type
	user.first_name = C_User.first_name
	user.last_name = C_User.last_name
	user.save()
	
	if user_type == C_User.STAFF:
		Staffs.objects.create(admin=user)
	elif user_type == C_User.STUDENT:
		Students.objects.create(admin=user)
	elif user_type == C_User.HOD:
		AdminHOD.objects.create(admin=user)
	return render(request, 'login_page.html')

	
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')


def get_user_type_from_email(email_id):
	"""
	Returns C_User.user_type corresponding to the given email address
	email_id should be in following format:
	'<username>.<staff|student|hod>@<college_domain>'
	eg.: 'abhishek.staff@jecrc.com'
	"""

	try:
		email_id = email_id.split('@')[0]
		email_user_type = email_id.split('.')[1]
		return C_User.EMAIL_TO_USER_TYPE_MAP[email_user_type]
	except:
		return None


# def session_year_view(request):
#     if request.method == 'POST':
#         form = SessionYearForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('session_year_list')  # Adjust the redirect as necessary
#     else:
#         form = SessionYearForm()
#     return render(request, 'session_year_form.html', {'form': form})

# def session_year_list_view(request):
#     session_years = SessionYearModel.objects.all()
#     return render(request, 'session_year_list.html', {'session_years': session_years})