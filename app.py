import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd

# Carregar .env localmente
load_dotenv()

# Função para obter variáveis de ambiente de forma segura
def get_env(key):
    return os.getenv(key)

# Conexão com banco de dados
def conectar_database_selecionado():
    return mysql.connector.connect(
        host=get_env("MYSQL_HOST"),
        port=int(get_env("MYSQL_PORT")),
        user=get_env("MYSQL_USER"),
        password=get_env("MYSQL_PASSWORD"),
        database=get_env("MYSQL_DB")
    )

# === Funções de consulta ===
def consultar_profissionais():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome, genero, email, senioridade FROM profissionais ORDER BY id ASC")
        profissionais = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        cursor.close()
        conn.close()
    return profissionais, colunas

def consultar_habilidades():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome FROM habilidades ORDER BY id ASC")
        habilidades = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        cursor.close()
        conn.close()
    return habilidades, colunas

def consultar_profissional_habilidades():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT profissional_id, habilidade_id, nivel FROM profissional_habilidades ORDER BY profissional_id ASC")
        profissional_habilidades = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        cursor.close()
        conn.close()
    return profissional_habilidades, colunas

def consultar_experiencias():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, profissional_id, empresa, cargo, tempo_meses FROM experiencias ORDER BY id ASC")
        experiencias = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        cursor.close()
        conn.close()
    return experiencias, colunas

def consultar_salarios():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, profissional_id, salario_mensal, data_referencia FROM salarios ORDER BY id ASC")
        salarios = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        cursor.close()
        conn.close()
    return salarios, colunas

def consultar_localizacoes():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, profissional_id, estado, cidade, remoto FROM localizacoes ORDER BY id ASC")
        localizacoes = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        cursor.close()
        conn.close()
    return localizacoes, colunas

# === Funções auxiliares ===
def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

def formatar_data(data):
    return data.strftime('%d/%m/%Y')

def formatar_localizacao_remoto(remoto):
    return "Sim" if remoto == 1 else "Não"

# === Configuração do Streamlit ===
st.set_page_config(page_title="TechProfile", layout="centered")
st.title("TechProfile - Plataforma Inteligente de Análise de dados de Profissionais de TI")
st.text("A TechProfile é uma plataforma inteligente voltada para a análise de dados de profissionais de tecnologia. Você poderá obter informações sobre profissionais, habilidades, experiências, salários e localização.")

# === Filtro ===
def filtrar_profissional():
    st.sidebar.header("🔍 Filtro de Profissionais")
    profissionais, colunas = consultar_profissionais()
    df_profissionais = pd.DataFrame(profissionais, columns=colunas)
    df_profissionais.columns = df_profissionais.columns.str.upper()

    genero_opcao = st.sidebar.multiselect(
        "Filtrar por Gênero:",
        options=df_profissionais["GENERO"].unique(),
        default=df_profissionais["GENERO"].unique()
    )

    somente_generos = st.sidebar.checkbox("Mostrar apenas os gêneros", value=False)

    senioridade_opcao = st.sidebar.multiselect(
        "Filtrar por Senioridade:",
        options=df_profissionais["SENIORIDADE"].unique(),
        default=df_profissionais["SENIORIDADE"].unique()
    )

    somente_senioridades = st.sidebar.checkbox("Mostrar apenas as senioridades", value=False)

    dados_filtrados = df_profissionais[
        (df_profissionais["GENERO"].isin(genero_opcao)) &
        (df_profissionais["SENIORIDADE"].isin(senioridade_opcao))
    ]

    if somente_senioridades:
        st.write(dados_filtrados["SENIORIDADE"])
    elif somente_generos:
        st.write(dados_filtrados["GENERO"])
    else:
        st.dataframe(dados_filtrados, use_container_width=True)

# === Execução principal ===
if __name__ == "__main__":
    st.subheader("👥 Profissionais")
    filtrar_profissional()
