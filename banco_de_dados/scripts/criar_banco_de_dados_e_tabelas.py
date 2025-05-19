import mysql.connector
from dotenv import load_dotenv
import os
from faker import Faker
import random
import csv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função auxiliar para obter variáveis de ambiente
def get_env(key):
    return os.getenv(key)

# Conexão genérica (sem banco selecionado)
def conectar_database():
    return mysql.connector.connect(
        host=get_env("MYSQL_HOST"),
        port=int(get_env("MYSQL_PORT")),
        user=get_env("MYSQL_USER"),
        password=get_env("MYSQL_PASSWORD"),
    )

# Conexão com banco de dados selecionado
def conectar_database_selecionado():
    return mysql.connector.connect(
        host=get_env("MYSQL_HOST"),
        port=int(get_env("MYSQL_PORT")),
        user=get_env("MYSQL_USER"),
        password=get_env("MYSQL_PASSWORD"),
        database=get_env("MYSQL_DB")
    )

# Cria o banco se ele não existir
def criar_database():
    database = get_env("MYSQL_DB")
    conn = conectar_database()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conn.commit()
    cursor.close()
    conn.close()

# Cria as tabelas e relações
def criar_tabela():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissionais (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            genero ENUM('M', 'F', 'O', 'N'),
            email VARCHAR(150) UNIQUE,
            senioridade VARCHAR(20)
        ) ENGINE=InnoDB;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habilidades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) UNIQUE
        ) ENGINE=InnoDB;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissional_habilidades (
            profissional_id INT,
            habilidade_id INT,
            nivel VARCHAR(20),
            PRIMARY KEY (profissional_id, habilidade_id),
            FOREIGN KEY (profissional_id) REFERENCES profissionais(id),
            FOREIGN KEY (habilidade_id) REFERENCES habilidades(id)
        ) ENGINE=InnoDB;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiencias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            profissional_id INT,
            empresa VARCHAR(100),
            cargo VARCHAR(100),
            tempo_meses INT,
            FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
        ) ENGINE=InnoDB;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            profissional_id INT,
            salario_mensal DECIMAL(10,2),
            data_referencia DATE,
            FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
        ) ENGINE=InnoDB;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS localizacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            profissional_id INT,
            estado VARCHAR(2),
            cidade VARCHAR(100),
            remoto TINYINT(1),
            FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
        ) ENGINE=InnoDB;
    """)

    conn.commit()
    cursor.close()
    conn.close()

fake = Faker('pt_BR')

def gerar_dados_profissionais():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    nomes_usados = set()
    emails_usados = set()
    total_para_gerar = 50
    criados = 0
    try:
        while criados < total_para_gerar:
            genero = random.choice(['M', 'F', 'O', 'N']) # 'Masculino', 'Feminino', 'Outro', 'Prefere não informar'
            if genero == 'M':
                nome = fake.name_male()
            elif genero == 'F':
                nome = fake.name_female()
            else:
                nome = fake.name()
            if nome in nomes_usados:
                continue
            nomes_usados.add(nome)
            email = fake.email()
            if email in emails_usados:
                continue
            emails_usados.add(email)
            cursor.execute("SELECT COUNT(*) FROM profissionais WHERE nome = %s OR email = %s", (nome, email))
            if cursor.fetchone()[0] == 0:
                senioridade = random.choice(["Júnior", "Pleno", "Sênior"])
                cursor.execute("""
                    INSERT INTO profissionais (nome, genero, email, senioridade)
                    VALUES (%s, %s, %s, %s)
                """, (nome, genero, email, senioridade))
                criados += 1
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def gerar_dados_habilidades():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()

    habilidades = [
        'HTML', 'CSS', 'JavaScript', 'TailwindCSS', 'React', 'Node.js',
        'Next.js', 'Nest.js', 'Angular', 'Bootstrap', 'Vue.js', 'Python',
        'C', 'Java', 'C++', 'C#', 'Rust', 'Ruby', 'Flutter', 'React Native',
        'MongoDB', 'MySQL', 'PostgreSQL', 'Oracle', 'SQL Server', 'SQLite',
        'Prisma', 'Docker', 'GIT'
    ]

    try:
        for habilidade in habilidades:
            cursor.execute("SELECT COUNT(*) FROM habilidades WHERE nome = %s", (habilidade,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO habilidades (nome) VALUES (%s)", (habilidade,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()  

def gerar_dados_profissional_habilidades():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    niveis = ['Iniciante', 'Intermediário', 'Avançado']
    
    try:
        cursor.execute("SELECT id FROM profissionais")
        profissionais = cursor.fetchall()

        cursor.execute("SELECT id FROM habilidades")
        habilidades = [h[0] for h in cursor.fetchall()]

        dados_para_inserir = []

        for (profissional_id,) in profissionais:
            qtd_habilidades = random.randint(1, 6)

            habilidades_escolhidas = random.sample(habilidades, qtd_habilidades)

            for habilidade_id in habilidades_escolhidas:
                nivel = random.choice(niveis)
                dados_para_inserir.append((profissional_id, habilidade_id, nivel))

        cursor.executemany("""
            INSERT IGNORE INTO profissional_habilidades (profissional_id, habilidade_id, nivel)
            VALUES (%s, %s, %s)
        """, dados_para_inserir)

        conn.commit()

    finally:
        cursor.close()
        conn.close()

def gerar_dados_experiencias():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    empresas = [
        'TechSphere Solutions', 'CodeNest Technologies', 'InfoByte Systems', 'NexCloud Innovations',
        'BitCraft Software', 'PixelForge Labs', 'QuantumCore IT', 'SkyCode Digital', 'DevPulse Studio',
        'SynapseSoft', 'BrightStack Solutions', 'CyberNova Tech', 'Zenware Technologies', 'RocketDev Systems',
        'NeoLogic Group', 'CoreVision IT', 'BluePixel Tech', 'FusionBit Systems', 'NextEra Digital', 'AlgoHive Technologies'
    ]
    cargos = [
        'Frontend', 'Backend', 'Fullstack',
        'DevOps', 'Design UI/UX', 'Infraestrutura',
        'Data Science', 'Machine Learning', 'Big Data',
        'Cloud Computing', 'Analista de Dados', 'Engenheiro de Dados'
    ]
    try:
        cursor.execute("SELECT id FROM profissionais")
        profissionais = cursor.fetchall()

        dados_para_inserir = []

        for (profissional_id,) in profissionais:
            empresa = random.choice(empresas)
            cargo = random.choice(cargos)
            tempo_meses = random.randint(6, 240)
            dados_para_inserir.append((profissional_id, empresa, cargo, tempo_meses))

        cursor.executemany("""
            INSERT INTO experiencias (profissional_id, empresa, cargo, tempo_meses)
            VALUES (%s, %s, %s, %s)
        """, dados_para_inserir)

        conn.commit()
    finally:
        cursor.close()
        conn.close()

def gerar_dados_salarios():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM profissionais")
        profissionais = cursor.fetchall()

        dados_para_inserir = []

        for (profissional_id,) in profissionais:
            salario_mensal = round(random.uniform(2500.00, 50000.00), 2)
            data_referencia = fake.date_between(start_date='-25y', end_date='today')
            dados_para_inserir.append((profissional_id, salario_mensal, data_referencia))

        cursor.executemany("""
            INSERT INTO salarios (profissional_id, salario_mensal, data_referencia)
            VALUES (%s, %s, %s)
        """, dados_para_inserir)

        conn.commit()
    finally:
        cursor.close()
        conn.close()

def gerar_dados_localizacoes():
    conn = conectar_database_selecionado()
    cursor = conn.cursor()
    estados_uf_e_cidades = {
        'SP': 'São Paulo',
        'MG': 'Belo Horizonte',
        'RJ': 'Rio de Janeiro',
        'RS': 'Rio Grande do Sul',
        'PR': 'Paraná',
        'SC': 'Santa Catarina',
        'BA': 'Salvador'
    }
    try:
        cursor.execute("SELECT id FROM profissionais")
        profissionais = cursor.fetchall()

        dados_para_inserir = []

        for (profissional_id,) in profissionais:
            uf, cidade = random.choice(list(estados_uf_e_cidades.items()))
            remoto = random.choice([True, False])
            dados_para_inserir.append((profissional_id, uf, cidade, remoto))
        
        cursor.executemany("""
            INSERT INTO localizacoes (profissional_id, estado, cidade, remoto)
            VALUES (%s, %s, %s, %s)
        """, dados_para_inserir)

        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Função para exportar os dados para CSV
def exportar_para_csv(query, filename, headers):
    conn = conectar_database_selecionado()
    cursor = conn.cursor()

    cursor.execute(query)
    data = cursor.fetchall()

    if data:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Exportado para {filename}")
    else:
        print(f"Sem dados para exportar na consulta: {query}")

# Criar a pasta datasets se não existir
os.makedirs('banco_de_dados/datasets', exist_ok=True)

if __name__ == "__main__":
    criar_database()
    criar_tabela()
    gerar_dados_profissionais()
    gerar_dados_habilidades()
    gerar_dados_profissional_habilidades()
    gerar_dados_experiencias()
    gerar_dados_salarios()
    gerar_dados_localizacoes()
    # Exportar os dados das tabelas para CSV
    exportar_para_csv('SELECT * FROM profissionais', 'banco_de_dados/datasets/profissionais.csv', ['id', 'nome', 'genero', 'email', 'senioridade'])
    exportar_para_csv('SELECT * FROM habilidades', 'banco_de_dados/datasets/habilidades.csv', ['id', 'nome'])
    exportar_para_csv('SELECT * FROM profissional_habilidades', 'banco_de_dados/datasets/profissional_habilidades.csv', ['profissional_id', 'habilidade_id', 'nivel'])
    exportar_para_csv('SELECT * FROM experiencias', 'banco_de_dados/datasets/experiencias.csv', ['id', 'profissional_id', 'empresa', 'cargo', 'tempo_meses'])
    exportar_para_csv('SELECT * FROM salarios', 'banco_de_dados/datasets/salarios.csv', ['id', 'profissional_id', 'salario_mensal', 'data_referencia'])
    exportar_para_csv('SELECT * FROM localizacoes', 'banco_de_dados/datasets/localizacoes.csv', ['id', 'profissional_id', 'estado', 'cidade', 'remoto'])