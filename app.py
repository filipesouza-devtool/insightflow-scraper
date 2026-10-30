#app.py
import streamlit as st
import pandas as pd
st.set_page_config(page_title="InsightFlow Analytics", layout="wide")

#Gabarito
AZUL_TEXTO = "#93C5FD"
AZUL_SUBTEXTO = "#60A5FA"
AZUL_BOTAO = "#3B82F6"
AZUL_BACK = "#1E293B"

# Função de Estilização
def colorir(texto, cor_hex, tamanho="16px", negrito=False):
    peso = "bold" if negrito else "normal"
    return f"<span style='color: {cor_hex}; font-size: {tamanho}; font-weight: {peso};'>{texto}</span>"

st.write(f"""
# {colorir("InsightFlow Analytics", AZUL_TEXTO, "38px", True)}
Painel Para Analise de Dados
""", unsafe_allow_html=True)
st.write("---")

#Barra lateral
st.sidebar.markdown(f"{colorir("Painel de Controle", AZUL_TEXTO, "18px", False)}", unsafe_allow_html=True)
st.write("")
upload = st.sidebar.file_uploader("carregar arquivo csv", type=["csv"])

@st.cache_data #funcao de ler o arquivo, e armanezenar no cache
def carregar_dados(arquivo):
    try: #tenta: com utf8
        return pd.read_csv(arquivo, encoding="utf-8")
    except Exception:
        try: #tenta: padrao comum ;, latino
            arquivo.seek(0)
            return pd.read_csv(arquivo, sep=";", encoding="latin1")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return None
            
if upload:
    df = carregar_dados(upload)
    st.sidebar.success("📂 Dados carregados com sucesso!")
else:
    arqv = "dados_raspados.csv"
    df = carregar_dados(arqv)
    st.success("📂 Dados pré-carregados!")
    
if df is not None:
    st.metric(label="📊 Total de Citações Analisadas", value=len(df))
    st.write("---")
    
    #Funcao de Destaque
    def destaque_dado(contagem):
        for dado, qnt in contagem.items():
            st.markdown(f"• *{dado}* :blue-background[{qnt}]")
                
    #DESTAQUES: colunas Autor / Tag mais citados
    st.markdown(f"{colorir("Destaques", AZUL_SUBTEXTO, "32px", True)}", unsafe_allow_html=True)
    col_autor, col_tag = st.columns(2)
    with col_autor:
        with st.container(border=True):
            contagem_autor = df['Autor'].value_counts().head(3)
            st.markdown("##### ✍️ Autores:")
            st.write("---")
            destaque_dado(contagem_autor)
                
    with col_tag:
        with st.container(border=True):
            contagem_tag = df['Tags'].value_counts().head(3)
            st.write("##### 🏷️ Tags:")
            st.write("---")
            destaque_dado(contagem_tag)
    
    #Filtro
    st.write("---")
    colunas_disponiveis = list(df.columns)
    colunas_selecionadas = st.multiselect("Filtrar Dados por Coluna: ", 
    options=colunas_disponiveis, 
    default=colunas_disponiveis[:3])
    
    if colunas_selecionadas:
        df_filtrado = df[colunas_selecionadas]
        
        #Tabela de dados
        st.markdown(f"{colorir("Tabela de Dados", AZUL_TEXTO, "32px", True)}", unsafe_allow_html=True)
        st.write("")
        tabela_css = """
        <style>
            .table { width: 100%; border-collapse: collapse; font-size: 13px; font-family: sans-serif; }
            .table th { background: #1e293b; color: #ffffff; padding: 10px 12px; text-align: left; border-bottom: 2px solid #334155; font-weight: 400; white-space: nowrap; }
            .table td { padding: 10px 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); color: #f3f4f6; background: transparent; vertical-align: top; white-space: nowrap; }
            .table td:nth-child(2) { white-space: normal; word-break: break-word; min-width: 250px; }
            .table tr:hover td { background: rgba(255, 255, 255, 0.03); }
        </style>
        """
        tabela_html = df_filtrado.to_html(classes ="table table-striped", index=False)
        st.components.v1.html(tabela_css + tabela_html, height=600, scrolling=True)
        
    else:
        st.write("Selecione ao menos uma coluna")
    
else:
    st.info("💡 **Dica:** Selecione um arquivo")
    
st.write("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 12px;'>InsightFlow Analytics • Desenvolvido em Python & Streamlit</p>", unsafe_allow_html=True)
