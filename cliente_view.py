import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage, filedialog 
from ttkbootstrap.tableview import Tableview
import re
from pycpfcnpj import cpfcnpj

class ClienteView(ttk.Frame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.pack(fill=BOTH, expand=YES)

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        """Cria os widgets da tela de clientes: formulário e tabela."""
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # --- Formulário de Cadastro ---
        form_frame = ttk.LabelFrame(main_frame, text="Gerenciar Cliente", padding=15)
        form_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(form_frame, text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.nome_entry = ttk.Entry(form_frame)
        self.nome_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="CPF/CNPJ:").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.cpf_cnpj_entry = ttk.Entry(form_frame)
        self.cpf_cnpj_entry.grid(row=1, column=2, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Data de Nascimento:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.data_nascimento_entry = ttk.DateEntry(form_frame, bootstyle=PRIMARY, dateformat="%d/%m/%Y")
        self.data_nascimento_entry.grid(row=3, column=0, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Telefone:").grid(row=2, column=1, padx=5, pady=5, sticky=W)
        self.telefone_entry = ttk.Entry(form_frame)
        self.telefone_entry.grid(row=3, column=1, padx=5, pady=5, sticky=EW)

        # Frame para a foto
        self.foto_frame = ttk.Frame(form_frame, width=100, height=100, relief=SOLID, borderwidth=1)
        self.foto_frame.grid(row=2, column=2, rowspan=2, padx=5, pady=5, sticky=NSEW)
        self.foto_label = ttk.Label(self.foto_frame, text="Sem Foto", anchor="center")
        self.foto_label.pack(fill=BOTH, expand=YES)
        self.foto_path = None  # Guarda o caminho da foto

        # Botão para carregar a foto
        ttk.Button(form_frame, text="Carregar Foto", command=self.carregar_foto, width=15).grid(row=4, column=2, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Observações:").grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.observacoes_entry = tk.Text(form_frame, height=4)
        self.observacoes_entry.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Endereço:").grid(row=6, column=0, padx=5, pady=5, sticky=W)
        self.endereco_entry = ttk.Entry(form_frame)
        self.endereco_entry.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky=EW)

        form_frame.columnconfigure((0, 1, 2), weight=1)

        # --- Botões de Ação ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)
        
        ttk.Button(btn_frame, text="Adicionar", command=self.add_cliente, bootstyle=SUCCESS).pack(side=LEFT, padx=5)

        ttk.Button(btn_frame, text="Atualizar", command=self.update_cliente, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_cliente, bootstyle=DANGER).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", command=self.clear_form, bootstyle=SECONDARY).pack(side=LEFT, padx=5)

        # --- Tabela de Clientes ---
        table_frame = ttk.LabelFrame(main_frame, text="Clientes Cadastrados", padding=10)
        table_frame.pack(fill=BOTH, expand=YES)

        self.col_headers = [

            {"text": "ID", "stretch": False, "width": 40},
            {"text": "Nome", "stretch": True},
            {"text": "CPF/CNPJ", "stretch": True},
            {"text": "Data Nasc.", "stretch": True},
            {"text": "Telefone", "stretch": True},
            {"text": "Endereço", "stretch": True},

        ]

        self.table = Tableview(
            master=table_frame,
            coldata=self.col_headers,
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(None, "#f0f0f0")
        )
        self.table.pack(fill=BOTH, expand=YES)
        self.table.view.bind("<<TreeviewSelect>>", self.on_row_select)

    def populate_table(self):
        """Busca os dados do banco e preenche a tabela."""
        for row in self.table.get_children():
            self.table.delete(row)
        
        clientes = self.db.get_clientes()
        self.table.build_table_data(self.col_headers, clientes)

        self.table.autofit_columns()


    def carregar_foto(self):
        """Abre a caixa de diálogo para selecionar a foto."""
        self.foto_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if self.foto_path:
            foto = PhotoImage(file=self.foto_path)
            self.foto_label.config(image=foto)
            self.foto_label.image = foto  # Guarda a referência para evitar que o garbage collector a elimine
    def on_row_select(self, event=None):
        try:
            selected_row = self.table.view.item(self.table.view.selection()[0])['values']
        except IndexError:
            return

        self.clear_form()
        self.selected_item_id = selected_row[0]
        self.nome_entry.insert(END, selected_row[1])
        self.cpf_cnpj_entry.insert(END, selected_row)
        self.data_nascimento_entry.entry.delete(0, END)
        self.data_nascimento_entry.entry.insert(0, selected_row)
        self.telefone_entry.insert(END, selected_row)
        self.endereco_entry.insert(END, selected_row)
        self.observacoes_entry.insert(END, selected_row)

    def get_form_data(self):
        """Coleta e valida os dados do formulário."""
        nome = self.nome_entry.get()
        if not nome:

            messagebox.showwarning("Campo Obrigatório", "O nome do cliente é obrigatório.")
            return None
        
        # Ler a foto como binário
        foto_binario = None
        if self.foto_path:
            with open(self.foto_path, "rb") as file:
                foto_binario = file.read()

        return (
            nome,
            self.cpf_cnpj_entry.get(),
            self.data_nascimento_entry.entry.get(), 
            self.telefone_entry.get(),
            foto_binario,
            self.observacoes_entry.get("1.0", END),
            self.endereco_entry.get()
        )

    def add_cliente(self):
        """Adiciona um novo cliente ao banco de dados."""

        data = self.get_form_data()
        if data:
            self.db.add_cliente(data)
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
            self.clear_form()
            self.populate_table()

    def update_cliente(self):
        """Atualiza um cliente selecionado."""

        if not hasattr(self, 'selected_item_id'):
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para atualizar.")
            return
        data = self.get_form_data()
        if data:
            self.db.update_cliente(self.selected_item_id, data)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            self.clear_form()
            self.populate_table()

    def delete_cliente(self):
        """Exclui um cliente selecionado."""

        if not hasattr(self, 'selected_item_id'):
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para excluir.")
            return
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir o cliente selecionado?"):
            self.db.delete_cliente(self.selected_item_id)
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            self.clear_form()
            self.populate_table()

    def clear_form(self):
        """Limpa todos os campos do formulário."""

        self.nome_entry.delete(0, END)
        self.cpf_cnpj_entry.delete(0, END)
        self.data_nascimento_entry.entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
        self.observacoes_entry.delete("1.0", END)
        self.foto_label.config(image='', text="Sem Foto")
        self.foto_label.image = None
        self.foto_path = None
        self.nome_entry.focus_set()
        if hasattr(self, 'selected_item_id'):
            del self.selected_item_id