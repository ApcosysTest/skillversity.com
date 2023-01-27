from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, logout, login as auth_login, update_session_auth_hash
from .helper import send_forget_password_mail
import uuid
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def is_customer(user):
    return user.groups.filter(name='Customer').exists()

# Index page 
def index(request):
    bundle = Bundle.objects.all()
    bundle1 = Bundle.objects.all()[:2]
    bundle2 = Bundle.objects.all()[2:]
    context = {'bundle':bundle, 'bundle1':bundle1, 'bundle2':bundle2}
    return render(request, 'index.html', context)

# About Page 
def about(request):
    bundle = Bundle.objects.all()
    context = {'bundle':bundle}
    return render(request, 'about.html', context)

# Register page 
def register(request):
    if request.method == 'POST':
        form1=RegisterUserForm(request.POST)
        form2=RegisterExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_user_group=Group.objects.get_or_create(name='Customer')
            my_user_group[0].user_set.add(user)

            return redirect('registerSuccess')
    else:
        form1=RegisterUserForm()
        form2=RegisterExtraForm()

    context={
        'form1':form1,
        'form2':form2
    }
    return render(request, 'register.html', context)

# Login Page 
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='Customer'):
                    auth_login(request,user)
                    return redirect('index')
                else:
                    messages.success(request, 'Your account is not found')
            else:
                messages.success(request, 'Check your username and password')
    else:
         form = LoginForm()

    context ={
        'form':form
    }
    return render(request, 'login.html', context)

# Logout function 
def logout_view(request):
    logout(request)
    return redirect('/')

# Forget Password page 
def forgotPassword(request):
    try:
        if request.method == 'POST':
            form = ForgotpassForm(request.POST)
            email = request.POST.get('email')
            if not Register.objects.filter(email=email).first():
                messages.success(request, 'No user found with this Email.')
                return redirect('forgetPassword')
            else:
                token = str(uuid.uuid4())
                profile_object = Register.objects.get(email = email)
                profile_object.forgot_password_token = token
                profile_object.save()
                host =  request.META['HTTP_HOST']
                send_forget_password_mail(email, token, host)
                return redirect('sendForgotpass')

    except Exception as e:
        print(e)
    form = ForgotpassForm()
    return render(request,'forgotPassword.html',{'form':form}) 

# Reset Password
def resetPassword(request, token):
    try:
        profile_object = Register.objects.get(forgot_password_token = token)
        context = {'user_id': profile_object.user.id}
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_pass')
            user_id = profile_object.user.id

            if user_id is None:
                messages.success(request, "No user Found")
                return redirect(f'/resetPassword/{token}/')

            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            
            if profile_object.forgot_password_token is not None:
                profile_object.forgot_password_token = None
                profile_object.save()
            return redirect('Success')
            
    except Exception:
        return redirect('invalidLink')
    return render(request, 'resetPassword.html', context)

def sendForgotpass(request):
    return render(request, 'sendForgotpass.html')

# Success Page after Change password
def Success(request):
    return render(request, 'Success.html')  

def invalidLink(request):
    return render(request, 'invalidLink.html')

# Gallery page 
def gallery(request):
    bundle = Bundle.objects.all()
    context = {'bundle':bundle}
    return render(request, 'gallery.html', context)

# Instructor page
def instructor(request):
    bundle = Bundle.objects.all()
    if request.method == "POST":  
        form = InstructorForm(request.POST)  
        if form.is_valid():
            
            # --------------------------------------contact us ---------------------------------------
            subject = "Instructor Inquiry" 
            Name = form.cleaned_data.get('Name')
            Email = form.cleaned_data.get('Email')
            Contact = form.cleaned_data.get('Contact')
            textarea = form.cleaned_data.get('textarea')
            
            data = form.save()
            data.save()

            send_mail(subject,f'Name:{Name}\n\nEmail :{Email}\n\nContact:{Contact}\n\ntextarea:{textarea}','noreply@sversity.com', ['noreply@sversity.com'],fail_silently=False)
           
            messages.success(request, "Mail Sent .." )
            return redirect ("/instructor")
        
        else:
            messages.success(request, "Mail Not Sent .." )
            return render(request,"base.html")
          
    else:  
        form = InstructorForm()  
    
    context ={'bundle':bundle, 'form':form}
    return render(request,'instructor.html',context) 

# Regiter success redirect Page 
def registerSuccess(request):
    return render(request, 'registerSuccess.html')

# Contact us 
def contact(request):
    if request.method == "POST":  
        Email = request.session.get('Email')
        form = ContactusForm(request.POST)  
        if form.is_valid():
            subject = "Website Inquiry" 
            Name = form.cleaned_data.get('Name')
            Email = form.cleaned_data.get('Email')
            Contact = form.cleaned_data.get('Contact')
            textarea = form.cleaned_data.get('textarea')
            send_mail(subject,f'Name:{Name}\n\nEmail :{Email}\n\nContact:{Contact}\n\ntextarea:{textarea}','noreply@sversity.com', ['noreply@sversity.com'],fail_silently=False)
            messages.success(request, "Mail Sent .." )
            return redirect ("contactSuccess")
        
        else:
            messages.success(request, "Mail Not Sent .." )
            return render(request,"index.html")

    else:  
        form = ContactusForm()  
    return render(request,'index.html',{'form':form}) 

# Contact send request page 
def contactSuccess(request):
    return render(request, 'contactSuccess.html')

# Course Detail Page 
def courseDetail(request, id):
    bundle = Bundle.objects.all()
    bundle_head = Bundle.objects.get(id=id)
    silver = Course.objects.filter(category__name='Silver',bundle_id=id).order_by('name')
    gold = Course.objects.filter(category__name='Gold',bundle_id=id).order_by('name')
    context = {'bundle':bundle, 'bundle_head':bundle_head, 'silver':silver, 'gold':gold}
    return render(request, 'courseDetail.html', context)

def standAlone(request):
    bundle = Bundle.objects.all()
    silver = Course.objects.filter(category__name='Silver', standalone='Yes').order_by('name')
    gold = Course.objects.filter(category__name='Gold', standalone='Yes').order_by('name')

    context = {'bundle':bundle, 'silver':silver, 'gold':gold}
    return render(request, 'standAlone.html', context)

# Investor Page 
def investor(request):
    bundle = Bundle.objects.all()
    if request.method == "POST":  
        form = InvestorsForm(request.POST)  
        if form.is_valid():
            
            # --------------------------------------contact us ---------------------------------------
            subject = "Inverstors Inquiry" 
            Name = form.cleaned_data.get('Name')
            Email = form.cleaned_data.get('Email')
            Contact = form.cleaned_data.get('Contact')

            send_mail(subject,f'Name:{Name}\n\nEmail :{Email}\n\nContact:{Contact}','noreply@sversity.com', ['noreply@sversity.com'],fail_silently=False)
            messages.success(request, "Mail Sent .." )
            return redirect ("/investor")
        
        else:
            messages.success(request, "Mail Not Sent .." )
            return render(request,"base.html")
          
    else:  
        form = InvestorsForm()  
    context={'bundle':bundle, 'form':form}
    return render(request,'investor.html',context)

#change password
@login_required(login_url='login')
@user_passes_test(is_customer)
def changePassword(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('index')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = MyPasswordChangeForm(request.user)
    return render(request, 'changePassword.html', {'form': form})
