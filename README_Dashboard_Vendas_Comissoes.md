# 📊 Dashboard de Vendas e Comissões

Este é um aplicativo desenvolvido em Streamlit para análise interativa de vendas e comissões por produto e por mês.

## 🔐 Login

Acesso padrão:

- **Usuário:** `teste01`
- **Senha:** `teste01@`

## 📦 Funcionalidades

- Upload de planilha Excel com colunas:
  - `Mês`
  - `Família`
  - `Valor da Venda`
  - `Comissão (%)`
  - `Comissão (R$)`
- Filtros por **mês** e **produto**
- Indicadores consolidados:
  - Venda total
  - Comissão total
- Gráficos:
  - Linha: evolução de vendas por mês
  - Dispersão: comissão por produto
  - Barras: ranking por venda e por comissão
- Exportação final em PDF com resumo detalhado

## ▶️ Como usar

1. Faça o upload da planilha no formato `.xlsx`
2. Use os filtros laterais para visualizar os dados
3. Clique em **Baixar Relatório em PDF** para exportar

## 🚀 Publicação

Para publicar no [Streamlit Cloud](https://streamlit.io/cloud), inclua neste repositório:

- `dashboard_vendas_comissoes.py`
- `requirements.txt`

---

Desenvolvido por Smart Office Consultoria.