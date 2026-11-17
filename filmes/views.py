from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Filme

def lista(request):
    request.session["visitas"] = (request.session.get("visitas", 0) + 1)
    filmes = Filme.objects.all()
    return render(request, "filmes/lista.html",
                {"filmes": filmes})

def novo(request):
    return render(request, "filmes/novo.html")

@require_POST
def salvar_novo(request):
    Filme.objects.create(
        titulo=request.POST["titulo"],
        genero=request.POST["genero"],
        ano=request.POST["ano"],
        assistido="assistido" in request.POST,
    )
    request.session["ultimo_filme"] = request.POST["titulo"]
    return redirect("lista")

def editar(request, id):
    filme = get_object_or_404(Filme, id=id)
    request.session["ultimo_filme"] = filme.titulo
    
    return render(request, "filmes/editar.html",
        {"filme": filme})

@require_POST
def salvar_edicao(request, id):
    filme = get_object_or_404(Filme, id=id)
    filme.titulo = request.POST["titulo"]
    filme.genero = request.POST["genero"]
    filme.ano = request.POST["ano"]
    filme.assistido = "assistido" in request.POST
    filme.save()
    
    return redirect("lista")

@require_POST
def excluir(request, id):
    filme = get_object_or_404(Filme, id=id)
    filme.delete()
    return redirect("lista")

@require_POST
def salvar_nome(request):
    nome = request.POST.get("nome", "").strip()[:40]
    if nome:
        request.session["nome_visitante"] = nome
    return redirect("lista")

@require_POST
def esquecer_nome(request):
    request.session.pop("nome_visitante", None)
    return redirect("lista")

def favoritar(request, id):
    favs = request.session.get("favoritos", [])
    if id not in favs:
        favs.append(id)
    
    request.session["favoritos"] = favs
    return redirect("editar", id=id)