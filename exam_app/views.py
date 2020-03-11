from django.shortcuts import render, redirect
from .models import User, Job
from django.contrib import messages
import bcrypt

def route(request):
    return render(request, 'index.html')
    
def create_user(request):
    errors= User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    password=request.POST['password']
    pw_hash= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    messages.info(request, 'You have successfully registered--go ahead and log in')


    new_user=User.objects.create(first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'], password=pw_hash)
    return redirect ('/')

def validate_login(request):
    print(request.POST)
    users=User.objects.filter(email=request.POST['email'])
    if len(User.objects.filter(email=request.POST['email']))!=1:
        messages.error(request, 'invalid email address or password')
        return redirect('/')

    user = users[0]
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request,'invalid email address or password.')
        return redirect('/')
    
    else:
        request.session['user_id']=user.id  #where do these session brackets come from?
        request.session['user_email']= user.email
        request.session['user_firstname']= user.first_name
        request.session['user_lastname']=user.last_name
        return redirect('/success')
    return redirect('/')




def logout(request):
    request.session.clear()
    messages.info(request, 'You have logged out')

    return redirect('/')
   

def success(request):
    if not "user_id" in request.session:
        messages.error(request, "na-ah, you gotta log in, sunny")
        return redirect('/')

    context= {
        'alljobs': Job.objects.all()
    }
    return render(request, 'dashboard.html', context)


def new_job(request):

    return render(request,'addjob.html' )

def create_job(request):
    #vali
    errors=Job.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/newjob')

    else:
        this_user=User.objects.get(id=request.session['user_id'])
        new_job=Job.objects.create(title=request.POST['title'], description=request.POST['description'], location=request.POST['location'], user=this_user)
        print(request.POST)

    return redirect('/success')

def view_job(request, job_id):

    context={
        "jobtoshow":Job.objects.get(id=job_id)
    }

    return render(request, 'showjob.html', context)

def remove_job(request, job_id):
    job_to_remove=Job.objects.get(id=job_id)
    job_to_remove.delete()
    return redirect('/success')

def edit_job(request, job_id):
    context={
        "job": Job.objects.get(id=job_id),
        "jobtoshow":Job.objects.get(id=job_id)
    }
    
    return render(request, 'editshow.html', context)


def update_job(request, job_id):
    errors=Job.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/editjob/{job_id}')
    else:
        job_to_update=Job.objects.get(id=job_id)
        job_to_update.title=request.POST['title']
        job_to_update.description=request.POST['description']
        job_to_update.location=request.POST['location']
        job_to_update.save()

    return redirect('/success')


def add_personaljob(request, job_id):
    
    
    job_to_add = Job.objects.get(id=job_id)
    job_to_add.assigned=User.objects.get(id=request.session['user_id'])
    job_to_add.save()
   
    context ={
        "jobs_to_add": Job.objects.filter(assigned=request.session['user_firstname'])
    } 
    
    return render(request, 'dashboard.html', context)
    