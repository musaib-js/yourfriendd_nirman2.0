from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.views.generic import TemplateView
from .decorators import patient_required, consultant_required
from .forms import PatientSignUpForm, ConsultantSignUpForm, PatientForm, ConsultantForm
from .models import Patient, Subscription_Packs, User ,Subscribed_Users, Consultant
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from home.forms import AppointmentForm
from home.models import Appointment,SelfCare

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
            return redirect('/')
    return render(request, 'login.html')

#Handles the logout
def logout(request):
    auth_logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

#Subscription
def subscribe(request, name):
    user  = request.user
    pack = Subscription_Packs.objects.get(name = name)
    newsubscribeduser = Subscribed_Users(user = user, subscription_type = pack)
    print(newsubscribeduser)
    newsubscribeduser.save()
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
            appointment = Appointment.objects.filter(doctor = consultant)
            context = {'consultant':consultant, 'appointment':appointment}
            return render(request, 'doctordashboard.html', context)
        return redirect('/')

#Handles the appointment booking --done
def bookappointment(request, pk):
    user = request.user
    doctor = Consultant.objects.get(pk = pk)
    try:
        sub_user = Subscribed_Users.objects.get(user = user)
        if sub_user:
            if request.method == "POST":
                name = request.POST['name']
                age = request.POST['age']
                date = request.POST['date'].isoformat()
                newAppointment = Appointment(patient = request.user, doctor = doctor, name = name, age = age, date = date, meet_link = "Not Approved")
                newAppointment.save()
                messages.success(request, "Appointment booked succesfully. Wait for the doctor to approve.")
                return redirect('/')
            else:
                 messages.error(request, "Fill the form correctly")
                 context = {'doctor':doctor}
            return render(request, 'bookappointment.html', context) 
    except:
        print("not subscribed")
        return redirect('/')

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

def selectsubscription(request):
    subscription = Subscription_Packs.objects.all()
    context = {'subscription': subscription}
    return render(request, 'subscriptions.html', context)

def myappointments(request):
    user = request.user
    print(user)
    patient = Patient.objects.filter(user = user).first()
    print(patient)
    name = patient.name
    userappointments = Appointment.objects.filter(name = name)
    context = {'userapp': userappointments}
    return render(request, 'myappointments.html', context)


# class ConsultantSignUpView(CreateView):
#     model = User
#     form_class = ConsultantSignUpForm
#     template_name = 'doctorsignup.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'consultant'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         auth_login(self.request, user)
#         return redirect('/auth/consultantprofile')

# class SignUpView(TemplateView):
#     template_name = 'signup.html'

# class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'patientsignup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('/auth/patientprofile')
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
