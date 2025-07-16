# 🧠 Sistema de Operações – Lojas MIMI

**Versão:** 1.0
**Desenvolvedor:** Pablo
**Última atualização:** 2025

## 📦 Visão Geral

O **Sistema de Operações – Lojas MIMI** é um aplicativo web desenvolvido com Python e Streamlit para unificar e digitalizar três processos logísticos internos das unidades da rede:

* Processo de **Trocas** com fornecedores
* Solicitação de **Pedidos** pelas unidades
* **Transferência de produtos** entre lojas

A aplicação centraliza essas funcionalidades em uma interface intuitiva, segura e com geração automática de planilhas integráveis ao sistema interno da empresa.

---

## 🚀 Funcionalidades

### ♻️ Processo de Trocas

* Busca de produtos por código de barras ou referência (REF)
* Adição de produtos com controle de fornecedor único
* Geração automática de formulário de troca em Excel
* Preenchimento direto em template padrão: `FORM-TROCAS.xlsx`

### 🛍️ Processo de Pedidos

* Filtragem por fornecedor e busca de produtos por código/REF
* Adição individual ou em lote via upload de Excel
* Geração de planilha final com pedidos solicitados
* Pronto para integração com sistema (CADIMPORT, CADPRO, CADPLA)

### 📦 Transferência entre Lojas

* Seleção de loja de origem e destino
* Cadastro de transferências individual ou em lote via Excel
* Geração de relatórios em template padrão: `FORMULÁRIO DE TRANSFERENCIA ENTRE LOJAS.xlsx`

---

## ⚙️ Como Executar

### Pré-requisitos

* Python 3.8 ou superior
* Pacotes:

  * `streamlit`
  * `pandas`
  * `openpyxl`
  * `Pillow`

### Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/LojasMimi/sistema-operacoes.git
cd sistema-operacoes
pip install -r requirements.txt
```

### Execução

```bash
streamlit teste_apps_unificados.py
```

Abra [http://localhost:8501](http://localhost:8501) no navegador.

---

## 🧾 Estrutura do Projeto

```
sistema-operacoes/
├── teste_apps_unificados.py              # Código principal da aplicação
├── requirements.txt                      # Lista de dependências
├── logo_lojas_mimi.jpeg                  # Logotipo da aplicação
├── FORM-TROCAS.xlsx                      # Template de formulário de trocas
├── FORMULÁRIO DE TRANSFERENCIA...xlsx    # Template de transferências
```

---

## 🔒 Segurança

* Nenhum dado é enviado para servidores externos
* Toda a operação é local e executada na memória do sistema
* Os arquivos gerados são baixados diretamente pelo navegador

---

## 🧠 Observações Técnicas

* O sistema usa `st.session_state` para manter o estado da aplicação
* Suporta adição incremental de produtos sem duplicações
* Utiliza planilha de catálogo padronizada hospedada em:
  [cad\_concatenado.csv (GitHub)](https://raw.githubusercontent.com/LojasMimi/transferencia_loja/refs/heads/main/cad_concatenado.csv)

---

## 🛠️ Desenvolvimento

Este sistema foi desenvolvido por **Pablo** para uso interno das **Lojas MIMI**, com o objetivo de melhorar a rastreabilidade, eficiência e segurança dos processos operacionais.

---

## 📝 Licença

**Privado** — Este sistema é de uso exclusivo das Lojas MIMI.
© 2025 Lojas MIMI – Todos os direitos reservados.

---

