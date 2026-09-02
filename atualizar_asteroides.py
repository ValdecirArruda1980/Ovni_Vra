import os

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Garante que os objetos da NASA venham com a categoria explícita de Asteroide/NEO
old_nasa_label = '"shape": "Artefato / Corpo Espacial",'
new_nasa_label = '"shape": "Asteroide / Corpo Espacial NEO",'

content = content.replace(old_nasa_label, new_nasa_label)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

with open("static/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Atualiza a função getShapeConfig no index.html para identificar claramente asteroides e a fonte da NASA
old_shape_func = """        function getShapeConfig(shape, isNasa) {
            if (isNasa) return { css: 'shape-nasa', name: 'Artefato / Meteoro', iconSymbol: '☄️' };"""

new_shape_func = """        function getShapeConfig(shape, isNasa) {
            if (isNasa || (shape || '').includes('Asteroide')) return { css: 'shape-nasa', name: 'Asteroide / Corpo Espacial (NASA)', iconSymbol: '☄️' };"""

html_content = html_content.replace(old_shape_func, new_shape_func)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Identificação de asteroides da NASA ativada!")
