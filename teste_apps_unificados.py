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
    st.header("♻️ Processo de Trocas")
    st.divider()

    if "trocas_dados" not in st.session_state:
        st.session_state.trocas_dados = []

    df_combinado = carregar_csv_combinado()

    fornecedores_unicos = sorted(df_combinado["FORNECEDOR"].dropna().unique())
    selected_fornecedor = st.selectbox("Selecione o Fornecedor para realizar a troca:", [""] + fornecedores_unicos)

    if selected_fornecedor:
        df_fornecedor = df_combinado[df_combinado["FORNECEDOR"] == selected_fornecedor]

        st.subheader("🔍 Buscar Produto para Troca")
        col1, col2, col3 = st.columns([3, 4, 2])
        tipo_busca = col1.selectbox("Buscar por:", ["CÓDIGO DE BARRAS", "REF"])
        coluna_id = "CODIGO BARRA" if tipo_busca == "CÓDIGO DE BARRAS" else "CODIGO"
        identificadores_disponiveis = sorted(df_fornecedor[coluna_id].dropna().astype(str).str.strip().unique())
        identificador = col2.selectbox(f"Selecione o {tipo_busca}:", [""] + identificadores_disponiveis)
        quantidade = col3.number_input("Quantidade", min_value=1, step=1, value=1)

        if st.button("🔎 Buscar Produto para Troca"):
            if not identificador:
                st.warning("❌ Por favor, selecione um identificador válido.")
            else:
                resultado = buscar_produto(identificador, coluna_id, df_fornecedor)
                if resultado is not None:
                    st.session_state.trocas_dados.append({
                        "CODIGO BARRA": resultado.get("CODIGO BARRA", ""),
                        "CODIGO": resultado.get("CODIGO", ""),
                        "FORNECEDOR": resultado.get("FORNECEDOR", ""),
                        "DESCRICAO": resultado.get("DESCRICAO", ""),
                        "QUANTIDADE": quantidade
                    })
                    st.success(f"✅ Produto adicionado: {resultado.get('DESCRICAO', '')}")
                else:
                    st.warning("❌ Produto não encontrado com esse identificador.")
    else:
        st.info("Por favor, selecione um fornecedor para iniciar o processo de troca.")

    if st.session_state.trocas_dados:
        st.subheader(f"📋 Produtos para Troca ({len(st.session_state.trocas_dados)} itens)")
        df_trocas = pd.DataFrame(st.session_state.trocas_dados)
        st.dataframe(df_trocas, use_container_width=True)

        colA, colB = st.columns([1, 3])
        if colA.button("🗑️ Remover Último Item"):
            removido = st.session_state.trocas_dados.pop()
            st.warning(f"Item removido: {removido['DESCRICAO']} (Qtd: {removido['QUANTIDADE']})")

        def gerar_formulario_excel(dados):
            fornecedores = set(item['FORNECEDOR'] for item in dados)
            if len(fornecedores) > 1:
                return None, "❌ Existem múltiplos fornecedores na lista."
            try:
                wb = load_workbook("FORM-TROCAS.xlsx")
                ws = wb.active
                fornecedor = fornecedores.pop()
                ws["C3"] = fornecedor
                for i, item in enumerate(dados[:27]):
                    row = i + 6
                    ws[f"A{row}"] = item["CODIGO BARRA"]
                    ws[f"B{row}"] = item["CODIGO"]
                    ws[f"C{row}"] = item["DESCRICAO"]
                    ws[f"D{row}"] = item["QUANTIDADE"]
                output = BytesIO()
                wb.save(output)
                output.seek(0)
                return output, None
            except Exception as e:
                return None, f"Erro ao gerar formulário: {e}"

        if colB.button("📄 Gerar Formulário de Troca"):
            excel_bytes, erro = gerar_formulario_excel(st.session_state.trocas_dados)
            if erro:
                st.error(erro)
            else:
                st.success("✅ Formulário gerado com sucesso!")
                st.download_button(
                    label="📥 Baixar Formulário de Troca",
                    data=excel_bytes,
                    file_name="FORMULARIO_TROCA.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.info("Nenhum produto adicionado para troca ainda.")

# ========================= APP 2: PEDIDOS =========================
def app_pedidos():
    st.header("🛍️ Processo de Pedidos")
    st.divider()

    if "produtos_solicitados" not in st.session_state:
        st.session_state.produtos_solicitados = []

    df = carregar_csv_combinado()

    aba1, aba2, aba3 = st.tabs(["🧍 Individual", "📂 Lote", "📋 Revisão"])

    with aba1:
        fornecedores = sorted(df["FORNECEDOR"].dropna().unique())
        forn = st.selectbox("Fornecedor:", fornecedores)
        tipo = st.selectbox("Buscar por:", ["CÓDIGO DE BARRAS", "REF"])
        col_busca = "CODIGO BARRA" if tipo == "CÓDIGO DE BARRAS" else "CODIGO"
        df_filt = df[df["FORNECEDOR"] == forn]
        opcao = st.selectbox("Produto:", sorted(df_filt[col_busca].dropna().unique()))
        qtd = st.number_input("Quantidade:", min_value=1, step=1)

        if st.button("➕ Adicionar Pedido"):
            produto = df_filt[df_filt[col_busca] == opcao]
            if not produto.empty:
                p = produto.iloc[0]
                item = {
                    "FORNECEDOR": forn,
                    "CODIGO BARRA": p["CODIGO BARRA"],
                    "CODIGO": p["CODIGO"],
                    "DESCRICAO": p["DESCRICAO"],
                    "QTD": qtd,
                    "ORIGEM": p.get("__ORIGEM_PLANILHA__", "")
                }
                st.session_state.produtos_solicitados.append(item)
                st.toast("✅ Produto adicionado!")
            else:
                st.error("❌ Produto não encontrado.")

    with aba2:
        col1, col2 = st.columns(2)
        if col1.button("📥 Baixar Modelo Excel"):
            modelo = pd.DataFrame(columns=["CODIGO BARRA", "CODIGO", "QTD"])
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                modelo.to_excel(writer, index=False, sheet_name="Modelo")
            output.seek(0)
            st.download_button("⬇️ Baixar modelo", output, "modelo_pedido.xlsx")

        arquivo = col2.file_uploader("📤 Enviar Excel Preenchido", type=["xlsx"])
        tipo_col = st.selectbox("Usar como identificador:", ["CÓDIGO DE BARRAS", "REF"])
        col_id = "CODIGO BARRA" if tipo_col == "CÓDIGO DE BARRAS" else "CODIGO"

        if arquivo:
            with st.spinner("Carregando dados..."):
                wb = load_workbook(filename=BytesIO(arquivo.read()))
                ws = wb.active
                data = ws.values
                cols = next(data)
                df_lote = pd.DataFrame(data, columns=cols).fillna("")
                for _, row in df_lote.iterrows():
                    cod = str(row.get(col_id, "")).strip()
                    qtd = int(str(row.get("QTD", "0")).strip())
                    produto = df[df[col_id] == cod]
                    if not produto.empty:
                        p = produto.iloc[0]
                        item = {
                            "FORNECEDOR": p["FORNECEDOR"],
                            "CODIGO BARRA": p["CODIGO BARRA"],
                            "CODIGO": p["CODIGO"],
                            "DESCRICAO": p["DESCRICAO"],
                            "QTD": qtd,
                            "ORIGEM": p.get("__ORIGEM_PLANILHA__", "")
                        }
                        st.session_state.produtos_solicitados.append(item)
                st.toast("✅ Produtos adicionados!")

    with aba3:
        if st.session_state.produtos_solicitados:
            df_final = pd.DataFrame(st.session_state.produtos_solicitados)
            st.dataframe(df_final, use_container_width=True)

            if st.button("📤 Gerar Planilha Final"):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_final.to_excel(writer, index=False, sheet_name="Pedidos")
                output.seek(0)
                st.success("✅ Planilha pronta!")
                st.download_button("⬇️ Baixar Planilha", output, "pedidos.xlsx")
        else:
            st.info("Nenhum pedido foi adicionado.")

# ========================= APP 3: TRANSFERÊNCIAS =========================
def app_transferencias():
    st.header("📦 Transferência entre Lojas")
    st.divider()

    if "formulario_dados" not in st.session_state:
        st.session_state.formulario_dados = []

    lojas = ["MIMI", "KAMI", "TOTAL MIX", "E-COMMERCE"]
    col1, col2 = st.columns(2)
    de_loja = col1.selectbox("Loja de Origem", lojas)
    para_loja = col2.selectbox("Loja de Destino", [l for l in lojas if l != de_loja])

    df = carregar_csv_combinado()
    modo = st.radio("Modo:", ["Individual", "Lote"], horizontal=True)

    if modo == "Lote":
        st.download_button("⬇️ Baixar Modelo", data=BytesIO(), file_name="modelo_transferencia.xlsx")
        file = st.file_uploader("📤 Upload Planilha", type=["xlsx"])
        if file:
            df_lote = pd.read_excel(file)
            for _, row in df_lote.iterrows():
                cod = str(row["CODIGO BARRA"]).strip()
                qtd = int(row["QUANTIDADE"])
                produto = buscar_produto(cod, "CODIGO BARRA", df)
                if produto is not None:
                    st.session_state.formulario_dados.append({
                        "CODIGO BARRA": cod,
                        "CODIGO": produto.get("CODIGO", ""),
                        "FORNECEDOR": produto.get("FORNECEDOR", ""),
                        "DESCRICAO": produto.get("DESCRICAO", ""),
                        "QUANTIDADE": qtd
                    })

    else:
        tipo, val, qtd = st.columns([2, 3, 2])
        busca_tipo = tipo.selectbox("Buscar por:", ["Código de Barras", "REF"])
        busca_val = val.text_input("Valor:")
        busca_qtd = qtd.number_input("Quantidade", min_value=1, step=1, value=1)

        if st.button("➕ Adicionar Produto"):
            col = "CODIGO BARRA" if busca_tipo == "Código de Barras" else "CODIGO"
            produto = buscar_produto(busca_val, col, df)
            if produto is not None:
                st.session_state.formulario_dados.append({
                    "CODIGO BARRA": produto["CODIGO BARRA"],
                    "CODIGO": produto["CODIGO"],
                    "FORNECEDOR": produto["FORNECEDOR"],
                    "DESCRICAO": produto["DESCRICAO"],
                    "QUANTIDADE": busca_qtd
                })
                st.toast("✅Produto adicionado com sucesso!")

    if st.session_state.formulario_dados:
        df_form = pd.DataFrame(st.session_state.formulario_dados)
        st.dataframe(df_form, use_container_width=True)
        if st.button("📄 Gerar Relatório Transferência"):
            wb = load_workbook("FORMULÁRIO DE TRANSFERENCIA ENTRE LOJAS.xlsx")
            ws = wb.active
            ws["A4"] = f"DE: {de_loja}"
            ws["C4"] = para_loja
            ws["D4"] = "DATA " + datetime.today().strftime("%d/%m/%Y")
            for i, item in enumerate(st.session_state.formulario_dados[:30]):
                ws[f"A{8+i}"] = item["CODIGO BARRA"]
                ws[f"B{8+i}"] = item["CODIGO"]
                ws[f"C{8+i}"] = item["FORNECEDOR"]
                ws[f"D{8+i}"] = item["DESCRICAO"]
                ws[f"E{8+i}"] = item["QUANTIDADE"]
            buffer = BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            st.download_button("⬇️ Baixar Formulário Preenchido", buffer, "TRANSFERENCIA.xlsx")

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
