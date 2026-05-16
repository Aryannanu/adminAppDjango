from email.policy import default
import hashlib
from random import choice, choices
from tkinter import CASCADE
from django.db import models
from ckeditor.fields import RichTextField


class AppUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=32) 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    job_post = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_admin = models.BooleanField(default=True)
    

    def set_password(self, raw_password: str) -> None:
        
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str) -> bool:

        hashed = hashlib.md5(raw_password.encode()).hexdigest()

        if self.password == hashed:
            return True

        if self.password == raw_password:
            self.password = hashed
            self.save(update_fields=['password'])
            return True

        return False

    def __str__(self):
        return self.username
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True)
    price =  models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(help_text="Estimated time")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class Project(models.Model):
    name = models.CharField(max_length=100)       
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    assigned_to = models.ForeignKey(
        AppUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects"
    )
    status = models.CharField(
        max_length=100,
        choices=[
            ('pending','pending'),
            ('active','active'),
            ('completed','completed')
        ],
        default='pending'
                              )
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Permission(models.Model):
       granted_to = models.ForeignKey(
           AppUser,
           on_delete=models.CASCADE,
           related_name="permissions",
           null=True,
           blank=True  
       )
       project_permission = models.ForeignKey(
           Project,
            on_delete=models.CASCADE,
            related_name="permissions",
            null=True,
            blank=True
       )
       can_view = models.BooleanField(default=False)
       can_edit = models.BooleanField(default=False)
       can_delete = models.BooleanField(default=False)
       created_at = models.DateTimeField(auto_now_add=True)
       
    
    


