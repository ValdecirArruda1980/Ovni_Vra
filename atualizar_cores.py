with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui os estilos CSS das cores do triângulo e do charuto
old_css_triangle = """        /* 2. Triângulo Verde */
        .shape-triangle {
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-bottom: 15px solid #00ff55;
            filter: drop-shadow(0 0 6px #00ff55);
        }"""

new_css_triangle = """        /* 2. Triângulo Verde Escuro */
        .shape-triangle {
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-bottom: 15px solid #15803d;
            filter: drop-shadow(0 0 4px #166534);
        }"""

old_css_charuto = """        /* 3. Charuto Vermelho */
        .shape-charuto {
            width: 18px;
            height: 8px;
            background: linear-gradient(to bottom, #ff3333, #990000);
            border-radius: 4px;
            box-shadow: 0 0 8px #ff0000;
        }"""

new_css_charuto = """        /* 3. Charuto Marrom Escuro */
        .shape-charuto {
            width: 18px;
            height: 8px;
            background: linear-gradient(to bottom, #78350f, #451a03);
            border-radius: 4px;
            box-shadow: 0 0 6px #291002;
        }"""

content = content.replace(old_css_triangle, new_css_triangle)
content = content.replace(old_css_charuto, new_css_charuto)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Cores atualizadas para triângulo verde escuro e charuto marrom escuro!")
