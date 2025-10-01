Meu Portal Python é um projeto desenvolvido em Flask que reúne diversas ferramentas úteis em um único lugar. Ele foi criado para facilitar o acesso a utilitários do dia a dia, como calculadora, tradutor, gerador de senhas, conversores, entre outros.

A ideia principal é ser um portal de utilidades online, acessível tanto localmente quanto hospedado em nuvem.

🔧 Ferramentas disponíveis
O projeto já conta com os seguintes módulos:

📅 Calendário – Visualização de calendários mensais/anuais.
🔳 Gerador de QR Code – Criação de QR Codes a partir de textos ou links.
▶️ YouTube Downloader – Download de vídeos do YouTube.
💱 Conversor de Moedas – Conversão de valores entre moedas.
📘 Média Escolar – Calculadora de médias de notas.
🌡️ Conversor de Temperatura – Celsius ↔ Fahrenheit ↔ Kelvin.
🔑 Gerador de Senhas – Cria senhas seguras automaticamente.
🎲 Sorteio Simples – Sorteio aleatório de nomes.
👥 Sorteio de Equipes – Divide nomes em grupos aleatórios.
📝 Estatísticas de Texto – Conta palavras, caracteres e frases.
⚖️ Calculadora de IMC – Índice de Massa Corporal.
🖼️ Editor de Imagens – Funções básicas com Pillow.
❓ Quiz – Quiz interativo de perguntas e respostas.
💰 Orçamento – Ferramenta simples para organizar gastos.
🧮 Calculadora – Operações matemáticas básicas.
🌍 Tradutor – Tradução de textos para vários idiomas.
🔗 Encurtador de Links – Gera URLs curtas.
📈 Juros Compostos – Calculadora de crescimento de capital.


⚙️ Como rodar o projeto localmente
Instale as dependências:
pip install flask pyqrcode pillow pytubefix requests googletrans==4.0.0-rc1

Execute o servidor:
python app.py

Acesse no navegador:
http://127.0.0.1:5000/


📂 Os resultados (QR Codes, vídeos baixados, etc.) ficam salvos na pasta /outputs.

Versão Online
O projeto também está disponível hospedado no Render:
meu-portal-python.onrender.com

🛠️ Como adicionar um novo módulo

Crie um arquivo em scripts/ (ex: meu_modulo.py).

Crie um template em templates/ (ex: meu_modulo.html).

No app.py, adicione uma nova rota para esse módulo.

No index.html, adicione um link para a nova ferramenta.

📌 Objetivo do Projeto

Este portal foi criado como um laboratório de estudos em Python e Flask, reunindo pequenos projetos em uma plataforma organizada.
O objetivo é facilitar o aprendizado, demonstrar integração de bibliotecas e oferecer um conjunto de ferramentas úteis para qualquer pessoa acessar.