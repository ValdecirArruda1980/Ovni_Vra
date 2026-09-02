with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Adiciona os estilos CSS para as formas geométricas customizadas no <style>
novo_estilo = """        .coord-txt { color: #38bdf8; font-weight: bold; }
        .city-txt { color: #facc15; font-weight: bold; }
        .city-start-txt { color: #38bdf8; font-weight: bold; }
        
        /* Ícones Customizados Geométricos */
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

content = content.replace(".coord-txt { color: #38bdf8; font-weight: bold; }", novo_estilo)

# 2. Atualiza a função getIconByShape para retornar as classes CSS correspondentes
old_func = """        function getIconByShape(shape, isNasa) {
            if (isNasa) return { icon: '☄️', label: 'Artefato / Meteoro', color: '#ff0055' };
            
            const shapeLower = (shape || '').toLowerCase();
            if (shapeLower.includes('triângulo') || shapeLower.includes('triangulo')) return { icon: '🔺', label: 'Triângulo Anômalo', color: '#38bdf8' };
            if (shapeLower.includes('esfera') || shapeLower.includes('orb') || shapeLower.includes('luminosa')) return { icon: '🟠', label: 'Objeto Luminoso Redondo', color: '#ff6600' };
            if (shapeLower.includes('tic-tac') || shapeLower.includes('cilindro') || shapeLower.includes('charuto')) return { icon: '🔋', label: 'Objeto Cilindrico', color: '#00ffaa' };
            if (shapeLower.includes('disco')) return { icon: '🛸', label: 'Disco Voador', color: '#a855f7' };
            
            return { icon: '🛸', label: 'Nave Não Identificada', color: '#00ffaa' };
        }"""

new_func = """        function getIconByShape(shape, isNasa) {
            if (isNasa) return { cssClass: 'shape-nasa', label: 'Artefato / Meteoro', color: '#ff0055', textSim: '☄️' };
            
            const shapeLower = (shape || '').toLowerCase();
            if (shapeLower.includes('triângulo') || shapeLower.includes('triangulo')) return { cssClass: 'shape-triangle', label: 'Triângulo Anômalo', color: '#38bdf8', textSim: '🔺' };
            if (shapeLower.includes('esfera') || shapeLower.includes('orb') || shapeLower.includes('luminosa')) return { cssClass: 'shape-plasma', label: 'Esfera de Fogo (Plasma)', color: '#ff5500', textSim: '🔥' };
            if (shapeLower.includes('tic-tac') || shapeLower.includes('cilindro') || shapeLower.includes('charuto')) return { cssClass: 'shape-cylinder', label: 'Cilindro Tático Verde', color: '#00ff55', textSim: '🔋' };
            if (shapeLower.includes('disco')) return { cssClass: 'shape-disco', label: 'Disco Voador', color: '#a855f7', textSim: '🛸' };
            
            return { cssClass: 'shape-cylinder', label: 'Vetor Anômalo', color: '#00ff55', textSim: '🛸' };
        }"""

content = content.replace(old_func, new_func)

# 3. Atualiza a criação do marcador no Leaflet para usar a classe CSS customizada
old_marker = """                        const customDivIcon = L.divIcon({
                            className: 'custom-ufo-icon',
                            html: `<span style="text-shadow: 0 0 8px ${iconData.color}; font-size: 20px;">${iconData.icon}</span>`,
                            iconSize: [28, 28],
                            iconAnchor: [14, 14]
                        });"""

new_marker = """                        const customDivIcon = L.divIcon({
                            className: 'custom-shape-icon',
                            html: `<div class="${iconData.cssClass}"></div>`,
                            iconSize: [24, 24],
                            iconAnchor: [12, 12]
                        });"""

content = content.replace(old_marker, new_marker)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Ícones em CSS puro atualizados (esfera de fogo e cilindro verde)!")
