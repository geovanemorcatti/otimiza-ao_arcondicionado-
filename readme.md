
### Descrição do Problema: Controle de Climatização Inteligente

**1. O Objetivo**
O problema consiste em desenvolver um sistema de inferência fuzzy para controlar a **Velocidade do Ventilador** de um aparelho de ar-condicionado. O objetivo é manter o ambiente confortável de forma automática, economizando energia ao evitar que o motor funcione em potência máxima sem necessidade.

**2. As Variáveis de Entrada (3 variáveis, 3 funções cada)**[cite: 1]
Para que o sistema tome uma decisão precisa, ele avaliará:
*   **Temperatura Ambiente ($^\circ C$):** Para medir o calor atual do recinto.
    *   *Termos:* Fria, Agradável, Quente.
*   **Umidade Relativa (%):** Pois a umidade alta aumenta a sensação térmica de calor.
    *   *Termos:* Baixa, Média, Alta.
*   **Presença de Pessoas (Quantidade):** Quantas pessoas estão no local (fontes de calor humano).
    *   *Termos:* Poucas, Moderado, Muitas.

**3. A Variável de Saída (Mínimo 1)**[cite: 1]
*   **Velocidade do Ventilador (% da potência):** Define a força com que o ar será insuflado no ambiente.
    *   *Termos:* Baixa, Média, Alta.

**4. Justificativa da Modelagem (Mamdani)**[cite: 1]
Será utilizado o modelo de **Mamdani** pois ele permite que tanto as entradas quanto as saídas sejam representadas por conjuntos fuzzy (termos linguísticos), o que facilita a interpretação humana das regras de controle (ex: "Se está Quente e com Muitas Pessoas, então a Velocidade é Alta")[cite: 1].

**5. Universo de Discurso (Sugestão para o seu código)**[cite: 1]
*   **Temperatura:** 10°C a 40°C.
*   **Umidade:** 0% a 100%.
*   **Presença:** 0 a 20 pessoas.
*   **Velocidade (Saída):** 0% a 100%.

---

### Exemplo de Base de Regras (Sugestão para compor as 10 obrigatórias)[cite: 1]:
1.  **SE** Temperatura é Quente **E** Presença é Muitas **ENTÃO** Velocidade é Alta.
2.  **SE** Temperatura é Fria **E** Umidade é Baixa **ENTÃO** Velocidade é Baixa.
3.  **SE** Temperatura é Agradável **E** Presença é Moderada **ENTÃO** Velocidade é Média.
*(Você deve completar até chegar em pelo menos 10 regras no seu trabalho)*[cite: 1].


definiçao do problema 


Com a Descrição do Problema definida, o próximo passo essencial é a Modelagem das Variáveis, onde você define os limites numéricos (Universos de Discurso) e as "curvas" (Funções de Pertinência) para cada variável.  Aqui está o planejamento detalhado para as suas variáveis e as funções que você precisará implementar manualmente no código:1. Definição dos Universos de DiscursoVocê precisará definir os intervalos numéricos que seu sistema aceita:  Temperatura ($T$): $[10, 40]$ $^\circ\text{C}$  Umidade ($U$): $[0, 100]$ $\%$  Presença ($P$): $[0, 20]$ pessoas  Velocidade Saída ($V$): $[0, 100]$ $\%$ de potência  2. Funções de Pertinência (Implementação Manual)Como o professor exige que a implementação seja feita "linha por linha", a forma mais simples é criar funções para Pertinência Triangular.  A fórmula para uma função triangular definida por três pontos $(a, b, c)$ é:$$f(x; a, b, c) = \max\left(0, \min\left(\frac{x - a}{b - a}, \frac{c - x}{c - b}\right)\right)$$Sugestão de Distribuição para a Temperatura ($T$):Fria: $[10, 10, 22]$ (Triangular iniciando no limite mínimo)  Agradável: $[18, 24, 30]$  Quente: $[26, 40, 40]$ (Triangular terminando no limite máximo)  Dica de código: Crie uma função Python chamada triangular(x, a, b, c) que retorne o valor de pertinência entre $0$ e $1$.  3. A Base de Regras (Mínimo 10)Aqui estão as 10 regras que você deve incluir no seu documento e código:  SE (Temp: Fria) E (Umidade: Baixa) ENTÃO (Velocidade: Baixa)  SE (Temp: Fria) E (Umidade: Alta) ENTÃO (Velocidade: Baixa)  SE (Temp: Agradável) E (Umidade: Média) ENTÃO (Velocidade: Baixa)  SE (Temp: Agradável) E (Presença: Poucas) ENTÃO (Velocidade: Baixa)  SE (Temp: Agradável) E (Presença: Muitas) ENTÃO (Velocidade: Média)  SE (Temp: Quente) E (Umidade: Baixa) ENTÃO (Velocidade: Média)  SE (Temp: Quente) E (Umidade: Alta) ENTÃO (Velocidade: Alta)  SE (Temp: Quente) E (Presença: Muitas) ENTÃO (Velocidade: Alta)  SE (Temp: Fria) E (Presença: Muitas) ENTÃO (Velocidade: Média)  SE (Temp: Quente) E (Presença: Poucas) ENTÃO (Velocidade: Média)  