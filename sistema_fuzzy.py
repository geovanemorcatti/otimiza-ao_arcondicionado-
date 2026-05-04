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
# --- Bloco 5: Agregação (Item 10 do Relatório) ---

def agregacao(lista_ativacoes, uni_saida):
    # 1. Definimos os conjuntos fuzzy de saída para todo o universo (eixo X)
    saida_baixa = np.array([triangular(x, 0, 0, 50) for x in uni_saida])
    saida_media = np.array([triangular(x, 25, 50, 75) for x in uni_saida])
    saida_alta  = np.array([triangular(x, 50, 100, 100) for x in uni_saida])

    # 2. Inicializamos o conjunto agregado com zeros
    agregado = np.zeros_like(uni_saida)

    # 3. Aplicamos as ativações de cada regra (Item 9 -> Item 10)
    for regra in lista_ativacoes:
        valor_ativacao = regra["valor"]
        
        if regra["saida"] == "Baixa":
            # "Corta" o triângulo no nível da ativação (operador MIN)
            corte = np.minimum(valor_ativacao, saida_baixa)
        elif regra["saida"] == "Media":
            corte = np.minimum(valor_ativacao, saida_media)
        else: # Alta
            corte = np.minimum(valor_ativacao, saida_alta)
        
        # Agrega usando o operador MAX (conforme permitido pelo documento)
        agregado = np.maximum(agregado, corte)
        
    return agregado

# --- CONTINUANDO O TESTE ---
# Gerando a saída agregada
saida_final_agregada = agregacao(lista_ativacoes, uni_saida)

print("\n--- Saída Agregada (Item 10) ---")
print(f"Vetor de agregação gerado com {len(saida_final_agregada)} pontos.")


# --- Bloco 6: Defuzzificação (Item 11 do Relatório) ---

def defuzzificacao_centroide(uni_saida, agregado):
    # Cálculo do Centroide: Soma(x * pertinencia) / Soma(pertinencia)
    numerador = np.sum(uni_saida * agregado)
    denominador = np.sum(agregado)
    
    # Tratamento caso nenhuma regra seja ativada (evita divisão por zero)
    if denominador == 0:
        return 0.0
    
    return numerador / denominador

# --- FINALIZANDO O TESTE ---
valor_final = defuzzificacao_centroide(uni_saida, saida_final_agregada)

print("\n--- Resultado Final (Item 11) ---")
print(f"Valor defuzzificado: {valor_final:.2f}% de velocidade do ventilador.")


def plotar_entradas(uni_temp, uni_umid, uni_pres):
    plt.figure(figsize=(15, 5))

    # Gráfico de Temperatura
    plt.subplot(1, 3, 1)
    # Calculamos os Ys para cada ponto do X (universo)
    y_fria = [triangular(x, 10, 10, 22) for x in uni_temp]
    y_agra = [triangular(x, 18, 24, 30) for x in uni_temp]
    y_quen = [triangular(x, 26, 40, 40) for x in uni_temp]
    
    plt.plot(uni_temp, y_fria, label='Fria')
    plt.plot(uni_temp, y_agra, label='Agradável')
    plt.plot(uni_temp, y_quen, label='Quente')
    plt.title('Pertinência: Temperatura (Item 12)')
    plt.legend()

    # Gráfico de Umidade
    plt.subplot(1, 3, 2)
    y_baixa = [triangular(x, 0, 0, 40) for x in uni_umid]
    y_media = [triangular(x, 30, 50, 70) for x in uni_umid]
    y_alta  = [triangular(x, 60, 100, 100) for x in uni_umid]
    
    plt.plot(uni_umid, y_baixa, label='Baixa')
    plt.plot(uni_umid, y_media, label='Média')
    plt.plot(uni_umid, y_alta, label='Alta')
    plt.title('Pertinência: Umidade (Item 12)')
    plt.legend()

    # Gráfico de Presença
    plt.subplot(1, 3, 3)
    y_pouc = [triangular(x, 0, 0, 8) for x in uni_pres]
    y_mode = [triangular(x, 5, 10, 15) for x in uni_pres]
    y_muit = [triangular(x, 12, 20, 20) for x in uni_pres]
    
    plt.plot(uni_pres, y_pouc, label='Poucas')
    plt.plot(uni_pres, y_mode, label='Moderada')
    plt.plot(uni_pres, y_muit, label='Muitas')
    plt.title('Pertinência: Presença (Item 12)')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Chamar a função
plotar_entradas(uni_temp, uni_umid, uni_pres)


def plotar_saida_agregada(uni_saida, agregado, valor_defuzz):
    plt.figure(figsize=(8, 5))
    
    # Desenha a área sombreada (Item 13)
    plt.fill_between(uni_saida, 0, agregado, facecolor='orange', alpha=0.5, label='Saída Agregada')
    
    # Desenha a linha do valor final defuzzificado (Item 11)
    plt.axvline(x=valor_defuzz, color='red', linestyle='--', label=f'Centroide: {valor_defuzz:.2f}%')
    
    plt.title('Saída Agregada antes da Defuzzificação (Item 13)')
    plt.xlabel('Velocidade do Ventilador (%)')
    plt.ylabel('Grau de Pertinência')
    plt.legend()
    plt.grid(True)
    plt.show()

# Chamar a função usando os dados dos blocos anteriores
plotar_saida_agregada(uni_saida, saida_final_agregada, valor_final)