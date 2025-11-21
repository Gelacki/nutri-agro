# c:/Users/aryel/OneDrive/Documents/Projetos/nutri-agro/database.py
import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="nutri_agro.db"):
        """Inicializa a conexão com o banco de dados e cria as tabelas se não existirem."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Cria as tabelas no banco de dados com base no checklist."""
        # Tabela de usuários para o login
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """)

        # Tabela de Vendas
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            valor_total REAL NOT NULL,
            valor_granel_kg REAL,
            tipo_pagamento TEXT,
            brindes TEXT,
            desconto REAL,
            fiado INTEGER DEFAULT 0,
            data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Tabela de Estoque
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            categoria TEXT,
            marca_fornecedor TEXT,
            qtd_total INTEGER NOT NULL,
            qtd_granel_kg REAL,
            valor_granel_kg REAL,
            valor_total REAL,
            data_validade DATE,
            tipo_movimento TEXT,
            data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Tabela de Clientes
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_cnpj TEXT,
            data_nascimento TEXT,
            telefone TEXT,
            foto BLOB,
            observacoes TEXT,
            endereco TEXT
        )
        """)

        # Tabela de Fornecedores
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_empresa TEXT NOT NULL,
            contato TEXT,
            telefone TEXT,
            email TEXT,
            endereco TEXT
        )
        """)
        
        # Adiciona um usuário padrão se não houver nenhum
        self.cursor.execute("SELECT COUNT(*) FROM usuarios")
        if self.cursor.fetchone()[0] == 0:
            self.add_user("admin", "admin")

        self.conn.commit()

    def add_user(self, username, password):
        """Adiciona um novo usuário com senha criptografada."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (username, password_hash))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Usuário já existe

    def check_user(self, username, password):
        """Verifica as credenciais do usuário."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password_hash = ?", (username, password_hash))
        return self.cursor.fetchone() is not None

    # --- Métodos para o Estoque ---

    def add_produto_estoque(self, produto_data):
        """Adiciona um novo produto ao estoque."""
        sql = """
        INSERT INTO estoque (produto, categoria, marca_fornecedor, qtd_total, qtd_granel_kg, valor_granel_kg, valor_total, data_validade, tipo_movimento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, produto_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_produtos_estoque(self):
        """Retorna todos os produtos do estoque."""
        self.cursor.execute("SELECT * FROM estoque ORDER BY produto")
        return self.cursor.fetchall()

    def update_produto_estoque(self, produto_id, produto_data):
        """Atualiza um produto existente no estoque."""
        sql = """
        UPDATE estoque SET produto=?, categoria=?, marca_fornecedor=?, qtd_total=?, qtd_granel_kg=?, valor_granel_kg=?, valor_total=?, data_validade=?, tipo_movimento=?
        WHERE id=?
        """
        self.cursor.execute(sql, (*produto_data, produto_id))
        self.conn.commit()

    def delete_produto_estoque(self, produto_id):
        """Deleta um produto do estoque pelo ID."""
        self.cursor.execute("DELETE FROM estoque WHERE id=?", (produto_id,))
        self.conn.commit()

    # --- Métodos para Vendas ---

    def add_venda(self, venda_data):
        """Adiciona uma nova venda."""
        sql = """
        INSERT INTO vendas (produto, valor_total, valor_granel_kg, tipo_pagamento, brindes, desconto, fiado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, venda_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_vendas(self):
        """Retorna todas as vendas, da mais recente para a mais antiga."""
        # Seleciona as colunas na ordem que a tabela da VendasView espera
        self.cursor.execute("SELECT id, produto, valor_total, tipo_pagamento, fiado, data_venda FROM vendas ORDER BY data_venda DESC")
        return self.cursor.fetchall()

    # --- Métodos para Clientes ---

    def add_cliente(self, cliente_data):
        """Adiciona um novo cliente."""
        sql = "INSERT INTO clientes (nome, cpf_cnpj, data_nascimento, telefone, foto, observacoes, endereco) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(sql, cliente_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_clientes(self):
        """Retorna todos os clientes, ordenados por nome."""
        self.cursor.execute("SELECT * FROM clientes ORDER BY nome")
        return self.cursor.fetchall()

    def update_cliente(self, cliente_id, cliente_data):
        """Atualiza um cliente existente."""
        sql = "UPDATE clientes SET nome=?, telefone=?, endereco=? WHERE id=?"
        self.cursor.execute(sql, (*cliente_data, cliente_id))
        self.conn.commit()

    def delete_cliente(self, cliente_id):
        """Deleta um cliente pelo ID."""
        self.cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        self.conn.commit()

    # --- Métodos para Fornecedores ---

    def add_fornecedor(self, fornecedor_data):
        """Adiciona um novo fornecedor."""
        sql = "INSERT INTO fornecedores (nome_empresa, contato, telefone, email, endereco) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql, fornecedor_data)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_fornecedores(self):
        """Retorna todos os fornecedores ordenados por nome da empresa."""
        self.cursor.execute("SELECT * FROM fornecedores ORDER BY nome_empresa")
        return self.cursor.fetchall()

    def update_fornecedor(self, fornecedor_id, fornecedor_data):
        """Atualiza um fornecedor existente."""
        sql = "UPDATE fornecedores SET nome_empresa=?, contato=?, telefone=?, email=?, endereco=? WHERE id=?"
        self.cursor.execute(sql, (*fornecedor_data, fornecedor_id))
        self.conn.commit()

    def delete_fornecedor(self, fornecedor_id):
        """Deleta um fornecedor pelo ID."""
        self.cursor.execute("DELETE FROM fornecedores WHERE id=?", (fornecedor_id,))
        self.conn.commit()
    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
