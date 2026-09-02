with open("static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui o trecho que renderiza os cards para calcular a distância e geolocalização automaticamente ao carregar
old_card_loop = """                    result.data.forEach((item, idx) => {
                        const isNasa = item.source.includes("NASA");
                        const shapeCfg = getShapeConfig(item.shape, isNasa);
                        const keyId = `ufo-${idx}`;"""

new_card_loop = """                    result.data.forEach((item, idx) => {
                        const isNasa = item.source.includes("NASA");
                        const shapeCfg = getShapeConfig(item.shape, isNasa);
                        const keyId = `ufo-${idx}`;

                        // Dispara o cálculo em background para preencher o card imediatamente
                        setTimeout(() => {
                            carregarCidadesVoo(item, `card-${keyId}`);
                        }, idx * 50);"""

content = content.replace(old_card_loop, new_card_loop)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Cálculo automático para todos os cards da lista lateral ativado!")
