import streamlit as st
import pandas as pd
import floyd
import graph_visualization

st.title("Floyd-Warshall Interactive")

# brief description of the algorithm and what the app shows
st.markdown(
    """
    **Algoritmo de Floyd–Warshall**

    O Floyd–Warshall é um algoritmo de programação dinâmica que calcula os
    caminhos mais curtos entre *todos* os pares de vértices em um grafo
    direcionado. Dada uma matriz de adjacência de pesos (onde um valor
    grande ou infinito representa ausência de aresta), o método itera sobre
    todos os vértices intermediários `k` e tenta melhorar a distância entre
    cada par `(i, j)` usando `k` como ponto de passagem.

    Este aplicativo permite fornecer as matrizes de distâncias e de
    predecessores e exibe as versões finais após a computação, além de
    ilustrar o grafo resultante.
    """
)

# allow user to directly upload CSV files for matrices
upload_dist = st.file_uploader("Arquivo CSV da matriz de distâncias", type=["csv"])
upload_pred = st.file_uploader("Arquivo CSV da matriz de predecessores", type=["csv"])

n = st.number_input("Número de vértices", min_value=1, step=1)

# parse text areas if uploads not provided
if upload_dist:
    try:
        dist_df = pd.read_csv(upload_dist, header=None)
        dist = dist_df.values.tolist()
    except Exception as e:
        st.error(f"Erro ao ler matriz de distâncias: {e}")
        dist = None
else:
    dist = None

if upload_pred:
    try:
        pred_df = pd.read_csv(upload_pred, header=None)
        pred = pred_df.values.tolist()
    except Exception as e:
        st.error(f"Erro ao ler matriz de predecessores: {e}")
        pred = None
else:
    pred = None

# allow manual text input if files not provided
if dist is None:
    st.write("Digite a matriz de distâncias (linhas separadas por ENTER, valores por espaço)")
    dist_input = st.text_area("Matriz de distâncias")
    try:
        dist = [list(map(int, line.split())) for line in dist_input.strip().splitlines() if line]
    except ValueError:
        dist = None

if pred is None:
    st.write("Digite a matriz de predecessores (mesmo formato)")
    pred_input = st.text_area("Matriz de predecessores")
    try:
        pred = [list(map(int, line.split())) for line in pred_input.strip().splitlines() if line]
    except ValueError:
        pred = None

# option to see how the algorithm proceeds
show_steps = st.checkbox("Mostrar etapas intermediárias")

if st.button("Calcular"):
    try:
        if dist is None or pred is None:
            st.error("Matrizes incompletas")
        elif len(dist) != n or len(pred) != n:
            st.error("Dimensões das matrizes não batem com o número de vértices")
        else:
            if show_steps:
                dist, pred, steps = floyd.floyd_warshall(dist, pred, trace=True)
            else:
                dist, pred = floyd.floyd_warshall(dist, pred)
                steps = None

            df_dist = pd.DataFrame(dist)
            df_pred = pd.DataFrame(pred)
            st.subheader("Matriz de distâncias")
            st.dataframe(df_dist)
            st.subheader("Matriz de predecessores")
            st.dataframe(df_pred)

            if show_steps and steps is not None:
                st.subheader("Etapas intermediárias")
                for k, mat in enumerate(steps):
                    st.markdown(f"**Após inserir vértice intermediário {k}**")
                    st.dataframe(pd.DataFrame(mat))

            st.subheader("Grafo gerado")
            fig = graph_visualization.criar_grafo(dist)
            st.pyplot(fig)

            # allow download of results
            csv1 = df_dist.to_csv(index=False).encode('utf-8')
            csv2 = df_pred.to_csv(index=False).encode('utf-8')
            st.download_button("Download dist CSV", csv1, "distancias.csv", "text/csv")
            st.download_button("Download pred CSV", csv2, "predecessores.csv", "text/csv")
    except Exception as e:
        st.error(f"Erro: {e}")
