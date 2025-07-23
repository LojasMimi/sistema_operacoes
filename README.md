
# 🧠 Sistema de Operações – Lojas MIMI

**Versão:** 3.0
**Desenvolvedor:** Pablo
**Última atualização:** 2025

---

## 📦 Visão Geral

O **Sistema de Operações – Lojas MIMI** é um sistema web interno desenvolvido em **Python + Streamlit**, criado para integrar e digitalizar os principais processos logísticos e comerciais da rede Lojas MIMI. A versão 3.0 consolida as rotinas administrativas mais importantes da empresa em um único painel operacional.

### 🔧 Módulos incluídos:

* **♻️ Trocas com Fornecedores**
* **🛍️ Pedidos das Lojas**
* **📦 Transferência entre Lojas**
* **🔍 Pesquisa de Produtos**
* **🛠️ Atualizador de Preços (NOVO)**

---

## 🚀 Funcionalidades

### ♻️ Processo de Trocas

* Busca por código de barras ou REF
* Inclusão individual ou por lote via planilha Excel
* Validação automática e controle de fornecedor único
* Geração automática do formulário padrão `FORM-TROCAS.xlsx`

### 🛍️ Processo de Pedidos

* Busca por código de barras ou REF, filtrada por fornecedor
* Adição de produtos manualmente ou em lote via Excel
* Geração de planilha final pronta para importação (CADIMPORT, CADPRO, CADPLA)

### 📦 Transferência entre Lojas

* Escolha da loja de origem e destino
* Adição de produtos individualmente ou por planilha
* Geração automática do modelo `FORMULÁRIO DE TRANSFERENCIA ENTRE LOJAS.xlsx`

### 🔍 Pesquisa de Produtos

* Consulta ao **catálogo corporativo padronizado**
* Busca por código de barras, código VF ou REF
* Resultados apresentados diretamente na interface
* Fonte: planilha `cad_concatenado.csv` hospedada no GitHub

### 🛠️ Atualizador de Preços (**NOVO na versão 3.0**)

* Login via API do **Varejo Fácil**
* Consulta e atualização de **preço de venda** e **custo** por produto
* Suporte a busca por código de barras ou ID de produto
* Atualizações aplicadas diretamente nas lojas cadastradas (IDs: 1, 2, 5)

---

## ⚙️ Como Executar

### 🔧 Pré-requisitos

* Python 3.8 ou superior
* Instalar os pacotes:

  ```bash
  pip install -r requirements.txt
  ```

  Pacotes principais:

  * `streamlit`
  * `pandas`
  * `openpyxl`
  * `Pillow`
  * `requests`

### ▶️ Execução

```bash
streamlit run teste_apps_unificados.py
```

Abra o navegador em: [http://localhost:8501](http://localhost:8501)

---

## 🧾 Estrutura do Projeto

```
sistema-operacoes/
├── teste_apps_unificados.py              # Código principal da aplicação
├── requirements.txt                      # Lista de dependências
├── logo_lojas_mimi.jpeg                  # Logotipo da aplicação
├── FORM-TROCAS.xlsx                      # Template de trocas
├── FORMULÁRIO DE TRANSFERENCIA...xlsx    # Template de transferências
```

---

## 🔐 Segurança

* Todos os dados são processados **localmente**
* Nenhuma informação sensível é enviada a servidores externos, exceto quando necessário via API segura do Varejo Fácil
* Geração e download de arquivos feita diretamente no navegador

---

## 🔍 Integrações

* **Varejo Fácil API**

  * Utilizada para consulta e atualização de produtos e preços
  * Acesso autenticado via `accessToken` seguro
* **Planilha de Catálogo Centralizado**

  * [cad\_concatenado.csv (GitHub)](https://raw.githubusercontent.com/LojasMimi/transferencia_loja/refs/heads/main/cad_concatenado.csv)

---

## 📌 Observações Técnicas

* Utiliza `st.session_state` para manter o estado entre interações
* Geração dinâmica de arquivos Excel com `openpyxl`
* Interface otimizada com HTML/CSS para melhor usabilidade
* Compatível com múltiplos tipos de identificadores de produto

---

## 🛠️ Desenvolvimento

Este sistema foi desenvolvido por **Pablo** para uso interno das **Lojas MIMI**, com o objetivo de **automatizar processos operacionais**, **reduzir erros manuais** e **melhorar a integração entre lojas e colaboradores**.

---

## 📝 Licença

**Privado** — Sistema de uso exclusivo das Lojas MIMI.
© 2025 Lojas MIMI – Todos os direitos reservados.


