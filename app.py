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

# Entrada da matriz de distâncias
st.subheader("Matriz de Distâncias")
st.markdown("Insira as distâncias entre os vértices. Use 'inf' para infinito (sem conexão direta).")
dist = []
for i in range(n):
    row = []
    cols = st.columns(n)
    for j in range(n):
        if i == j:
            val = 0
        else:
            val = cols[j].text_input(f"Distância {i+1} -> {j+1}", value="inf" if i != j else "0", key=f"dist_{i}_{j}")
            val = float('inf') if val.lower() == 'inf' else float(val)
        row.append(val)
    dist.append(row)

# Entrada da matriz de predecessores
st.subheader("Matriz de Predecessores")
st.markdown("Insira os predecessores iniciais. Use 0 para nenhum predecessor.")
pred = []
for i in range(n):
    row = []
    cols = st.columns(n)
    for j in range(n):
        if i == j:
            val = 0
        else:
            val = cols[j].number_input(f"Predecessor {i+1} -> {j+1}", value=0, key=f"pred_{i}_{j}")
        row.append(int(val))
    pred.append(row)

# Opção para mostrar passos
show_steps = st.checkbox("Mostrar passos intermediários")

# Armazenar no session_state
st.session_state["dist"] = dist
st.session_state["pred"] = pred
st.session_state["n"] = n
st.session_state["show_steps"] = show_steps

if st.button("Calcular"):
    try:
        # Validação de dimensões
        if len(dist) != n or any(len(row) != n for row in dist):
            st.error(f"A matriz deve ser {n}x{n}. Verifique os dados introduzidos.")
        elif len(pred) != n or any(len(row) != n for row in pred):
            st.error(f"A matriz de predecessores deve ser {n}x{n}.")
        else:
            # Execução do Algoritmo
            if show_steps:
                dist_final, pred_final, steps = floyd_warshall(dist, pred, trace=True)
            else:
                dist_final, pred_final = floyd_warshall(dist, pred)
                steps = None

            # Exibição dos Resultados em Abas
            tab1, tab2, tab3 = st.tabs(["📊 Matrizes Finais", "🕸️ Grafo", "🌡️ Heatmap"])

            with tab1:
                st.subheader("Matriz de Distâncias Final")
                st.dataframe(pd.DataFrame(dist_final))
                st.subheader("Matriz de Predecessores Final")
                st.dataframe(pd.DataFrame(pred_final))

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
                    st.write(step)

    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
