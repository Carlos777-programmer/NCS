from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class QuoteSubmission(models.Model):
    vehicle = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    services = models.JSONField(default=dict, blank=True, null=True)
    total_estimated = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle} - R$ {self.total_estimated}"
    
class ProjectMedia(models.Model):
    project = models.ForeignKey('Project', related_name='media_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='projects/media/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mídia de {self.project.title}"