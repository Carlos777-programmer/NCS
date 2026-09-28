from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Project, ProjectMedia, Category, VehicleType
from .forms import ProjectForm

def projects_list(request):
    projects = Project.objects.prefetch_related('media_files', 'category', 'vehicle_type').all().order_by('-created_at')
    categories = Category.objects.all()
    vehicle_types = VehicleType.objects.all()
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        projects = projects.filter(category_id=categoria_id)

    vehicle_type_id = request.GET.get('vehicle_type')
    if vehicle_type_id:
        projects = projects.filter(vehicle_type_id=vehicle_type_id)

    context = {
        'projects': projects,
        'categories': categories,
        'vehicle_types': vehicle_types,
        'categoria_selecionada': categoria_id,
        'vehicle_type_selecionado': vehicle_type_id,
    }
    return render(request, 'garage/projects_list.html', context)

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            files = request.FILES.getlist('media_files')
            for f in files:
                ProjectMedia.objects.create(project=project, file=f)
            return redirect('projects_list')
    else:
        form = ProjectForm()
    
    categories = Category.objects.all()
    vehicle_types = VehicleType.objects.all()
    return render(request, 'garage/project_form.html', {'form': form, 'categories': categories, 'vehicle_types': vehicle_types})

def api_projects_list(request):
    projects = Project.objects.prefetch_related('media_files', 'category', 'vehicle_type').all().order_by('-created_at')
    data = []
    for p in projects:
        media_urls = [request.build_absolute_uri(m.file.url) for m in p.media_files.all()]
        category_name = p.category.name if p.category else None
        vehicle_type_name = p.vehicle_type.name if p.vehicle_type else None
        
        data.append({
            'id': p.id,
            'title': p.title,
            'category': category_name,
            'vehicle_type': vehicle_type_name,
            'description': p.description,
            'media': media_urls,
            'created_at': p.created_at.isoformat()
        })
    return JsonResponse(data, safe=False)

def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            files = request.FILES.getlist('media_files')
            for f in files:
                ProjectMedia.objects.create(project=project, file=f)
            return redirect('projects_list') 
    else:
        form = ProjectForm(instance=project)
        
    categories = Category.objects.all()
    vehicle_types = VehicleType.objects.all()
    return render(request, 'garage/project_form.html', {'form': form, 'project': project, 'categories': categories, 'vehicle_types': vehicle_types})

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects_list')
    return render(request, 'garage/project_confirm_delete.html', {'project': project})