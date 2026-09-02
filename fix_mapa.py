with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui o servidor do CartoDB pelo servidor Esri World Street Map (Livre, sem API key e em português/latino)
old_tile = "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
new_tile = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"

content = content.replace(old_tile, new_tile)

# Ajusta a atribuição do mapa
content = content.replace("attribution: '&copy; CartoDB &copy; OpenStreetMap'", "attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom'")

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Mapa corrigido para Esri sem chave de API!")
