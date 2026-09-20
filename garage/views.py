from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Project, ProjectMedia  # Importamos o modelo ProjectMedia
from .forms import ProjectForm

def projects_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'garage/projects_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            
            # Captura e salva múltiplos arquivos de uma vez (fotos e vídeos)
            files = request.FILES.getlist('media_files')
            for f in files:
                ProjectMedia.objects.create(project=project, file=f)
                
            return redirect('projects_list')
    else:
        form = ProjectForm()
    
    return render(request, 'garage/project_form.html', {'form': form})

def api_projects_list(request):
    # Otimizamos a consulta usando prefetch_related para puxar as mídias junto
    projects = Project.objects.prefetch_related('media_files').all().order_by('-created_at')
    data = []
    for p in projects:
        # Cria uma lista contendo as URLs absolutas de todas as fotos/vídeos deste projeto
        media_urls = [request.build_absolute_uri(m.file.url) for m in p.media_files.all()]
        
        data.append({
            'id': p.id,
            'title': p.title,
            'category': p.category,
            'description': p.description,
            'media': media_urls,  # Retorna a lista completa de mídias
            'created_at': p.created_at.isoformat()
        })
    return JsonResponse(data, safe=False)

def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            
            # Adiciona novos arquivos caso o usuário envie mais mídias na edição
            files = request.FILES.getlist('media_files')
            for f in files:
                ProjectMedia.objects.create(project=project, file=f)
                
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