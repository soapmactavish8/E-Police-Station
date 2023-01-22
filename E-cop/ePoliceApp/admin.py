from django.contrib import admin
from .models import *
from .views import app_info
from .cities import cities

class SuperAdmin(admin.ModelAdmin):
    admin.site.site_header = admin.site.site_title = app_info['app_name']
    admin.site.index_title = f"{app_info['app_name']}'s Admin"
    list_per_page = 10
    ordering = ['id']

# auto creating roles table
class AutoCreate:
    def __init__(self):
        roles = ['citizen', 'department', 'police']
        if not len(Role.objects.all()):
            for role in roles:
                Role.objects.create(Role=role)
                
        # auto creating State and table records
        if not len(State.objects.all()):
            state = State.objects.create(Name='gujarat')

            if not len(City.objects.all()):
                for city in cities:
                    City.objects.create(State=state, Name=city)

        models_list = [Chowki, Role, Department, Citizen, State, City, Complaint, CrimeList, SuspectList, Inspector, Master, PolicePerson, Station, SubInspector]

        for model in models_list:
            admin.site.register(model, SuperAdmin)

init = AutoCreate()