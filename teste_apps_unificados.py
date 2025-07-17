import streamlit as st
import pandas as pd
import requests
from openpyxl import load_workbook
from io import BytesIO
from datetime import datetime
from PIL import Image

# ========================= CONFIG GERAL =========================
st.set_page_config(
    page_title="Operações - Lojas MIMI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================= ESTILO PERSONALIZADO =========================
st.markdown("""
    <style>
    .stButton > button {
        background-color: #0047AB;
        color: white;
        font-weight: bold;
    }
    .stDownloadButton > button {
        background-color: #28A745;
        color: white;
        font-weight: bold;
    }
    .stSelectbox, .stTextInput, .stNumberInput {
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .big-font {
        font-size: 22px !important;
    }
    .small-font {
        font-size: 14px;
        color: gray;
    }
    </style>
""", unsafe_allow_html=True)

# ========================= TÍTULO PRINCIPAL =========================
st.title("🧠 Sistema de Operações - Lojas MIMI")

# ========================= MENU LATERAL =========================
logo = Image.open("logo_lojas_mimi.jpeg")
st.sidebar.image(logo, use_container_width=True)
st.sidebar.markdown("## 📁 Menu de Operações")
menu = st.sidebar.radio(
    "Escolha a operação:",
    ["♻️ Processo de Trocas", "🛍️ Processo de Pedidos", "📦 Transferência entre Lojas", "🔍 Pesquisa de Produtos"]
)

# ========================= FUNÇÕES COMUNS =========================
@st.cache_data(show_spinner=False)
def carregar_csv_combinado():
    url = "https://raw.githubusercontent.com/LojasMimi/transferencia_loja/refs/heads/main/cad_concatenado.csv"
    df = pd.read_csv(url, dtype=str).fillna("")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed", case=False)]
    df.columns = df.columns.str.strip().str.upper()

    def dedup_columns(cols):
        seen = {}
        new_cols = []
        for col in cols:
            if col in seen:
                seen[col] += 1
                new_cols.append(f"{col}_{seen[col]}")
            else:
                seen[col] = 0
                new_cols.append(col)
        return new_cols

    df.columns = dedup_columns(df.columns)

    if "SITUACAO" in df.columns:
        df["SITUACAO"] = df["SITUACAO"].str.replace("ç", "c", regex=False)
    if "DESCRIÇÃO" in df.columns:
        df["DESCRIÇÃO"] = df["DESCRIÇÃO"].str.replace("ç", "c", regex=False)

    return df

def buscar_produto(codigo, coluna, df):
    codigo = str(codigo).strip()
    resultado = df[df[coluna].astype(str).str.strip() == codigo]
    return resultado.iloc[0] if not resultado.empty else None

# ========================= APP 1: TROCAS =========================
def app_trocas():
    # ... (mantém igual)
    pass

# ========================= APP 2: PEDIDOS =========================
def app_pedidos():
    # ... (mantém igual)
    pass

# ========================= APP 3: TRANSFERÊNCIAS =========================
def app_transferencias():
    # ... (mantém igual)
    pass

# ========================= APP 4: PESQUISA DE PRODUTOS (API) =========================
def app_pesquisa():
    st.header("🔍 Pesquisa de Produtos (API Varejo Fácil)")
    st.divider()

    st.markdown("<p class='small-font' style='text-align: center;'>Consulta em tempo real na base do Varejo Fácil</p>", unsafe_allow_html=True)

    codigo_barras = st.text_input("📦 Digite o código de barras do produto", placeholder="Ex: 7891234567890")

    if st.button("🔎 Consultar Produto"):
        if not codigo_barras.strip():
            st.warning("⚠️ Por favor, digite um código de barras válido.")
        else:
            url_1 = f"https://lojasmimi.varejofacil.com/api/v1/produto/produtos/consulta/0{codigo_barras}"

            headers = {
                'x-api-key': st.secrets.api.x_api_key,
                'Cookie': st.secrets.api.cookie
            }

            try:
                response_1 = requests.get(url_1, headers=headers)

                if response_1.status_code == 200:
                    dados_produto = response_1.json()

                    if 'id' in dados_produto and 'descricao' in dados_produto:
                        produto_id = dados_produto['id']
                        descricao = dados_produto['descricao']

                        st.success("✅ Produto encontrado com sucesso!")
                        st.markdown(f"<div class='big-font'><strong>📄 Descrição:</strong> {descricao}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='small-font'>🆔 ID do Produto: {produto_id}</div>", unsafe_allow_html=True)

                        url_2 = f"https://lojasmimi.varejofacil.com/api/v1/produto/produtos/{produto_id}/precos"
                        response_2 = requests.get(url_2, headers=headers)

                        if response_2.status_code == 200:
                            lista_precos = response_2.json()
                            preco_loja_1 = next((item for item in lista_precos if item.get("lojaId") == 1), None)

                            if preco_loja_1:
                                preco_venda = preco_loja_1.get("precoVenda1", "N/A")
                                custo = preco_loja_1.get("custoProduto", "N/A")

                                with st.expander("💰 Ver detalhes de preço"):
                                    st.write(f"**Preço de Venda:** R$ {preco_venda:.2f}" if isinstance(preco_venda, (int, float)) else f"**Preço de Venda:** {preco_venda}")
                                    st.write(f"**Custo do Produto:** R$ {custo:.2f}" if isinstance(custo, (int, float)) else f"**Custo do Produto:** {custo}")
                            else:
                                st.info("ℹ️ Nenhuma informação de preço disponível para esta loja.")
                        else:
                            st.error(f"❌ Erro ao consultar preços: {response_2.status_code}")
                    else:
                        st.warning("🚫 Produto não encontrado ou dados incompletos.")
                else:
                    st.error(f"❌ Erro ao buscar produto: Código {response_1.status_code}")
            except Exception as e:
                st.exception(f"Erro inesperado: {e}")

# ========================= EXECUTAR OPERAÇÃO =========================
if menu == "♻️ Processo de Trocas":
    app_trocas()
elif menu == "🛍️ Processo de Pedidos":
    app_pedidos()
elif menu == "📦 Transferência entre Lojas":
    app_transferencias()
elif menu == "🔍 Pesquisa de Produtos":
    app_pesquisa()

# ========================= RODAPÉ =========================
st.markdown("""
<hr style="margin-top: 40px; margin-bottom: 10px;">
<div style='text-align: center; font-size: 13px; color: gray;'>
Desenvolvido por <strong>Pablo</strong> · Lojas MIMI © 2025
</div>
""", unsafe_allow_html=True)
