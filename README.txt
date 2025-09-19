Meu Portal Python - Flask

Projetos inclusos:
- Calendário (calendar)
- QR Code Generator (pyqrcode)
- YouTube Downloader (pytubefix)
- conversor (requests)

 Como rodar se for so no terminal sem ser o site oficial:
1 pip install flask pyqrcode pillow pytubefix requests
2 python app.py
3 Acesse http://127.0.0.1:5000/

Os resultados (QR codes, vídeos) ficam em /outputs.

https://meu-portal-python.onrender.com/

 🛠️ Como adicionar um novo módulo

1. Crie um arquivo em `scripts/` (ex: `meu_modulo.py`).
2. Crie um template em `templates/` (ex: `meu_modulo.html`).
3. No `app.py`, adicione uma nova rota para esse módulo.
4. No `index.html`, adicione um link na lista de ferramentas.
