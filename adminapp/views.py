from django.contrib import messages

from django.conf import os, settings
from django.shortcuts import redirect, render, HttpResponse
from .models import AppUser, Permission , Project , Service
import hashlib
import os
from .permissions import admin_required
from .jwt_utils import generate_jwt


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import AppUser, Project, Service
from .jwt_utils import generate_jwt
from .permissions import admin_required
import hashlib



def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = AppUser.objects.get(username=username, is_active=True, is_admin=True)
            if user.check_password(password):
                token = generate_jwt(user)
                response = redirect('dashboard')
                response.set_cookie(
                    'jwt_token',
                    token,
                    httponly=True,
                    samesite='Lax',
                    path='/'
                )
                return response
            error = "Invalid credentials"
        except AppUser.DoesNotExist:
            error = "Invalid credentials"

    return render(request, 'login.html', {'error': error})




@admin_required
def logout_view(request):
    response = redirect('login_view')
    response.delete_cookie('jwt_token')
    return response



@admin_required
def dashboard(request):
    current_user = request.current_user
    users = AppUser.objects.all()
    services = Service.objects.all()
    projects = Project.objects.select_related('service', 'assigned_to')

    return render(request, 'dashboard.html', {
        'current_user': current_user,
        'users': users,
        'services': services,
        'projects': projects,
    })






@admin_required
def accounts(request):
    current_user = request.current_user
    users = AppUser.objects.all()
    return render(request, 'accounts.html', {
        'current_user': current_user,
        'users': users
    })

@admin_required
def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})



    
    
@admin_required
def projects(request):
    projects = Project.objects.select_related('service', 'assigned_to')
    return render(request, 'projects.html', {'projects': projects})

@admin_required
def service_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration_days = request.POST.get('duration_days')
        
        service = Service.objects.create(
            name = name,
            description = description,
            price = price,
            duration_days = duration_days,
        )
        messages.success(request, "Form submitted successfully!")
        return redirect('service_form')
        
    return render(request, 'service_form.html')

@admin_required
def projects_form(request):
    services =  Service.objects.all()
    users = AppUser.objects.filter(is_active=True)
    if request.method == "POST":
        name = request.POST.get('name')
        service_id = request.POST.get('service')
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status')
        image = request.FILES.get('image')
        service = Service.objects.get(id=service_id)
        assigned_to = (
            AppUser.objects.get(id=assigned_to_id)
            if assigned_to_id else None
        )
        
        project = Project.objects.create(
            name = name,
            service = service,
            assigned_to = assigned_to,
            status = status,
            image=image
        )
        messages.success(request, "Form submitted successfully!")
        
        return redirect('projects_form')
        
    return render(request, 'project_form.html', {
        'services':services,
        'users':users
    })

@admin_required
def user_form(request):
    return render(request, 'user_form.html')

@admin_required
def project_edit(request, pk):
    project = Project.objects.get(id=pk)
    users = AppUser.objects.filter(is_active=True)

    if request.method == "POST":
        project.name = request.POST.get('name')
        project.status = request.POST.get('status')
        project.assigned_to = AppUser.objects.get(id=request.POST.get('assigned_to')) if request.POST.get('assigned_to') else None
        project.image = request.FILES.get('image') if 'image' in request.FILES else project.image
        project.save()
        messages.success(request, "Project updated successfully!")
        return redirect('project_edit', pk=project.id)

    return render(request, 'project_edit.html', {'project': project, 'users': users})

@admin_required
def project_delete(request, pk):
    project = Project.objects.get(id=pk)
    project.delete()
    return redirect('dashboard')

@admin_required
def user_update(request):
    user_id = request.session.get('app_user_id') 
    if not user_id:
        return redirect('login_view')

    user = AppUser.objects.get(id=user_id)

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.job_post = request.POST.get('job_post')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')

        if 'image' in request.FILES:
            user.image = request.FILES['image']

        user.save()
        messages.success(request, "User updated successfully!")
        return redirect('dashboard')

    return render(request, 'user_update.html', {'user': user})

@admin_required
def service_edit(request, pk):
    service = Service.objects.get(id=pk)
    users = AppUser.objects.filter(is_active=True)


    if request.method == "POST":
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.duration_days = request.POST.get('duration_days')
        service.save()
        
        return redirect('services')

    return render(request, 'service_edit.html', {'service': service, 'users': users})

@admin_required
def user_delete(request):
    user_id = request.session.get('app_user_id')
    user = AppUser.objects.get(id=user_id)
    user.delete()
    return redirect('login_view')    

@admin_required
def service_delete(request, pk):    
    service = Service.objects.get(id=pk)
    service.delete()
    return redirect('services')

@admin_required
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        image = request.FILES.get("image")
        job_post = request.POST.get("job_post")
        address = request.POST.get("address")

        if AppUser.objects.filter(username=username).exists():
            return render(request, "user_form.html", {
                "error": "Username already exists"
            })

        user = AppUser(
            username=username,
            email=email,
            phone=phone,
            image=image,
            job_post=job_post,
            address=address,
            is_active=True
        )

        user.set_password(password)  
        user.save()                  
        messages.success(request, "User created successfully!")
        return redirect("user_form")

    return render(request, "user_form.html")

       
def project_post(request):
    projects = Project.objects.select_related('service','assigned_to')
    
    return render(request,'project_post.html',{'projects':projects})


def project_all(request, pk):
    project = Project.objects.select_related(
        'service', 'assigned_to'
    ).get(id=pk)

    return render(request, 'project_all.html', {
        'project': project
    })


def project_pagess(request):
    projects = Project.objects.all()
    
    return render(request,'public/project_pageview.html',{'projects':projects})

def project_alldetails(request, pk):
    project = Project.objects.select_related('service', 'assigned_to').get(id=pk)
    
    return render(request, 'public/project_alldetails.html',{'project':project})
    

def save_user(username, password):
    hashed = hashlib.md5(password.encode()).hexdigest()

    base_dir = os.path.dirname(__file__)  
    file_path = os.path.join(base_dir, "user.txt")

    with open(file_path, "a") as file:
        file.write(f"{username},{hashed}\n")


@admin_required
def permissions(request):    
    return render(request, 'permission.html')
    
        
@admin_required 
def assign_permissions(request):    
    users = AppUser.objects.filter(is_active=True)
    projects = Project.objects.all()

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        project_id = request.POST.get('project_id')

        can_view = request.POST.get('can_view') == 'on'
        can_edit = request.POST.get('can_edit') == 'on'
        can_delete = request.POST.get('can_delete') == 'on'

        user = AppUser.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)

        Permission.objects.create(
            granted_to=user,
            project_permission=project,
            can_view=can_view,
            can_edit=can_edit,
            can_delete=can_delete
        )

        messages.success(request, "Permissions assigned successfully!")
        return redirect('assign_permissions')

    return render(request, 'permission_assign.html', {
        'users': users,
        'projects': projects
    })
            