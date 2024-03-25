from django.contrib import admin
from project.models import Project,Category,Tag,Picture,Rate,Donation

# Register your models here.

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Picture)
admin.site.register(Donation)
admin.site.register(Rate)