from django.contrib.auth import login
from django.shortcuts import render, redirect
from enroll.models import Student
from django.contrib import messages
import numpy as np
import pandas as pd
import pickle

# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def signupuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 !=pass2:
            messages.error(request,"password do not match")
            return redirect('signup')

        # Check if the username and email are unique
        if Student.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        else:
            # Create a new student object and save it
            student = Student(username=username, fname=fname, lname=lname, email=email, pass1=pass1, pass2=pass2)
            student.save()

        # Redirect to the login page after successful registration
        messages.error(request, f"{username} saved successfully")
        return redirect('login')
    else:
        return render(request,'reg.html')

def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        student = Student.objects.filter(username=username, pass1=pass1).first()
        if student:
            # Set the student ID in the session to keep the student logged in
            request.session['student_id'] = student.id
            messages.error(request, "Logged in successfully")
            return redirect('home')

        student = Student.objects.filter(email=username,pass1=pass1).first()
        if student:
            # Set the student ID in the session to keep the student logged in
            request.session['student_id'] = student.id
            messages.success(request, "Logged in Successfully")
            return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid Aadhaar number or password'})

    # return render(request, 'login.html')
    return render(request,'login.html')









from django.core.mail import send_mail
from django.conf import settings
import random
import time

otp_storage = {}

def otp_login(request):
    if request.method == 'POST':
        email = request.POST['email']

        if not email:
            messages.success(request, "Email is required")
            return redirect('otp_login')


        student = Student.objects.filter(email=email).first()
        if student:
            # Set the student ID in the session to keep the student logged in
            otp = random.randint(100000, 999999)  # Generate 6-digit OTP
            otp_storage[email] = otp  # Store OTP temporarily

            # Send OTP email
            subject = "Your OTP for Login"
            message = f" Breast Cancer Detection \n Your OTP is {otp}. Please use this to log in. \n OTP is valid for 10 minutes only."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "OTP sent successfully")

            global otp_time
            otp_time = time.time()  # Store the time when OTP is generated
            return redirect('check_mail')

        messages.error(request, "Email is not registered")
        return redirect('otp_login')

    return render(request,'otp_login.html')


def check_mail(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        current_time = time.time()

        if not email or not otp:
            messages.error(request, "Email and OTP are required")

        if current_time - otp_time > 600:  # 60 seconds = 1 minutes .......... 600 seconds = 10 minutes
            messages.error(request, "OTP has expired. Please request a new one.")
            return redirect('otp_login')

        elif email in otp_storage and otp_storage[email] == int(otp):
            student = Student.objects.filter(email=email).first()
            request.session['student_id'] = student.id

            del otp_storage[email]  # Remove OTP after successful login

            messages.success(request, "Logged in Successfully")
            return redirect('home')

        messages.error(request, "Invalid OTP")
        return redirect('check_mail')

    return render(request,'check_mail.html')


















def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if not email:
            messages.success(request, "Email is required")
            return redirect('otp_login')

        student = Student.objects.filter(email=email).first()
        if student:
            # Set the student ID in the session to keep the student logged in
            otp = random.randint(100000, 999999)  # Generate 6-digit OTP
            otp_storage[email] = otp  # Store OTP temporarily

            # Send OTP email
            subject = "Your OTP for Reset password"
            message = f" Breast Cancer Detection \n Your OTP is {otp}. Please use this to reset your password.\nOTP is valid for 5 minutes only."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "OTP sent successfully")

            global otp_time_new
            otp_time_new = time.time()  # Store the time when OTP is generated
            return redirect('verify_reset_otp')

        messages.error(request, "Email is not registered")
        return redirect('forget_password')

    return render(request,'forget_password.html')

def verify_reset_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        current_time = time.time()

        if not email or not otp:
            messages.error(request, "Email and OTP are required")

        if current_time - otp_time_new > 300:  # 60 seconds = 1 minutes .......... 300 seconds = 5 minutes
            messages.error(request, "OTP has expired. Please request a new one.")
            return redirect('forget_password')

        elif email in otp_storage and otp_storage[email] == int(otp):

            del otp_storage[email]  # Remove OTP after successful login
            messages.success(request, "OTP Verified Successfully")
            return redirect('update_password')

        messages.error(request, "Invalid OTP")
        return redirect('verify_reset_otp')

    return render(request,"verify_reset_otp.html")


def update_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        pass_1 = request.POST.get("pass_new")
        pass_2 = request.POST.get("pass1")

        if not email or not pass_1 or not pass_2:
            messages.error(request, "Fill all the details")
            return redirect('update_password')

        if pass_1 != pass_2:
            messages.error(request, "Both passwords did not match")
            return redirect('update_password')

        # Get student instance
        student = Student.objects.filter(email=email).first()
        if not student:
            messages.error(request, "No student found with this email")
            return redirect('update_password')

        if student:
            student.pass1 = pass_1  # Assign the new password value
            student.save()

        messages.success(request, "Password updated successfully")
        return redirect('login')

    return render(request, 'update_password.html')

def logoutuser(request):
    request.session.flush()  # Ends the session and clears all session data
    messages.success(request, "Successfully logged out!")
    return redirect('index')  # Redirects to the URL named 'index'


def home(request):
    student_id = request.session['student_id']
    user = Student.objects.get(id=student_id)
    fname = user.fname
    return render(request,'home.html',{"fname":fname.capitalize()})


def users(request):
    obj = Student.objects.all()
    context = {
        'obj':obj
    }
    return render(request,'users.html',context)

def predict(request):
    if request.method == "POST":
        model = pickle.load(open('dataset/xgb_classifier2.pkl','rb'))

        input_features = [
            float(request.POST.get("mean_radius")),
            float(request.POST.get("mean_texture")),
            float(request.POST.get("mean_perimeter")),
            float(request.POST.get("mean_area")),
            float(request.POST.get("mean_smoothness")),
            float(request.POST.get("mean_compactness")),
            float(request.POST.get("mean_concavity")),
            float(request.POST.get("mean_concave_points")),
            float(request.POST.get("mean_symmetry")),
            float(request.POST.get("mean_fractal_dimension")),
            float(request.POST.get("radius_error")),
            float(request.POST.get("texture_error")),
            float(request.POST.get("perimeter_error")),
            float(request.POST.get("area_error")),
            float(request.POST.get("smoothness_error")),
            float(request.POST.get("compactness_error")),
            float(request.POST.get("concavity_error")),
            float(request.POST.get("concave_points_error")),
            float(request.POST.get("symmetry_error")),
            float(request.POST.get("fractal_dimension_error")),
            float(request.POST.get("worst_radius")),
            float(request.POST.get("worst_texture")),
            float(request.POST.get("worst_perimeter")),
            float(request.POST.get("worst_area")),
            float(request.POST.get("worst_smoothness")),
            float(request.POST.get("worst_compactness")),
            float(request.POST.get("worst_concavity")),
            float(request.POST.get("worst_concave_points")),
            float(request.POST.get("worst_symmetry")),
            float(request.POST.get("worst_fractal_dimension"))

        ]
        features_value = [np.array(input_features)]

        features_name = ['mean radius', 'mean texture', 'mean perimeter', 'mean area',
                         'mean smoothness', 'mean compactness', 'mean concavity',
                         'mean concave points', 'mean symmetry', 'mean fractal dimension',
                         'radius error', 'texture error', 'perimeter error', 'area error',
                         'smoothness error', 'compactness error', 'concavity error',
                         'concave points error', 'symmetry error', 'fractal dimension error',
                         'worst radius', 'worst texture', 'worst perimeter', 'worst area',
                         'worst smoothness', 'worst compactness', 'worst concavity',
                         'worst concave points', 'worst symmetry', 'worst fractal dimension']

        df = pd.DataFrame(features_value, columns=features_name)
        output = model.predict(df)

        if output == 0:
            # res_val = "** breast cancer **"
            return redirect('yes')
        else:
            return redirect('no')

    return render(request, 'predict.html')

def yes(request):
    return render(request,'yes.html')

def no(request):
    return render(request,'no.html')