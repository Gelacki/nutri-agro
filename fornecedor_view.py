import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

class FornecedorView(ttk.Frame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.pack(fill=BOTH, expand=YES)

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        """Cria os widgets da tela de fornecedores: formulário e tabela."""
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # --- Formulário de Cadastro ---
        form_frame = ttk.LabelFrame(main_frame, text="Gerenciar Fornecedor", padding=15)
        form_frame.pack(fill=X, pady=(0, 20))

        # Linha 1
        ttk.Label(form_frame, text="Nome da Empresa:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.nome_empresa_entry = ttk.Entry(form_frame)
        self.nome_empresa_entry.grid(row=1, column=0, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Pessoa de Contato:").grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.contato_entry = ttk.Entry(form_frame)
        self.contato_entry.grid(row=1, column=1, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Telefone:").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.telefone_entry = ttk.Entry(form_frame)
        self.telefone_entry.grid(row=1, column=2, padx=5, pady=5, sticky=EW)

        # Linha 2
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Endereço:").grid(row=2, column=2, padx=5, pady=5, sticky=W)
        self.endereco_entry = ttk.Entry(form_frame)
        self.endereco_entry.grid(row=3, column=2, padx=5, pady=5, sticky=EW)

        form_frame.columnconfigure((0, 1, 2), weight=1)

        # --- Botões de Ação ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)

        ttk.Button(btn_frame, text="Adicionar", command=self.add_fornecedor, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Atualizar", command=self.update_fornecedor, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_fornecedor, bootstyle=DANGER).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", command=self.clear_form, bootstyle=SECONDARY).pack(side=LEFT, padx=5)

        # --- Tabela de Fornecedores ---
        table_frame = ttk.LabelFrame(main_frame, text="Fornecedores Cadastrados", padding=10)
        table_frame.pack(fill=BOTH, expand=YES)

        self.col_headers = [
            {"text": "ID", "stretch": False, "width": 50},
            {"text": "Nome da Empresa", "stretch": True},
            {"text": "Contato", "stretch": True},
            {"text": "Telefone", "stretch": True},
            {"text": "Email", "stretch": True},
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
        
        fornecedores = self.db.get_fornecedores()
        self.table.build_table_data(self.col_headers, fornecedores)
        self.table.autofit_columns()

    def on_row_select(self, event=None):
        """Preenche o formulário quando uma linha da tabela é selecionada."""
        try:
            selected_row = self.table.view.item(self.table.view.selection()[0])['values']
        except IndexError:
            return

        self.clear_form()
        self.selected_item_id = selected_row[0]
        self.nome_empresa_entry.insert(END, selected_row[1])
        self.contato_entry.insert(END, selected_row[2])
        self.telefone_entry.insert(END, selected_row[3])
        self.email_entry.insert(END, selected_row[4])
        self.endereco_entry.insert(END, selected_row[5])

    def get_form_data(self):
        """Coleta e valida os dados do formulário."""
        nome_empresa = self.nome_empresa_entry.get()
        if not nome_empresa:
            messagebox.showwarning("Campo Obrigatório", "O nome da empresa é obrigatório.")
            return None
        return (
            nome_empresa,
            self.contato_entry.get(),
            self.telefone_entry.get(),
            self.email_entry.get(),
            self.endereco_entry.get()
        )

    def add_fornecedor(self):
        """Adiciona um novo fornecedor ao banco de dados."""
        data = self.get_form_data()
        if data:
            self.db.add_fornecedor(data)
            messagebox.showinfo("Sucesso", "Fornecedor adicionado com sucesso!")
            self.clear_form()
            self.populate_table()

    def update_fornecedor(self):
        """Atualiza um fornecedor selecionado."""
        if not hasattr(self, 'selected_item_id'):
            messagebox.showwarning("Aviso", "Selecione um fornecedor na tabela para atualizar.")
            return
        data = self.get_form_data()
        if data:
            self.db.update_fornecedor(self.selected_item_id, data)
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
            self.clear_form()
            self.populate_table()

    def delete_fornecedor(self):
        """Exclui um fornecedor selecionado."""
        if not hasattr(self, 'selected_item_id'):
            messagebox.showwarning("Aviso", "Selecione um fornecedor na tabela para excluir.")
            return
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir o fornecedor selecionado?"):
            self.db.delete_fornecedor(self.selected_item_id)
            messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
            self.clear_form()
            self.populate_table()

    def clear_form(self):
        """Limpa todos os campos do formulário."""
        self.nome_empresa_entry.delete(0, END)
        self.contato_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
        self.nome_empresa_entry.focus_set()
        if hasattr(self, 'selected_item_id'):
            del self.selected_item_id