with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui as classes CSS para garantir tamanho e visibilidade correta dos ícones no Leaflet
old_css = """        /* Ícones Customizados Geométricos */
        .custom-shape-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 11px;
        }
        .shape-plasma {
            width: 16px;
            height: 16px;
            background: radial-gradient(circle, #fff 0%, #ff5500 50%, #ff0000 100%);
            border-radius: 50%;
            box-shadow: 0 0 10px #ff5500, 0 0 20px #ff3300;
        }
        .shape-cylinder {
            width: 8px;
            height: 20px;
            background: linear-gradient(to right, #003311, #00ff55, #003311);
            border-radius: 4px;
            box-shadow: 0 0 8px #00ff55;
        }
        .shape-triangle {
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-bottom: 16px solid #38bdf8;
            filter: drop-shadow(0 0 6px #38bdf8);
        }
        .shape-disco {
            width: 18px;
            height: 10px;
            background: radial-gradient(ellipse at center, #c084fc 0%, #7e22ce 100%);
            border-radius: 50%;
            box-shadow: 0 0 8px #a855f7;
        }
        .shape-nasa {
            width: 12px;
            height: 12px;
            background: #ff0055;
            transform: rotate(45deg);
            box-shadow: 0 0 8px #ff0055;
        }"""

new_css = """        /* Ícones Customizados Geométricos Visíveis */
        .custom-shape-icon {
            background: transparent;
        }
        .shape-plasma {
            width: 14px;
            height: 14px;
            background: radial-gradient(circle, #ffffff 0%, #ff6600 60%, #cc0000 100%);
            border-radius: 50%;
            border: 1px solid #ffaa00;
            box-shadow: 0 0 10px #ff5500, 0 0 15px #ff0000;
        }
        .shape-cylinder {
            width: 8px;
            height: 18px;
            background: linear-gradient(to right, #003311, #00ff55, #003311);
            border-radius: 3px;
            border: 1px solid #ffffff;
            box-shadow: 0 0 10px #00ff55;
        }
        .shape-triangle {
            width: 0;
            height: 0;
            border-left: 7px solid transparent;
            border-right: 7px solid transparent;
            border-bottom: 14px solid #38bdf8;
            filter: drop-shadow(0 0 6px #38bdf8);
        }
        .shape-disco {
            width: 16px;
            height: 9px;
            background: radial-gradient(ellipse at center, #e879f9 0%, #9333ea 100%);
            border-radius: 50%;
            border: 1px solid #f0abfc;
            box-shadow: 0 0 8px #a855f7;
        }
        .shape-nasa {
            width: 12px;
            height: 12px;
            background: #ff0055;
            transform: rotate(45deg);
            border: 1px solid #ffffff;
            box-shadow: 0 0 8px #ff0055;
        }"""

content = content.replace(old_css, new_css)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ CSS dos ícones corrigido para exibição imediata no mapa!")
