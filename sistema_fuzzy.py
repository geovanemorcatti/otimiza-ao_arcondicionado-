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