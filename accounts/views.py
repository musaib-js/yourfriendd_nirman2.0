from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import PatientSignUpForm, ConsultantSignUpForm, PatientForm, ConsultantForm
from .models import Patient, Subscription_Packs, User ,Subscribed_Users, Consultant
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from home.forms import AppointmentForm
from home.models import Appointment,SelfCare, Post

# Handles the Patient Signup
def handleSignup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]

        if password != cpassword:
            messages.error(request, "Passwords don't match")
            return redirect('/auth/accounts/signup')
        else:
            newuser = User.objects.create_user(username = username, password = password, is_patient = True)
            newuser.save()
            auth_login(request, newuser)
            messages.success(request, "Patient Account Created Successfully")
            return redirect('/auth/patientprofile')

    return render(request, "signup.html")

# Handles the patient's profile creation
def createProfile(request):
    if request.method == "POST":
        name = request.POST['name']
        gender = request.POST['gender']
        age = request.POST['age']
        history = request.POST['history']
        newProfile = Patient.objects.create(user = request.user, name = name, gender = gender, age =  age, history = history)
        newProfile.save()
        messages.success(request, "Your Profile Has Been Created Successfully")
        return redirect('/auth/selectsubscription')
    return render(request, 'patientprofile.html')

#Handles the login
def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            if user.is_patient:
                return redirect('/')
            elif user.is_consultant:
                return redirect('/auth/doctordashboard')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/auth/login')
    return render(request, 'login.html')

#Handles the logout
def logout(request):
    auth_logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

#Subscription
def subscribe(request, pk):
    user  = request.user
    pack = Subscription_Packs.objects.get(pk=pk)
    newsubscribeduser = Subscribed_Users(user = user, subscription_type = pack)
    print(newsubscribeduser)
    try:
        newsubscribeduser.save()
    except Exception as e:
        print(e)
    messages.success(request, "You've succesfully subscribed")
    return redirect('/')

#Handles the patient profile update (Pending)
def patientupdate(request):
    user = request.user
    profile = Patient.objects.filter(user = user).first()
    userlogged = Patient.objects.filter(user = user).first()
    form = PatientForm(request.POST, instance = userlogged) 
    context = {'profile':profile, 'form':form}
    if form.is_valid():  
        form.save()  
        messages.success(request, "Details Updated Successfully")
        return redirect('/auth/selectsubscription')  
    else:
         messages.error(request, "Fill the form correctly")
    return render(request, 'patientprofile.html', context)  

#Handles the consultant update
def consultantupdate(request):
    user = request.user
    profile = Consultant.objects.filter(user = user).first()
    userlogged = Consultant.objects.filter(user = user).first()
    form = ConsultantForm(request.POST, instance = userlogged) 
    context = {'profile':profile, 'form':form} 
    if form.is_valid():  
        form.save()  
        messages.success(request, "Details Updated Successfully")
        return redirect('/auth/doctordashboard')  
    else:
         messages.error(request, "Fill the form correctly")
    return render(request, 'consultantprofile.html', context)  

#Handles the doctor dashboard -- Done
@login_required
def doctordashboard(request):
    if request.user.is_authenticated:
        if request.user.is_consultant:
            consultant = Consultant.objects.filter(user = request.user).first()
            appointment = Appointment.objects.filter(doctor = consultant.user)
            context = {'consultant':consultant, 'appointment':appointment}
            return render(request, 'doctordashboard.html', context)
        return redirect('/')

#Handles the appointment booking --done
def bookappointment(request, pk):
    user = request.user
    doctor = Consultant.objects.get(pk = pk)
    try:
        sub_user = Subscribed_Users.objects.get(user = user)
        context = {'doctor':doctor}
        if sub_user:
            if request.method == "POST":
                name = request.POST['name']
                age = request.POST['age']
                date = request.POST['date']
                newAppointment = Appointment(patient = user, doctor = doctor.user, name = name, age = age, date = date, meet_link = "Not Approved")
                print(newAppointment)
                newAppointment.save()
                messages.success(request, "Appointment booked succesfully. Wait for the doctor to approve.")
                return redirect('/')
            else:
                return render(request, 'appointment.html', context) 
    except Exception as e:
        print(e)
        messages.success(request, "Please subscribe to any of our packs")
        return redirect('/auth/selectsubscription/')

#View to fetch the doctors
def doctors(request):
    consultant = Consultant.objects.all()
    context = {'consultant':consultant}
    return render(request, 'doctors.html', context)

#Fetches the profile of a specific doctor
def doctorr(request, pk):
    doctor = Consultant.objects.filter(pk = pk).first()
    selfcare_techniques = SelfCare.objects.filter(posted_by=doctor.user)
    context = {'doctor':doctor,'techniques':selfcare_techniques}
    return render(request, 'doctor.html', context)

def meditation(request):
    return render(request, 'meditation.html')
    
def coping(request):
    return render(request, 'coping.html')

@login_required
def selectsubscription(request):
    subscription = Subscription_Packs.objects.all()
    context = {'subscription': subscription}
    return render(request, 'subscriptions.html', context)

@login_required
def myappointments(request):
    userappointments = Appointment.objects.filter(patient = request.user)
    context = {'appointment': userappointments}
    return render(request, 'myappointments.html', context)

@login_required
def selfCare(request):
    if request.method == 'POST':
        name=request.POST['name']
        files=request.FILES['file']
        description=request.POST['description']
        selfcare = SelfCare(name=name,posted_by=request.user,file=files,description=description)
        selfcare.save()
        return redirect('/selfcare/')
    elif request.method =='GET':
        selfcare_techniques = SelfCare.objects.all()
        context={'techniques':selfcare_techniques}
        return render(request,'selfcare.html',context)

def AppointmentApproved(request,pk):
    if request.method == "POST":
        meet_link = request.POST['meet_link']
        appointment = Appointment.objects.get(pk = pk)
        appointment.approved = True
        appointment.meet_link = meet_link
        appointment.save()
        messages.success(request,"Successfully Approved")
        return redirect('/auth/doctordashboard')


def postBlog(request):
    if request.method == "POST":
        title = request.POST['title']
        body = request.POST['body']
        slug = request.POST['slug']
        tags = request.POST['tags']

        newPost = Post(title = title, body = body, slug =slug, tags = tags, author = request.user)
        newPost.save()
        messages.success(request, "Posted Successfully")
        return redirect('/auth/doctordashboard')

