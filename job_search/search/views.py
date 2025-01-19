from django.shortcuts import render
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega o arquivo .env


# Configuração da API
API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")

def buscar_vagas(query):
    """Faz a busca na API do Google Custom Search."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": API_ID,
        "q": query,
        "num": 10
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        return {"error": f"Erro na busca: {e}"}

def index(request):
    """Página principal com o formulário de busca."""
    results = []
    if request.method == "POST":
        cargo = request.POST.get("cargo")
        nivel = request.POST.get("nivel")
        localidade = request.POST.get("localidade")
        modelo_vaga = request.POST.get("modelo_vaga")
        query = f"{cargo} {nivel} {localidade} {modelo_vaga}"
        results = buscar_vagas(query)
    return render(request, "index.html", {"results": results})
