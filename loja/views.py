import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics
from .models import ProdutoLoja
from .serializers import ProdutoLojaSerializer
from .forms import ProdutoLojaForm
from google import genai
from google.genai import types

class ProdutoLojaListAPIView(generics.ListAPIView):
    queryset = ProdutoLoja.objects.all().order_by('rank')
    serializer_class = ProdutoLojaSerializer

@staff_member_required
def novo_produto_ia_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ritual = request.POST.get('ritual')
        tag = request.POST.get('tag')
        description = request.POST.get('description')
        price = request.POST.get('price') or None
        volume = request.POST.get('volume', 'A confirmar')
        rendimento = request.POST.get('rendimento', 'A confirmar')
        ph = request.POST.get('ph', 'A confirmar')
        durabilidade = request.POST.get('durabilidade', 'A confirmar')
        icon = request.POST.get('icon', 'droplets')
        affiliate_url = request.POST.get('affiliate_url', '')
        verified_partner = True if request.POST.get('verified_partner') == 'on' else False
        image = request.FILES.get('image')

        # Definir rank automático como o último + 1
        last_rank = ProdutoLoja.objects.count() + 1

        ProdutoLoja.objects.create(
            name=name, ritual=ritual, tag=tag, description=description,
            price=price, volume=volume, rendimento=rendimento, ph=ph,
            durabilidade=durabilidade, icon=icon, affiliate_url=affiliate_url,
            verified_partner=verified_partner, image=image, rank=last_rank
        )
        return redirect('/admin/loja/produtoloja/')
        
    return render(request, 'loja/novo_produto_ia.html')

@staff_member_required
def api_extrair_produto_ia(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            texto = body.get('texto', '')
            
            if not texto:
                return JsonResponse({'success': False, 'error': 'Texto vazio.'}, status=400)
            
            # Cliente moderno do Gemini
            client = genai.Client()
            
            prompt = f'''
            Analise o texto abaixo sobre um produto de estética automotiva e extraia as informações em formato JSON estrito, contendo exatamente estas chaves:
            - "name": Nome do produto (string)
            - "ritual": Escolha obrigatoriamente entre 'lavagem', 'blindagem' ou 'acabamento' (string)
            - "tag": Tag curta de destaque, ex: 'Lavagem segura', 'Proteção' (string)
            - "description": Descrição comercial resumida e atrativa (string)
            - "price": Preço numérico em formato float ou null se não houver (number/null)
            - "volume": Volume ou tamanho, ex: '500ml', '1L' (string)
            - "rendimento": Rendimento estimado, ex: 'Até 15 carros' (string)
            - "ph": Valor do pH, ex: 'Neutro', 'pH 7', 'Ácido' (string)
            - "durabilidade": Durabilidade, ex: '3 meses', 'Não se aplica' (string)
            - "icon": Escolha um ícone adequado entre: 'droplets', 'scan-search', 'shield-check', 'sparkles', 'wind', 'layers-3' (string)

            Texto do produto:
            "{texto}"
            '''
            
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            
            resultado_json = json.loads(response.text)
            return JsonResponse({'success': True, 'data': resultado_json})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)

def vitrine_loja_view(request):
    return render(request, 'loja/loja.html')

def gerenciar_produtos(request):
    produtos = ProdutoLoja.objects.all().order_by('-id')
    return render(request, 'loja/gerenciar_produtos.html', {'produtos': produtos})

def editar_produto(request, pk):
    produto = get_object_or_404(ProdutoLoja, pk=pk)
    if request.method == 'POST':
        form = ProdutoLojaForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_produtos')
    else:
        form = ProdutoLojaForm(instance=produto)
    return render(request, 'loja/editar_produto.html', {'form': form, 'produto': produto})

def excluir_produto(request, pk):
    produto = get_object_or_404(ProdutoLoja, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('gerenciar_produtos')
    return render(request, 'loja/excluir_produto.html', {'produto': produto})