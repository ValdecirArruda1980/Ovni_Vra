with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui a renderização do card para calcular a distância direto na hora da criação do HTML (sem dependência externa)
old_card_code = """                    card.innerHTML = `
                        <div class="ufo-title">
                            <span>${shapeCfg.iconSymbol} ${item.id}</span>
                            <span class="badge ${isNasa ? 'badge-warn' : ''}">${item.source}</span>
                        </div>
                        <b>CIDADE INÍCIO:</b> <span class="city-start-txt" id="card-${keyId}-start">${item.country}</span><br>
                        <b>CIDADE ATUAL:</b> <span class="city-txt" id="card-${keyId}-curr">${item.country}</span><br>
                        <b>PAÍS / REGIÃO:</b> ${item.country}<br>
                        <b>COORDENADAS:</b> <span class="coord-txt">${item.latitude}, ${item.longitude}</span><br>
                        <b>DISTÂNCIA PERCORRIDA:</b> <span style="color:#00ffaa; font-weight:bold;" id="card-${keyId}-dist">Calculando...</span><br>
                        <b>FORMA:</b> ${shapeCfg.name}<br>
                        <b>VELOCIDADE:</b> ${item.speed_kmh.toLocaleString()} km/h<br>
                        <b>ALTITUDE:</b> ${item.altitude_m.toLocaleString()} m<br>
                        <p style="margin-top: 5px; opacity: 0.85;">${item.summary}</p>
                    `;"""

new_card_code = """                    // Calcula a distância diretamente pelas coordenadas do trajeto
                    const startPt = item.trajectory && item.trajectory.length > 0 ? item.trajectory[0] : [item.latitude, item.longitude];
                    const distCalc = calcularDistanciaKm(startPt[0], startPt[1], item.latitude, item.longitude);

                    card.innerHTML = `
                        <div class="ufo-title">
                            <span>${shapeCfg.iconSymbol} ${item.id}</span>
                            <span class="badge ${isNasa ? 'badge-warn' : ''}">${item.source}</span>
                        </div>
                        <b>CIDADE INÍCIO:</b> <span class="city-start-txt" id="card-${keyId}-start">${item.country}</span><br>
                        <b>CIDADE ATUAL:</b> <span class="city-txt" id="card-${keyId}-curr">${item.country}</span><br>
                        <b>PAÍS / REGIÃO:</b> ${item.country}<br>
                        <b>COORDENADAS:</b> <span class="coord-txt">${item.latitude}, ${item.longitude}</span><br>
                        <b>DISTÂNCIA PERCORRIDA:</b> <span style="color:#00ffaa; font-weight:bold;">${distCalc.toLocaleString()} km</span><br>
                        <b>FORMA:</b> ${shapeCfg.name}<br>
                        <b>VELOCIDADE:</b> ${item.speed_kmh.toLocaleString()} km/h<br>
                        <b>ALTITUDE:</b> ${item.altitude_m.toLocaleString()} m<br>
                        <p style="margin-top: 5px; opacity: 0.85;">${item.summary}</p>
                    `;"""

content = content.replace(old_card_code, new_card_code)

# Remove o setTimeout redundante anterior
content = content.replace("""                        // Dispara o cálculo em background para preencher o card imediatamente
                        setTimeout(() => {
                            carregarCidadesVoo(item, `card-${keyId}`);
                        }, idx * 50);""", "")

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Distâncias calculadas e exibidas instantaneamente em todos os cartões!")
