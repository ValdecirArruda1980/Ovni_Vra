with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Função auxiliar para injetar o cálculo de distância entre pontos da trajetória
old_calc_func = """        async function carregarCidadesVoo(item, prefix) {
            const startPoint = item.trajectory && item.trajectory.length > 0 ? item.trajectory[0] : [item.latitude, item.longitude];
            const currPoint = [item.latitude, item.longitude];

            const [cidadeInicio, cidadeAtual] = await Promise.all([
                obterNomeCidade(startPoint[0], startPoint[1], item.country),
                obterNomeCidade(currPoint[0], currPoint[1], item.country)
            ]);

            const elStart = document.getElementById(`${prefix}-start`);
            if (elStart) elStart.innerText = cidadeInicio;

            const elCurr = document.getElementById(`${prefix}-curr`);
            if (elCurr) elCurr.innerText = cidadeAtual;

            return { cidadeInicio, cidadeAtual };
        }"""

new_calc_func = """        function calcularDistanciaKm(lat1, lon1, lat2, lon2) {
            const R = 6371; // Raio da Terra em km
            const dLat = (lat2 - lat1) * Math.PI / 180;
            const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                      Math.sin(dLon/2) * Math.sin(dLon/2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            return Math.round(R * c);
        }

        async function carregarCidadesVoo(item, prefix) {
            const startPoint = item.trajectory && item.trajectory.length > 0 ? item.trajectory[0] : [item.latitude, item.longitude];
            const currPoint = [item.latitude, item.longitude];

            const [cidadeInicio, cidadeAtual] = await Promise.all([
                obterNomeCidade(startPoint[0], startPoint[1], item.country),
                obterNomeCidade(currPoint[0], currPoint[1], item.country)
            ]);

            const distanciaKm = calcularDistanciaKm(startPoint[0], startPoint[1], currPoint[0], currPoint[1]);

            const elStart = document.getElementById(`${prefix}-start`);
            if (elStart) elStart.innerText = cidadeInicio;

            const elCurr = document.getElementById(`${prefix}-curr`);
            if (elCurr) elCurr.innerText = cidadeAtual;

            const elDist = document.getElementById(`${prefix}-dist`);
            if (elDist) elDist.innerText = distanciaKm.toLocaleString() + " km";

            return { cidadeInicio, cidadeAtual, distanciaKm };
        }"""

content = content.replace(old_calc_func, new_calc_func)

# Adiciona o campo de distância no popup do mapa
old_popup = """                            <b>COORDENADAS:</b> ${item.latitude}, ${item.longitude}<br>
                            <b>FORMA/TIPO:</b> ${shapeCfg.name}<br>"""

new_popup = """                            <b>COORDENADAS:</b> ${item.latitude}, ${item.longitude}<br>
                            <b>DISTÂNCIA PERCORRIDA:</b> <span style="color:#00ffaa; font-weight:bold;" id="pop-${keyId}-dist">Calculando...</span><br>
                            <b>FORMA/TIPO:</b> ${shapeCfg.name}<br>"""

content = content.replace(old_popup, new_popup)

# Adiciona o campo de distância no card da lateral
old_card = """                        <b>COORDENADAS:</b> <span class="coord-txt">${item.latitude}, ${item.longitude}</span><br>
                        <b>FORMA:</b> ${shapeCfg.name}<br>"""

new_card = """                        <b>COORDENADAS:</b> <span class="coord-txt">${item.latitude}, ${item.longitude}</span><br>
                        <b>DISTÂNCIA PERCORRIDA:</b> <span style="color:#00ffaa; font-weight:bold;" id="card-${keyId}-dist">Calculando...</span><br>
                        <b>FORMA:</b> ${shapeCfg.name}<br>"""

content = content.replace(old_card, new_card)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Cálculo e exibição da distância percorrida adicionados!")
