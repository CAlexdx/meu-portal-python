# 🐍 Meu Portal Python

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Meu Portal Python é um projeto que desenvolvi em Flask reunindo diversas ferramentas úteis em um único lugar. Criei este projeto para facilitar o acesso a utilitários do dia a dia, como calculadora, tradutor, gerador de senhas, conversores, entre outros.

A ideia principal é ser um portal de utilidades online, acessível tanto localmente quanto hospedado em nuvem.

🔗 **[Acesse a versão online](https://meu-portal-python.onrender.com)**

---

## 🔧 Ferramentas Disponíveis

Meu projeto já conta com os seguintes módulos:

### 📊 Matemática e Finanças
- **🧮 Calculadora** - Realiza operações matemáticas básicas
- **📈 Juros Compostos** - Calcula o crescimento de capital ao longo do tempo
- **💰 Orçamento** - Ferramenta simples para organizar gastos
- **📘 Média Escolar** - Calcula médias e aprovações automaticamente
- **⚖️ Calculadora de IMC** - Calcula o Índice de Massa Corporal
- **💰 CLT vs PJ** - Compara salário líquido entre CLT e Pessoa Jurídica

### 🔄 Conversores
- **🌡️ Conversor de Temperatura** - Celsius ↔ Fahrenheit ↔ Kelvin
- **🕒 Conversor de Tempo** - Converte horas, minutos e segundos entre diferentes formatos
- **💱 Conversor de Moedas** - Converte valores entre moedas
- **⚙️ Conversor de Medidas** - Conversão entre diferentes unidades de medida

### 🌍 Utilidades Globais
- **☀️ Clima Global** - Exibe informações de temperatura, umidade e condições do tempo em cidades do mundo
- **🌍 Tradutor** - Tradução de textos para vários idiomas
- **🗺️ Mapa Turístico** - Mostra um mapa interativo com pontos turísticos e curiosidades

### 🛠️ Ferramentas de Produtividade
- **📅 Calendário** - Visualização de calendários mensais/anuais
- **📝 Estatísticas de Texto** - Conta palavras, caracteres e frases
- **🔑 Gerador de Senhas** - Cria senhas seguras automaticamente
- **🔗 Encurtador de Links** - Gera URLs curtas automaticamente
- **🔳 Gerador de QR Code** - Criação de QR Codes a partir de textos ou links

### 🎯 Entretenimento e Utilidades
- **🎲 Sorteio Simples** - Realiza sorteios aleatórios de nomes
- **👥 Sorteio de Equipes** - Divide nomes em grupos aleatórios
- **❓ Quiz** - Quiz interativo de perguntas e respostas
- **🚗 Consumo de Combustível** - Calcula o consumo médio de combustível de um veículo

### 🎨 Multimídia
- **🖼️ Editor de Imagens** - Ferramentas básicas de edição com Pillow
- **▶️ YouTube Downloader** - Faz download de vídeos do YouTube (somente localmente)

---

## ⚙️ Como Rodar o Projeto Localmente

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd meu-portal-python
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Execute o servidor local**
```bash
python app.py
```

6. **Acesse no navegador**
```
http://127.0.0.1:5000/
```

Os resultados (QR Codes, vídeos baixados, etc.) ficam salvos na pasta `/outputs`.

---

## 🌐 Versão Online

Hospedei o projeto no Render e está disponível em:
🔗 **[meu-portal-python.onrender.com](https://meu-portal-python.onrender.com)**

---

## 🛠️ Como Adicionar um Novo Módulo

Quando quero adicionar uma nova ferramenta, sigo estes passos:

1. Crio um arquivo em `scripts/` (exemplo: `meu_modulo.py`)
2. Crio um template em `templates/` (exemplo: `meu_modulo.html`)
3. No `app.py`, adiciono uma nova rota Flask para o módulo
4. No `index.html`, adiciono um link para a nova ferramenta

---

## 📌 Objetivo do Projeto

Criei este portal como um laboratório de estudos em Python e Flask, reunindo pequenos projetos em uma plataforma organizada. Meu objetivo é facilitar o aprendizado, demonstrar integração de bibliotecas e oferecer um conjunto de ferramentas úteis para qualquer pessoa acessar.

O projeto demonstra:
- Organização de rotas Flask
- Criação de interfaces HTML dinâmicas
- Integração com APIs externas (como clima e tradução)
- Manipulação de imagens e dados em Python
- Sistema de estatísticas e painel administrativo

---

## ⚠️ Observação sobre o Módulo YouTube Downloader

Descobri que a plataforma Render não permite que aplicativos hospedados realizem conexões diretas com os servidores do YouTube. Isso impede o funcionamento do módulo de download de vídeos na versão online do portal.

🔹 **Localmente (no computador)**: O download funciona normalmente.
🔹 **Online (Render)**: O módulo exibe uma mensagem explicando a limitação.

Essa restrição é comum em serviços de hospedagem e tem o objetivo de evitar abusos de rede ou possíveis violações de direitos autorais. Mantive o código incluído para fins de estudo e demonstração da integração com a biblioteca pytubefix.

---

## 🔧 Solução de Problemas

Se ao rodar o comando `python app.py` você receber o erro:
```
Foi feita uma tentativa de acesso a um soquete de uma maneira que é proibida pelas permissões de acesso
```

Isso significa que a porta 5000 está ocupada. Para resolver, altere a porta no `app.py` ou execute:
```bash
flask run --port=8000
```

---

## 💻 Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **Gunicorn** - Servidor WSGI para produção

### Bibliotecas Principais
- **requests** - Requisições HTTP para APIs externas
- **Pillow** - Manipulação de imagens
- **pyqrcode** & **pypng** - Geração de QR Codes
- **pytubefix** - Download de vídeos do YouTube
- **deep-translator** - Tradução de textos
- **holidays** - Gerenciamento de feriados
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript**

---

## 📁 Estrutura do Projeto

```
meu-portal-python/
│
├── app.py                      # Arquivo principal da aplicação
├── requirements.txt            # Dependências do projeto
├── Procfile                    # Configuração para deploy no Render
├── .env                        # Variáveis de ambiente (não versionado)
├── .gitignore                  # Arquivos ignorados pelo Git
├── stats.json                  # Estatísticas de uso das ferramentas
│
├── scripts/                    # Módulos Python das ferramentas
│   ├── calculadora.py
│   ├── calendario.py
│   ├── clima.py
│   ├── clt_vs_pj.py
│   └── ... (outros scripts)
│
├── templates/                  # Templates HTML
│   ├── index.html             # Página inicial
│   ├── admin.html             # Painel administrativo
│   └── ... (outros templates)
│
├── static/                     # Arquivos estáticos
│   ├── style.css              # Estilos CSS
│   └── image.png              # Imagens
│
└── outputs/                    # Arquivos gerados (QR Codes, downloads)
```

---

## 🔐 Painel Administrativo

Implementei um painel administrativo protegido por autenticação HTTP Basic.

### Como Acessar
1. Acesse `/admin`
2. Digite o usuário e senha configurados no `.env`
3. Visualize as estatísticas de uso

### Funcionalidades
- Total de acessos ao portal
- Estatísticas de uso de cada ferramenta
- Dados salvos em `stats.json`

---

## 🌐 Deploy no Render

Hospedei este projeto no Render. Se você quiser fazer o mesmo:

1. **Crie uma conta no [Render](https://render.com)**
2. **Conecte seu repositório GitHub**
3. **Configure as variáveis de ambiente**
   - `ADMIN_USER` - Seu usuário do painel admin
   - `ADMIN_PASS` - Sua senha
   - `SECRET_KEY` - Uma chave aleatória para o Flask
   - `FLASK_ENV=production`
   - `RENDER=true`
4. **O Render detecta automaticamente o `Procfile`**
5. **Aguarde o deploy ser concluído**

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você quiser adicionar algo:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT - livre para estudo e modificação.

---

## 👨‍💻 Sobre Mim

**Calebe Alves Câmara**

Desenvolvi este projeto como forma de estudar Python e Flask, reunindo várias ferramentas úteis em um só lugar. Espero que seja útil para outras pessoas também!

**Ano**: 2025

---

## 🙏 Agradecimentos

Agradeço à comunidade Flask e aos desenvolvedores das bibliotecas que utilizei neste projeto.

---

## 📊 Status do Projeto

✅ **Ativo** - Estou continuamente adicionando novas ferramentas e melhorias.

---

<div align="center">

**Desenvolvido com ❤️ e Python**

⭐ Se este projeto foi útil para você, considere dar uma estrela!

</div>