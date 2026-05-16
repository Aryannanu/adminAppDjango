from django.contrib import admin
from .models import AppUser, Permission,Service,Project

admin.site.register(AppUser)
admin.site.register(Service)
admin.site.register(Project)
admin.site.register(Permission)


# Register your models here.
