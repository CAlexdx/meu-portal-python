Meu Portal Python é um projeto desenvolvido em Flask que reúne diversas ferramentas úteis em um único lugar.
Ele foi criado para facilitar o acesso a utilitários do dia a dia, como calculadora, tradutor, gerador de senhas, conversores, entre outros.

A ideia principal é ser um portal de utilidades online, acessível tanto localmente quanto hospedado em nuvem.

🔧 FERRAMENTAS DISPONÍVEIS

O projeto já conta com os seguintes módulos:

📅 Calendário – Visualização de calendários mensais/anuais.
🕒 Conversor de Tempo – Converte horas, minutos e segundos entre diferentes formatos.
🧮 Calculadora – Realiza operações matemáticas básicas.
☀️ Clima Global – Exibe informações de temperatura, umidade e condições do tempo em cidades do mundo.
🌡️ Conversor de Temperatura – Celsius ↔ Fahrenheit ↔ Kelvin.
⚖️ Calculadora de IMC – Calcula o Índice de Massa Corporal.
▶️ YouTube Downloader – Faz download de vídeos do YouTube (somente localmente).
🔗 Encurtador de Links – Gera URLs curtas automaticamente.
🔳 Gerador de QR Code – Criação de QR Codes a partir de textos ou links.
🖼️ Editor de Imagens – Ferramentas básicas de edição com Pillow.
📝 Estatísticas de Texto – Conta palavras, caracteres e frases.
📘 Média Escolar – Calcula médias e aprovações automaticamente.
🗺️ Mapa Turístico/Global – Mostra um mapa interativo com pontos turísticos e curiosidades.
🌍 Tradutor – Tradução de textos para vários idiomas.
💱 Conversor de Moedas – Converte valores entre moedas.
💰 Orçamento – Ferramenta simples para organizar gastos.
🚗 Consumo de Combustível – Calcula o consumo médio de combustível de um veículo.
📈 Juros Compostos – Calcula o crescimento de capital ao longo do tempo.
🎲 Sorteio Simples – Realiza sorteios aleatórios de nomes.
👥 Sorteio de Equipes – Divide nomes em grupos aleatórios.
❓ Quiz – Quiz interativo de perguntas e respostas.
🔑 Gerador de Senhas – Cria senhas seguras automaticamente.

⚙️ COMO RODAR O PROJETO LOCALMENTE
Instale as dependências:
pip install flask pyqrcode pillow pytubefix requests googletrans==4.0.0-rc1
pip install -r requirements.txt

Execute o servidor local:
python app.py
Acesse no navegador:
http://127.0.0.1:5000/

Os resultados (QR Codes, vídeos baixados, etc.) ficam salvos na pasta /outputs.

🌐 VERSÃO ONLINE
O projeto também está disponível hospedado no Render:
🔗 meu-portal-python.onrender.com

🛠️ COMO ADICIONAR UM NOVO MÓDULO
Crie um arquivo em scripts/ (exemplo: meu_modulo.py)
Crie um template em templates/ (exemplo: meu_modulo.html)
No app.py, adicione uma nova rota Flask para o módulo.
No index.html, adicione um link para a nova ferramenta.

📌 OBJETIVO DO PROJETO

Este portal foi criado como um laboratório de estudos em Python e Flask, reunindo pequenos projetos em uma plataforma organizada.
O objetivo é facilitar o aprendizado, demonstrar integração de bibliotecas e oferecer um conjunto de ferramentas úteis para qualquer pessoa acessar.

O projeto também demonstra:
Organização de rotas Flask
Criação de interfaces HTML dinâmicas
Integração com APIs externas (como clima e tradução)
Manipulação de imagens e dados em Python

⚠️ OBSERVAÇÃO SOBRE O MÓDULO YOUTUBE DOWNLOADER
Por motivos de segurança, a plataforma Render não permite que aplicativos hospedados realizem conexões diretas com os servidores do YouTube.
Isso impede o funcionamento do módulo de download de vídeos na versão online do portal.

🔹 Localmente (no computador): O download funciona normalmente.
🔹 Online (Render): O módulo exibe uma mensagem explicando a limitação.

Essa restrição é comum em serviços de hospedagem e tem o objetivo de evitar abusos de rede ou possíveis violações de direitos autorais.
O código continua incluído para fins de estudo e demonstração da integração com a biblioteca pytubefix.

📚 INFORMAÇÕES TÉCNICAS

Tecnologias utilizadas:
Flask (Python)
HTML, CSS e JavaScript

Autor: Calebe Alves Câmara
Ano: 2025
Licença: Livre para estudo e modificação (uso não comercial)