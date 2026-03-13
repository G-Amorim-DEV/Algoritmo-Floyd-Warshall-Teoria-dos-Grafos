# Projeto Educacional de Grafos com Floyd-Warshall

Este repositório contém uma implementação do algoritmo de Floyd-Warshall
para cálculo de caminhos mínimos em grafos.

## Estrutura

- `floyd.py` — algoritmo principal com detecção de ciclos negativos.
- `main.py` — CLI simples para inserir matrizes via terminal.
- `app.py` — interface Streamlit interativa.
- `graph_visualization.py` — desenho do grafo usando NetworkX.
- `data_inout.py` — exemplo de heatmap usando Seaborn.
- `requirements.txt` — dependências do projeto.
- `tests/` — testes automatizados com pytest.

## Como usar

### Instalação
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### CLI
```bash
python main.py
``` 
Digite o número de vértices e as matrizes conforme solicitado.

### Interface web
```bash
streamlit run app.py
```

### Testes
```bash
pytest -q
```

## Como o algoritmo funciona

O Floyd–Warshall utiliza programação dinâmica para construir
progressivamente a menor distância entre todos os pares
(i,j) de vértices. O algoritmo mantém duas matrizes:

1. **dist** – distâncias atuais entre vértices.
2. **pred** – predecessor imediato em um caminho mínimo.

Em cada passo `k` o vértice `k` é considerado como um possível ponto
intermediário entre `i` e `j`, e a matriz `dist[i][j]` é atualizada se
`dist[i][k] + dist[k][j]` for menor. Repetindo para todos os `k` resulta
no valor final de menores distâncias.

A aplicação web permite marcar a opção **Mostrar etapas intermediárias**
para inspecionar a matriz de distâncias após cada iteração de `k`, o que
é útil para entender ou demonstrar o funcionamento do método.

## Sugestões de melhorias
- Leitura/ gravação de matrizes em arquivos (CSV, JSON).
- Exportação dos resultados para CSV/PDF.
- Melhoria da visualização: trajetos individuais, pesos negativos.
- Suporte a grafos não dirigidos ou ponderações variáveis.
- Empacotar como pacote instalável (`setup.py`/`pyproject.toml`).
- Adicionar CI (GitHub Actions) para rodar testes automaticamente.
