import numpy as np
import matplotlib.pyplot as plt

# --- FUNÇÃO DE PERTINÊNCIA (ITEM 5) ---
def calcular_triangulo(x, a, b, c):
    if x <= a or x >= c: return 0.0
    if a < x <= b:
        return (x - a) / (b - a) if a != b else 1.0
    if b < x < c:
        return (c - x) / (c - b) if b != c else 1.0
    return 0.0

# --- UNIVERSOS DE DISCURSO (ITEM 3) ---
eixo_temp = np.linspace(10, 40, 100)
eixo_umid = np.linspace(0, 100, 100)
eixo_pres = np.linspace(0, 20, 100)
eixo_saida = np.linspace(0, 100, 100)

# --- BASE DE REGRAS (ITEM 6) ---
minha_base_regras = [
    {"t": "Fria",      "u": "Baixa", "p": "Poucas",   "v": "Baixa"},
    {"t": "Fria",      "u": "Alta",  "p": "Muitas",   "v": "Baixa"},
    {"t": "Agradavel", "u": "Media", "p": "Moderada", "v": "Media"},
    {"t": "Agradavel", "u": "Baixa", "p": "Poucas",   "v": "Baixa"},
    {"t": "Quente",    "u": "Baixa", "p": "Poucas",   "v": "Media"},
    {"t": "Quente",    "u": "Media", "p": "Moderada", "v": "Alta"},
    {"t": "Quente",    "u": "Alta",  "p": "Muitas",   "v": "Alta"},
    {"t": "Fria",      "u": "Media", "p": "Muitas",   "v": "Media"},
    {"t": "Agradavel", "u": "Alta",  "p": "Muitas",   "v": "Alta"},
    {"t": "Quente",    "u": "Media", "p": "Poucas",   "v": "Media"}
]

# --- ITEM 12: GRÁFICO DAS ENTRADAS ---
def mostrar_graficos_entrada():
    plt.figure(figsize=(15, 4))
    
    # Temperatura
    plt.subplot(1, 3, 1)
    plt.plot(eixo_temp, [calcular_triangulo(x, 10, 10, 22) for x in eixo_temp], label="Fria")
    plt.plot(eixo_temp, [calcular_triangulo(x, 18, 24, 30) for x in eixo_temp], label="Agradável")
    plt.plot(eixo_temp, [calcular_triangulo(x, 26, 40, 40) for x in eixo_temp], label="Quente")
    plt.title("Temperatura (Item 12)")
    plt.legend()

    # Umidade
    plt.subplot(1, 3, 2)
    plt.plot(eixo_umid, [calcular_triangulo(x, 0, 0, 40) for x in eixo_umid], label="Baixa")
    plt.plot(eixo_umid, [calcular_triangulo(x, 30, 50, 70) for x in eixo_umid], label="Média")
    plt.plot(eixo_umid, [calcular_triangulo(x, 60, 100, 100) for x in eixo_umid], label="Alta")
    plt.title("Umidade (Item 12)")
    plt.legend()

    # Presença
    plt.subplot(1, 3, 3)
    plt.plot(eixo_pres, [calcular_triangulo(x, 0, 0, 8) for x in eixo_pres], label="Poucas")
    plt.plot(eixo_pres, [calcular_triangulo(x, 5, 10, 15) for x in eixo_pres], label="Moderada")
    plt.plot(eixo_pres, [calcular_triangulo(x, 12, 20, 20) for x in eixo_pres], label="Muitas")
    plt.title("Presença (Item 12)")
    plt.legend()
    
    plt.tight_layout()
    plt.show() # Esse comando faz o gráfico aparecer!

# --- LÓGICA FUZZY COMPLETA ---
def processar_fuzzy(val_t, val_u, val_p):
    # Fuzzificação
    g_t = {"Fria": calcular_triangulo(val_t, 10, 10, 22), "Agradavel": calcular_triangulo(val_t, 18, 24, 30), "Quente": calcular_triangulo(val_t, 26, 40, 40)}
    g_u = {"Baixa": calcular_triangulo(val_u, 0, 0, 40), "Media": calcular_triangulo(val_u, 30, 50, 70), "Alta": calcular_triangulo(val_u, 60, 100, 100)}
    g_p = {"Poucas": calcular_triangulo(val_p, 0, 0, 8), "Moderada": calcular_triangulo(val_p, 5, 10, 15), "Muitas": calcular_triangulo(val_p, 12, 20, 20)}

    # Inferência (Item 9) e Agregação (Item 10)
    agregado = np.zeros_like(eixo_saida)
    curvas_saida = {
        "Baixa": np.array([calcular_triangulo(x, 0, 0, 50) for x in eixo_saida]),
        "Media": np.array([calcular_triangulo(x, 25, 50, 75) for x in eixo_saida]),
        "Alta":  np.array([calcular_triangulo(x, 50, 100, 100) for x in eixo_saida])
    }

    for r in minha_base_regras:
        nivel_ativacao = min(g_t[r["t"]], g_u[r["u"]], g_p[r["p"]])
        if nivel_ativacao > 0:
            corte = np.minimum(nivel_ativacao, curvas_saida[r["v"]])
            agregado = np.maximum(agregado, corte)
    
    return agregado

def defuzzificar(area):
    if np.sum(area) == 0: return 0.0
    return np.sum(eixo_saida * area) / np.sum(area)

# --- EXECUÇÃO DOS 3 TESTES OBRIGATÓRIOS (ITEM 7) ---
if __name__ == "__main__":
    mostrar_graficos_entrada() # Primeiro gráfico obrigatório

    testes = [
        {"t": 12, "u": 15, "p": 1,  "label": "Frio e Vazio"},
        {"t": 22, "u": 45, "p": 5,  "label": "Agradável"},
        {"t": 38, "u": 90, "p": 18, "label": "Quente e Lotado"}
    ]

    for t in testes:
        area_final = processar_fuzzy(t["t"], t["u"], t["p"])
        valor_z = defuzzificar(area_final)
        
        print(f"Teste: {t['label']} -> Resultado: {valor_z:.2f}%")
        
        # Gráfico de Saída Agregada (Item 13)
        plt.figure(figsize=(7, 4))
        plt.fill_between(eixo_saida, 0, area_final, color='orange', alpha=0.5)
        plt.axvline(valor_z, color='red', linestyle='--', label=f'Centroide: {valor_z:.2f}%')
        plt.title(f"Saída Agregada: {t['label']} (Item 13)")
        plt.legend()
        plt.show() # Mostra um gráfico por vez