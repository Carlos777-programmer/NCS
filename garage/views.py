from django.shortcuts import get_object_or_404, redirect, render
from .models import Project
from .forms import ProjectForm

def projects_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'garage/projects_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        Project.objects.create(
            title=title,
            category=category,
            description=description,
            image=image
        )
        return redirect('projects_list')
    
    return render(request, 'garage/project_form.html')

from django.http import JsonResponse

def api_projects_list(request):
    data = list(Project.objects.values('id', 'title', 'category', 'description', 'image', 'created_at'))
    return JsonResponse(data, safe=False)

def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects_list') 
    else:
        form = ProjectForm(instance=project)
        
    return render(request, 'garage/project_form.html', {'form': form, 'project': project})

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('projects_list')
        
    return render(request, 'projects/project_confirm_delete.html', {'project': project})