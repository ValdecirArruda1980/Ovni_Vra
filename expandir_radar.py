with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Aumenta o número de alvos táticos gerados de 119 para 320
content = content.replace("for i in range(1, 120):", "for i in range(1, 321):")

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Quantidade de anomalias expandida para 300+ no radar!")
