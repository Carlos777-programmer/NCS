# NCS ERP - Sistema de Gestão para Estética Automotiva 🚗

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-orange?style=for-the-badge&logo=pwa&logoColor=white)

Sistema ERP especializado em gestão para o nicho de estética automotiva e oficinas, desenvolvido para centralizar o controle operacional, financeiro e de atendimento da empresa em uma interface moderna, responsiva e com suporte a PWA.

## 🚀 1. Funcionalidades Principais

*   **Autenticação e Segurança:** Tela de login customizada com animação institucional em vídeo e mecanismo de segurança contra tentativas excessivas de acesso incorreto.
*   **Cadastros e Catálogo:** Gestão completa de clientes, frota de veículos com autocomplete em tempo real e catálogo de serviços com precificação e custos estimados.
*   **Operações e Ordens de Serviço (OS):** Controle ponta a ponta do fluxo de atendimento, com agenda visual por status e buscas dinâmicas por período ou texto.
*   **Dashboard e Financeiro:** Painel centralizado com estatísticas em tempo real (faturamento, gastos, folha de pagamento e lucro líquido), além do controle de despesas e retiradas.
*   **Suporte a PWA:** Pronto para ser instalado e utilizado como aplicativo mobile-first.

## 🛠️ 2. Tecnologias Utilizadas

*   **Linguagem:** Python 3.x
*   **Framework Web:** Django
*   **Frontend:** HTML5, CSS3, JavaScript (com variáveis CSS customizadas e componentes responsivos)
*   **Banco de Dados:** SQLite (Desenvolvimento)
*   **Recursos Adicionais:** PWA (Service Worker)

## ⚙️ 3. Instalação e Configuração

3.1 **Clone o repositório:**
   ```bash
   git clone [https://github.com/Carlos777-programmer/NCS.git](https://github.com/Carlos777-programmer/NCS.git)
   ```
3.2 **Entre na pasta do projeto:**

```Bash
cd NCS
Configure o Ambiente Virtual (venv):
```

```Bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar no Windows (PowerShell):

.\venv\Scripts\Activate.ps1

# Ativar no Windows (Prompt de Comando/CMD):
.\venv\Scripts\activate.bat

# Ativar no Linux ou macOS:
source venv/bin/activate
```
3.3 **Instale as dependências:**

```Bash
pip install -r requirements.txt
```
## 🔐 4. Configuração de Segurança
Crie um arquivo .env na raiz do projeto (no mesmo nível do manage.py) e adicione as configurações de ambiente:

Snippet de código
````bash
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
````
## 🚀 5. Migrações e Execução
Para preparar o banco de dados e rodar o sistema pela primeira vez:

````Bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Para criar acesso ao painel administrativo
python manage.py runserver
Acesse o sistema no navegador através de: http://127.0.0.1:8000/

````

## 📈 Roadmap de Desenvolvimento
- [x] Estruturação da arquitetura base em Django e PWA.

- [x] Módulos de clientes, veículos e catálogo de serviços.

- [x] Gestão de Ordens de Serviço e Agendamentos.

- [x] Dashboard financeiro e controle de folha de pagamento.

## Desenvolvido por Carlos Marques

[LinkedIn](https://www.linkedin.com/in/carlos-marques-0b9346267/) | [GitHub](https://github.com/Carlos777-programmer)
