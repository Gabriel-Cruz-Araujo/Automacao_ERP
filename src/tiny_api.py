# tiny_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
# -----------------------------
# Configuração do token via variável de ambiente
# -----------------------------
TOKEN = os.getenv("TINY_API_TOKEN")

if not TOKEN:
    raise ValueError("O token da API do Tiny não está definido na variável de ambiente 'TINY_API_TOKEN'.")


def obter_tipo_contato_por_cpf(cpf: str) -> str:
    """
    Recebe CPF/CNPJ e retorna o tipo principal do contato no Tiny,
    ex: 'Cliente Home Care' ou 'Profissional'. Retorna 'Não definido' se não encontrado.
    
    """
    # 1) Buscar cliente pelo CPF
    url_busca = "https://api.tiny.com.br/api2/contatos.pesquisa.php"
    params_busca = {"cpf_cnpj": cpf, "token": TOKEN, "formato": "json"}
    response_busca = requests.get(url_busca, params=params_busca)
    
    if response_busca.status_code != 200:
        print(f"Erro ao buscar cliente: {response_busca.status_code} {response_busca.text}")
        return "Não definido"
    
    dados_busca = response_busca.json()
    contatos = dados_busca.get("retorno", {}).get("contatos", [])
    if not contatos:
        return "Não definido"
    
    cliente_id = contatos[0]["contato"]["id"]
    
    # 2) Buscar detalhes do cliente
    url_detalhe = "https://api.tiny.com.br/api2/contato.obter.php"
    params_detalhe = {"id": cliente_id, "token": TOKEN, "formato": "json"}
    response_detalhe = requests.get(url_detalhe, params=params_detalhe)
    
    if response_detalhe.status_code != 200:
        print(f"Erro ao detalhar cliente: {response_detalhe.status_code} {response_detalhe.text}")
        return "Não definido"
    
    dados_detalhe = response_detalhe.json()
    contato = dados_detalhe.get("retorno", {}).get("contato", {})
    tipos_contato = contato.get("tipos_contato", [])
    
    if tipos_contato:
        return tipos_contato[0]["tipo"].strip()
    
    return "Não definido"
