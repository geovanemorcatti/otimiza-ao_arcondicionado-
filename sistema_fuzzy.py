import numpy as np
import matplotlib.pyplot as plt

# Função manual para pertinência triangular
def calcular_pertinencia_triangular(x, a, b, c):
    # Garante que o cálculo siga a fórmula matemática manual
    return max(0, min((x - a) / (b - a), (c - x) / (c - b))) if a < x < c else 0

# Teste para a variável Temperatura (Fria: 10, 10, 22)
# Se a temperatura real for 15°C:
grau_frio = calcular_pertinencia_triangular(15, 10, 10, 22)
print(f"O grau de 'Frio' para 15°C é: {grau_frio}")

# Definição dos eixos (Universos de Discurso)
uni_temp = np.linspace(10, 40, 100)      # 10°C a 40°C
uni_umid = np.linspace(0, 100, 100)     # 0% a 100%
uni_pres = np.linspace(0, 20, 100)      # 0 a 20 pessoas
uni_saida = np.linspace(0, 100, 100)    # 0% a 100% de velocidade

# --- Bloco 2: Universos de Discurso (Item 3 do Relatório) ---
# Definimos o intervalo numérico de cada variável (Eixo X dos gráficos)

# Temperatura: de 10°C a 40°C
uni_temp = np.linspace(10, 40, 100)      

# Umidade: de 0% a 100%
uni_umid = np.linspace(0, 100, 100)     

# Presença de Pessoas: de 0 a 20 pessoas
uni_pres = np.linspace(0, 20, 100)      

# Saída - Velocidade do Ventilador: de 0% a 100% de potência
uni_saida = np.linspace(0, 100, 100)


# Base de Regras (Mínimo 10 regras - Requisito 5)
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

def motor_inferencia(fuzz_temp, fuzz_umid, fuzz_pres):
    ativacoes = []
    
    print("\n--- Graus de Ativação das Regras (Item 9) ---")
    for i, regra in enumerate(base_regras):
        # Pegamos o valor fuzzificado de cada entrada conforme a regra
        v1 = fuzz_temp[regra["temp"]]
        v2 = fuzz_umid[regra["umid"]]
        v3 = fuzz_pres[regra["pres"]]
        
        # Operador MIN para a conjunção "E" (Requisito de Mamdani)
        grau_ativacao = min(v1, v2, v3)
        
        ativacoes.append({"saida": regra["saida"], "valor": grau_ativacao})
        print(f"Regra {i+1}: Ativação = {grau_ativacao:.2f} -> Saída: {regra['saida']}")
        
    return ativacoes


# --- Bloco de Fuzzificação (Item 8 do Relatório) ---

def fuzzificacao(temp_val, umid_val, pres_val):
    # 1. Pertinência para Temperatura
    # Usando os pontos (a, b, c) definidos no Bloco 2
    fuzz_temp = {
        "Fria":      triangular(temp_val, 10, 10, 22),
        "Agradavel": triangular(temp_val, 18, 24, 30),
        "Quente":    triangular(temp_val, 26, 40, 40)
    }

    # 2. Pertinência para Umidade
    fuzz_umid = {
        "Baixa": triangular(umid_val, 0, 0, 40),
        "Media": triangular(umid_val, 30, 50, 70),
        "Alta":  triangular(umid_val, 60, 100, 100)
    }

    # 3. Pertinência para Presença de Pessoas
    fuzz_pres = {
        "Poucas":   triangular(pres_val, 0, 0, 8),
        "Moderada": triangular(pres_val, 5, 10, 15),
        "Muitas":   triangular(pres_val, 12, 20, 20)
    }

    return fuzz_temp, fuzz_umid, fuzz_pres

# --- EXEMPLO DE TESTE (Um dos 3 testes obrigatórios) ---
t_ent, u_ent, p_ent = 28, 65, 12  # Valores de exemplo

f_temp, f_umid, f_pres = fuzzificacao(t_ent, u_ent, p_ent)

print("--- Graus de Pertinência Obtidos (Item 8) ---")
print(f"Temperatura {t_ent}°C: {f_temp}")
print(f"Umidade {u_ent}%: {f_umid}")
print(f"Presença {p_ent} pessoas: {f_pres}")

# --- Bloco de Fuzzificação (Item 8 do Relatório) ---

def fuzzificacao(temp_val, umid_val, pres_val):
    # 1. Pertinência para Temperatura
    # Usando os pontos (a, b, c) definidos no Bloco 2
    fuzz_temp = {
        "Fria":      triangular(temp_val, 10, 10, 22),
        "Agradavel": triangular(temp_val, 18, 24, 30),
        "Quente":    triangular(temp_val, 26, 40, 40)
    }

    # 2. Pertinência para Umidade
    fuzz_umid = {
        "Baixa": triangular(umid_val, 0, 0, 40),
        "Media": triangular(umid_val, 30, 50, 70),
        "Alta":  triangular(umid_val, 60, 100, 100)
    }

    # 3. Pertinência para Presença de Pessoas
    fuzz_pres = {
        "Poucas":   triangular(pres_val, 0, 0, 8),
        "Moderada": triangular(pres_val, 5, 10, 15),
        "Muitas":   triangular(pres_val, 12, 20, 20)
    }

    return fuzz_temp, fuzz_umid, fuzz_pres

# --- EXEMPLO DE TESTE (Um dos 3 testes obrigatórios) ---
t_ent, u_ent, p_ent = 28, 65, 12  # Valores de exemplo

f_temp, f_umid, f_pres = fuzzificacao(t_ent, u_ent, p_ent)

print("--- Graus de Pertinência Obtidos (Item 8) ---")
print(f"Temperatura {t_ent}°C: {f_temp}")
print(f"Umidade {u_ent}%: {f_umid}")
print(f"Presença {p_ent} pessoas: {f_pres}")