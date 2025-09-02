# ⚡ Automação ERP

Automação inteligente para **qualificação de clientes** via integração entre **Tiny ERP**, **Kommo CRM** e **Olist**.  
O projeto utiliza **Selenium** para automatizar ações no Kommo, integrações com a **API Tiny** para consulta de clientes e regras customizadas para **classificação automática de leads**.

---

## ✨ Funcionalidades

- 🤖 Automatiza a navegação e ações no **Kommo CRM** usando Selenium.  
- 🔍 Consulta e qualifica clientes via **API Tiny** (usando CPF/CNPJ).  
- 🏷️ Classifica leads em categorias como **“Profissional”** ou **“Home Care”**.  
- 📊 Gera estatísticas do processamento realizado.  

---

## 📂 Estrutura do Projeto

```bash
AUTOMACAO_ERP/
├── .env                      # Variáveis de ambiente (credenciais API/CRM)
├── requirements.txt          # Dependências do projeto em Python
├── main.py                   # Ponto de entrada, executa a automação
└── src/
    ├── api/
    │   ├── tiny_api.py       # Consulta clientes via API Tiny
    │   └── teste_api.py      # Testes de integração da API
    │
    ├── selenium_bot/
    │   ├── qualificar_clientes.py # Automação principal do Kommo (Selenium)
    │   ├── erp_selenium.py        # Outras rotinas de automação
    │
    └── utils/                # Funções auxiliares e utilitárias
```
## ⚙️ Tecnologias Utilizadas

- 🐍**Python 3.10+**
- 🌐**Selenium**
- 🔗**Requests**
- 📦**Tiny API**
- 🔒**dotenv**

## 📋Requisitos

- Python 3.8+
- Navegador Google Chrome instalado
- ChromeDriver compatível, disponível no PATH
- Credenciais válidas do Tiny ERP, Kommo CRM e (opcional) Olist

## 🚀Instalação

### Clone o repositório
git clone https://github.com/seu-usuario/AUTOMACAO_ERP.git

cd AUTOMACAO_ERP

### Crie um ambiente virtual
python -m venv .venv

### Ative o ambiente virtual
- source .venv/bin/activate  -  **Linux/Mac**
- .venv\Scripts\activate     -  **Windows**

### Instale as dependências
pip install -r requirements.txt

## 🔑Configuração

Crie um arquivo `.env`  com suas credenciais:
```
ERP_USERNAME=""
ERP_PASSWORD=""
KOMMO_USERNAME=""
KOMMO_PASSWORD=""
KOMMO_URL=""
TINY_API_TOKEN=""
```

🔹O token da Tiny pode ser obtido no painel do ERP Tiny.🔹

## ▶️Como Usar

Basta rodar o arquivo `main.py` após configurar as variáveis de ambiente:

Isso inicializa o robô Selenium, faz login no Kommo, processa leads, consulta dados no Tiny e categoriza cada cliente processado.

## 🧩Principais Módulos

- `src/api/tiny_api.py`: Funções para consulta à API Tiny, como buscar tipo de cliente por CPF.
- `src/selenium_bot/qualificar_clientes.py`: Automação de navegação no Kommo, fluxo de qualificação, inclusão das chamadas à API Tiny.

## 🤝Contribuindo

Contribuições são bem-vindas!  
- Abra uma issue para sugerir melhorias ou reporte bugs.  
- Envie seu pull request seguindo os padrões do projeto.

## 📜Licença

MIT License. Consulte o arquivo `LICENSE` para detalhes.
