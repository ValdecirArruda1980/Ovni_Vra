import os

with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui o servidor de tiles padrão pelo CartoDB com rótulos em caracteres latinos/português
old_tile = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
new_tile = "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"

content = content.replace(old_tile, new_tile)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Mapa atualizado para padrão com caracteres latinos em português!")
