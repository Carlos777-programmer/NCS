from django.contrib import admin
from .models import Category, VehicleType, Project, ProjectMedia, QuoteSubmission

admin.site.register(Category)
admin.site.register(VehicleType)
admin.site.register(Project)
admin.site.register(ProjectMedia)
admin.site.register(QuoteSubmission)