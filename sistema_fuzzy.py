import numpy as np
import matplotlib.pyplot as plt

# --- Bloco 1: Funções de Pertinência (Item 5) ---
# Implementação robusta para evitar divisão por zero em conjuntos de borda
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a) if a != b else 1.0
    if b < x < c:
        return (c - x) / (c - b) if b != c else 1.0
    return 0.0

# --- Bloco 2: Universos de Discurso (Item 3) ---
uni_temp = np.linspace(10, 40, 100)      # 10°C a 40°C
uni_umid = np.linspace(0, 100, 100)     # 0% a 100%
uni_pres = np.linspace(0, 20, 100)      # 0 a 20 pessoas
uni_saida = np.linspace(0, 100, 100)    # 0% a 100% (Saída)

# --- Bloco 3: Base de Regras (Item 6) ---
base_regras = [
    {"temp": "Fria",      "umid": "Baixa", "pres": "Poucas",   "saida": "Baixa"},
    {"temp": "Fria",      "umid": "Alta",  "pres": "Muitas",   "saida": "Baixa"},
    {"temp": "Agradavel", "umid": "Media", "pres": "Moderada", "saida": "Media"},
    {"temp": "Agradavel", "umid": "Baixa", "pres": "Poucas",   "saida": "Baixa"},
    {"temp": "Quente",    "umid": "Baixa", "pres": "Poucas",   "saida": "Media"},
    {"temp": "Quente",    "umid": "Media", "pres": "Moderada", "saida": "Alta"},
    {"temp": "Quente",    "umid": "Alta",  "pres": "Muitas",   "saida": "Alta"},
    {"temp": "Fria",      "umid": "Media", "pres": "Muitas",   "saida": "Media"},
    {"temp": "Agradavel", "umid": "Alta",  "pres": "Muitas",   "saida": "Alta"},
    {"temp": "Quente",    "umid": "Media", "pres": "Poucas",   "saida": "Media"}
]

# --- Bloco de Fuzzificação (Item 8) ---
def fuzzificacao(temp_val, umid_val, pres_val):
    f_temp = {
        "Fria":      triangular(temp_val, 10, 10, 22),
        "Agradavel": triangular(temp_val, 18, 24, 30),
        "Quente":    triangular(temp_val, 26, 40, 40)
    }
    f_umid = {
        "Baixa": triangular(umid_val, 0, 0, 40),
        "Media": triangular(umid_val, 30, 50, 70),
        "Alta":  triangular(umid_val, 60, 100, 100)
    }
    f_pres = {
        "Poucas":   triangular(pres_val, 0, 0, 8),
        "Moderada": triangular(pres_val, 5, 10, 15),
        "Muitas":   triangular(pres_val, 12, 20, 20)
    }
    return f_temp, f_umid, f_pres

# --- Bloco 4: Motor de Inferência (Item 9) ---
def motor_inferencia(f_temp, f_umid, f_pres):
    ativacoes = []
    print("\n--- Graus de Ativação das Regras (Item 9) ---")
    for i, regra in enumerate(base_regras):
        v1 = f_temp[regra["temp"]]
        v2 = f_umid[regra["umid"]]
        v3 = f_pres[regra["pres"]]
        
        # Operador MIN (Mamdani)
        grau_ativacao = min(v1, v2, v3)
        ativacoes.append({"saida": regra["saida"], "valor": grau_ativacao})
        print(f"Regra {i+1}: Ativação = {grau_ativacao:.2f} -> Saída: {regra['saida']}")
    return ativacoes

# --- EXECUÇÃO DO TESTE ---
t_ent, u_ent, p_ent = 28, 65, 12 

# Passo 1: Fuzzificação
f_t, f_u, f_p = fuzzificacao(t_ent, u_ent, p_ent)
print("--- Graus de Pertinência (Item 8) ---")
print(f"Temp {t_ent}: {f_t}\nUmid {u_ent}: {f_u}\nPres {p_ent}: {f_p}")

# Passo 2: Inferência
lista_ativacoes = motor_inferencia(f_t, f_u, f_p)