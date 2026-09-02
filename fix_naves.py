with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui a função de ícones no script do index.html
old_func = """        function getIconByShape(shape, isNasa) {
            if (isNasa) return { icon: '☄️', label: 'Artefato / Meteoro' };
            
            const shapeLower = (shape || '').toLowerCase();
            if (shapeLower.includes('triângulo') || shapeLower.includes('triangulo')) return { icon: '🔺', label: 'Triângulo Anômalo' };
            if (shapeLower.includes('esfera') || shapeLower.includes('orb')) return { icon: '🔮', label: 'Esfera / Orb' };
            if (shapeLower.includes('tic-tac') || shapeLower.includes('cilindro') || shapeLower.includes('charuto')) return { icon: '💊', label: 'Tic-Tac / Cilindro' };
            if (shapeLower.includes('disco')) return { icon: '🛸', label: 'Disco Voador' };
            
            return { icon: '🟢', label: 'Vetor Anômalo' };
        }"""

new_func = """        function getIconByShape(shape, isNasa) {
            if (isNasa) return { icon: '☄️', label: 'Artefato / Meteoro', color: '#ff0055' };
            
            const shapeLower = (shape || '').toLowerCase();
            if (shapeLower.includes('triângulo') || shapeLower.includes('triangulo')) return { icon: '🔺', label: 'Triângulo Anômalo', color: '#38bdf8' };
            if (shapeLower.includes('esfera') || shapeLower.includes('orb') || shapeLower.includes('luminosa')) return { icon: '🔥', label: 'Objeto Luminoso (Plasma)', color: '#ff6600' };
            if (shapeLower.includes('tic-tac') || shapeLower.includes('cilindro') || shapeLower.includes('charuto')) return { icon: '🚀', label: 'Nave / Cilindro Tático', color: '#00ffaa' };
            if (shapeLower.includes('disco')) return { icon: '🛸', label: 'Disco Voador', color: '#a855f7' };
            
            return { icon: '🛸', label: 'Nave Não Identificada', color: '#00ffaa' };
        }"""

content = content.replace(old_func, new_func)

# Atualiza a criação do customDivIcon para aplicar a cor específica de cada objeto
old_marker_block = """                        const customDivIcon = L.divIcon({
                            className: `custom-ufo-icon ${isNasa ? 'warning-icon' : ''}`,
                            html: `<span>${iconData.icon}</span>`,
                            iconSize: [24, 24],
                            iconAnchor: [12, 12]
                        });"""

new_marker_block = """                        const customDivIcon = L.divIcon({
                            className: 'custom-ufo-icon',
                            html: `<span style="text-shadow: 0 0 8px ${iconData.color}; font-size: 20px;">${iconData.icon}</span>`,
                            iconSize: [28, 28],
                            iconAnchor: [14, 14]
                        });"""

content = content.replace(old_marker_block, new_marker_block)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Ícones atualizados para naves coloridas e fogo laranja para objetos luminosos!")
