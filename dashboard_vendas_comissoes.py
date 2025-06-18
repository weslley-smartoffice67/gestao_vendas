
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from fpdf import FPDF

# Configuração inicial obrigatória
st.set_page_config(page_title="Dashboard de Vendas e Comissões", layout="wide")

# Autenticação simples
st.sidebar.title("🔐 Login")
username = st.sidebar.text_input("Usuário")
password = st.sidebar.text_input("Senha", type="password")
if username != "teste01" or password != "teste01@":
    st.warning("Informe usuário e senha válidos.")
    st.stop()

st.title("📊 Dashboard de Vendas e Comissões")

# Upload do arquivo
arquivo = st.file_uploader("📁 Envie a planilha de vendas", type=["xlsx"])
if arquivo:
    df = pd.read_excel(arquivo)

    # Filtros
    with st.sidebar:
        st.header("📅 Filtros")
        meses = sorted(df["Mês"].unique())
        familias = sorted(df["Família"].unique())
        mes_filtro = st.multiselect("Selecione o(s) mês(es):", meses, default=meses)
        familia_filtro = st.multiselect("Selecione o(s) produtos:", familias, default=familias)

    # Aplicar filtros
    df_filt = df[df["Mês"].isin(mes_filtro) & df["Família"].isin(familia_filtro)]

    # KPIs
    total_vendas = df_filt["Valor da Venda"].sum()
    total_comissao = df_filt["Comissão (R$)"].sum()

    col1, col2 = st.columns(2)
    col1.metric("💰 Venda Total", f"R$ {total_vendas:,.2f}")
    col2.metric("🎯 Comissão Total", f"R$ {total_comissao:,.2f}")

    # Gráfico de linha - venda por mês
    vendas_mes = df_filt.groupby("Mês")["Valor da Venda"].sum().reset_index()
    fig_linha = px.line(vendas_mes, x="Mês", y="Valor da Venda", markers=True, title="Venda Total por Mês")
    fig_linha.update_traces(text=df_filt["Valor da Venda"], texttemplate="R$ %{y:,.2f}")

    # Gráfico de dispersão - Família x Comissão
    fig_disp = px.scatter(df_filt, x="Família", y="Comissão (R$)", size="Comissão (R$)",
                          title="Dispersão de Comissão por Produto", color="Família")
    fig_disp.update_traces(marker=dict(sizemode='area', line_width=2))

    # Ranking por venda
    vendas_familia = df_filt.groupby("Família")["Valor da Venda"].sum().reset_index()
    fig_rank_venda = px.bar(vendas_familia.sort_values("Valor da Venda", ascending=False),
                            x="Família", y="Valor da Venda", text_auto=".2s", title="Ranking de Produtos por Venda")

    # Ranking por comissão
    comissao_familia = df_filt.groupby("Família")["Comissão (R$)"].sum().reset_index()
    fig_rank_comissao = px.bar(comissao_familia.sort_values("Comissão (R$)", ascending=False),
                               x="Família", y="Comissão (R$)", text_auto=".2s", title="Ranking de Produtos por Comissão")

    st.markdown("---")
    col_linha, col_disp = st.columns(2)
    col_linha.plotly_chart(fig_linha, use_container_width=True)
    col_disp.plotly_chart(fig_disp, use_container_width=True)

    col_r1, col_r2 = st.columns(2)
    col_r1.plotly_chart(fig_rank_venda, use_container_width=True)
    col_r2.plotly_chart(fig_rank_comissao, use_container_width=True)

    # Exportar PDF
    def gerar_pdf(df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Resumo de Vendas e Comissões", ln=True, align="C")
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Venda Total: R$ {df['Valor da Venda'].sum():,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Comissão Total: R$ {df['Comissão (R$)'].sum():,.2f}", ln=True)
        pdf.ln(10)

        for _, row in df.iterrows():
            linha = f"{row['Mês']} - {row['Família']}: Venda R$ {row['Valor da Venda']:,.2f} | Comissão R$ {row['Comissão (R$)']:,.2f}"
            pdf.cell(200, 10, txt=linha.encode('latin-1', 'ignore').decode('latin-1'), ln=True)

        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        return buffer

    st.markdown("---")
    if st.button("📤 Baixar Relatório em PDF"):
        pdf_buffer = gerar_pdf(df_filt)
        st.download_button("📄 Clique aqui para baixar", data=pdf_buffer.read(),
                           file_name="relatorio_vendas_comissao.pdf")
