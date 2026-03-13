import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from floyd import floyd_warshall
from graph_visualization import criar_grafo

st.title("Algoritmo de Floyd-Warshall")
st.markdown("""
Este aplicativo calcula os caminhos mais curtos entre todos os pares de vértices em um grafo usando o algoritmo de Floyd-Warshall.
""")

# Entrada do número de vértices
n = st.number_input("Número de vértices", min_value=2, max_value=10, value=3, step=1)

# Função para parsear a matriz
def parse_matrix(text, n):
    lines = text.strip().split('\n')
    if len(lines) != n:
        raise ValueError(f"A matriz deve ter {n} linhas.")
    matrix = []
    for line in lines:
        row = []
        parts = line.split()
        if len(parts) != n:
            raise ValueError(f"Cada linha deve ter {n} valores.")
        for val in parts:
            if val.lower() in ['inf', 'infinity']:
                row.append(float('inf'))
            else:
                row.append(float(val))
        matrix.append(row)
    return matrix

# Entrada da matriz de distâncias
st.subheader("Matriz de Distâncias")
st.markdown("Digite a matriz de distâncias. Use 'inf' para infinito (sem conexão direta). Separe os valores com espaços e as linhas com enter.")
default_dist = "\n".join([" ".join(["0" if i == j else "inf" for j in range(n)]) for i in range(n)])
dist_text = st.text_area("Matriz de distâncias", value=default_dist, height=150, key="dist_text")

# Opção para mostrar passos
show_steps = st.checkbox("Mostrar passos intermediários")

if st.button("Calcular"):
    try:
        # Parse da matriz
        dist = parse_matrix(dist_text, n)
        
        # Validação de dimensões
        if len(dist) != n or any(len(row) != n for row in dist):
            st.error(f"A matriz deve ser {n}x{n}.")
        else:
            # Execução do Algoritmo
            if show_steps:
                dist_final, pred_final, steps = floyd_warshall(dist, trace=True)
            else:
                dist_final, pred_final = floyd_warshall(dist)
                steps = None

            # Exibição dos Resultados em Abas
            tab1, tab2, tab3 = st.tabs(["📊 Matrizes Finais", "🕸️ Grafo", "🌡️ Heatmap"])

            with tab1:
                st.subheader("Matriz de Distâncias Final")
                st.dataframe(pd.DataFrame(dist_final))
                st.subheader("Matriz de Predecessores Final")
                # Substituir None por -1 para exibição
                pred_display = [[-1 if p is None else p for p in row] for row in pred_final]
                st.dataframe(pd.DataFrame(pred_display))

            with tab2:
                st.subheader("Visualização do Grafo")
                fig_grafo = criar_grafo(dist_final)
                st.pyplot(fig_grafo)

            with tab3:
                st.subheader("Heatmap de Intensidade de Distâncias")
                fig_heat, ax = plt.subplots()
                df_heat = pd.DataFrame(dist_final).replace(float('inf'), 999)
                sns.heatmap(df_heat, annot=True, cmap="YlOrRd", ax=ax)
                st.pyplot(fig_heat)

            if show_steps and steps:
                st.subheader("Passos Intermediários")
                for step in steps:
                    st.write(pd.DataFrame(step))

    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
