with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui a função de ícones por emojis expressivos com forte brilho neon compatíveis com o Leaflet
old_func = """        function getIconByShape(shape, isNasa) {
            if (isNasa) return { cssClass: 'shape-nasa', label: 'Artefato / Meteoro', color: '#ff0055', textSim: '☄️' };
            
            const shapeLower = (shape || '').toLowerCase();
            if (shapeLower.includes('triângulo') || shapeLower.includes('triangulo')) return { cssClass: 'shape-triangle', label: 'Triângulo Anômalo', color: '#38bdf8', textSim: '🔺' };
            if (shapeLower.includes('esfera') || shapeLower.includes('orb') || shapeLower.includes('luminosa')) return { cssClass: 'shape-plasma', label: 'Esfera de Fogo (Plasma)', color: '#ff5500', textSim: '🔥' };
            if (shapeLower.includes('tic-tac') || shapeLower.includes('cilindro') || shapeLower.includes('charuto')) return { cssClass: 'shape-cylinder', label: 'Cilindro Tático Verde', color: '#00ff55', textSim: '🔋' };
            if (shapeLower.includes('disco')) return { cssClass: 'shape-disco', label: 'Disco Voador', color: '#a855f7', textSim: '🛸' };
            
            return { cssClass: 'shape-cylinder', label: 'Vetor Anômalo', color: '#00ff55', textSim: '🛸' };
        }"""

new_func = """        function getIconByShape(shape, isNasa) {
            if (isNasa) return { emoji: '🔴', label: 'Artefato / Meteoro', color: '#ff0055' };
            
            const shapeLower = (shape || '').toLowerCase();
            if (shapeLower.includes('triângulo') || shapeLower.includes('triangulo')) return { emoji: '🔺', label: 'Triângulo Anômalo', color: '#38bdf8' };
            if (shapeLower.includes('esfera') || shapeLower.includes('orb') || shapeLower.includes('luminosa')) return { emoji: '🟠', label: 'Esfera de Fogo (Plasma)', color: '#ff5500' };
            if (shapeLower.includes('tic-tac') || shapeLower.includes('cilindro') || shapeLower.includes('charuto')) return { emoji: '🟢', label: 'Cilindro Tático Verde', color: '#00ff55' };
            if (shapeLower.includes('disco')) return { emoji: '🛸', label: 'Disco Voador', color: '#a855f7' };
            
            return { emoji: '🛸', label: 'Vetor Anômalo', color: '#00ffaa' };
        }"""

content = content.replace(old_func, new_func)

# Atualiza a criação do customDivIcon para usar o emoji garantido com sombra de brilho
old_marker = """                        const customDivIcon = L.divIcon({
                            className: 'custom-shape-icon',
                            html: `<div class="${iconData.cssClass}"></div>`,
                            iconSize: [24, 24],
                            iconAnchor: [12, 12]
                        });"""

new_marker = """                        const customDivIcon = L.divIcon({
                            className: 'custom-ufo-icon',
                            html: `<span style="font-size: 16px; filter: drop-shadow(0 0 6px ${iconData.color});">${iconData.emoji}</span>`,
                            iconSize: [24, 24],
                            iconAnchor: [12, 12]
                        });"""

content = content.replace(old_marker, new_marker)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Ícones com emojis estilizados e brilho neon aplicados!")
