import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_numeric_validation

class EstoqueView(ttk.Frame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.pack(fill=BOTH, expand=YES)

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        """Cria os widgets da tela de estoque: formulário e tabela."""
        # Container principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # --- Formulário de Cadastro ---
        form_frame = ttk.LabelFrame(main_frame, text="Gerenciar Produto", padding=15)
        form_frame.pack(fill=X, pady=(0, 20))

        # Linha 1: Produto, Categoria, Marca
        ttk.Label(form_frame, text="Produto:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.produto_entry = ttk.Entry(form_frame)
        self.produto_entry.grid(row=1, column=0, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Categoria:").grid(row=0, column=1, padx=5, pady=5, sticky=W)
        categorias = ["Acessorios", "Artigos de Pesca", "Medicamentos", "Nutrição"]
        self.categoria_combo = ttk.Combobox(form_frame, values=categorias)
        self.categoria_combo.grid(row=1, column=1, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Marca/Fornecedor:").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.marca_entry = ttk.Entry(form_frame)
        self.marca_entry.grid(row=1, column=2, padx=5, pady=5, sticky=EW)

        # Linha 2: Quantidades e Valores
        ttk.Label(form_frame, text="Qtd. Total:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.qtd_total_entry = ttk.Entry(form_frame)
        add_numeric_validation(self.qtd_total_entry)
        self.qtd_total_entry.grid(row=3, column=0, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Qtd. Granel (kg):").grid(row=2, column=1, padx=5, pady=5, sticky=W)
        self.qtd_granel_entry = ttk.Entry(form_frame)
        add_numeric_validation(self.qtd_granel_entry)
        self.qtd_granel_entry.grid(row=3, column=1, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Valor Granel (kg):").grid(row=2, column=2, padx=5, pady=5, sticky=W)
        self.valor_granel_entry = ttk.Entry(form_frame)
        add_numeric_validation(self.valor_granel_entry)
        self.valor_granel_entry.grid(row=3, column=2, padx=5, pady=5, sticky=EW)

        # Linha 3: Validade, Movimento
        ttk.Label(form_frame, text="Data de Validade:").grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.validade_entry = ttk.DateEntry(form_frame, bootstyle=PRIMARY, dateformat="%d/%m/%Y")
        self.validade_entry.grid(row=5, column=0, padx=5, pady=5, sticky=EW)
        
        ttk.Label(form_frame, text="Tipo Movimento:").grid(row=4, column=1, padx=5, pady=5, sticky=W)
        self.movimento_combo = ttk.Combobox(form_frame, values=["Entrada", "Saída", "Troca"])
        self.movimento_combo.grid(row=5, column=1, padx=5, pady=5, sticky=EW)
        self.movimento_combo.current(0)

        ttk.Label(form_frame, text="Valor Total (R$):").grid(row=4, column=2, padx=5, pady=5, sticky=W)
        self.valor_total_entry = ttk.Entry(form_frame, state="readonly")
        self.valor_total_entry.grid(row=5, column=2, padx=5, pady=5, sticky=EW)

        # Adiciona o "trace" para o cálculo automático
        self.qtd_total_entry.bind("<KeyRelease>", self.calculate_total_value)
        self.valor_granel_entry.bind("<KeyRelease>", self.calculate_total_value)

        form_frame.columnconfigure((0, 1, 2), weight=1)

        # --- Botões de Ação ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)

        ttk.Button(btn_frame, text="Adicionar", command=self.add_produto, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Atualizar", command=self.update_produto, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_produto, bootstyle=DANGER).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", command=self.clear_form, bootstyle=SECONDARY).pack(side=LEFT, padx=5)

        # --- Tabela de Produtos ---
        table_frame = ttk.LabelFrame(main_frame, text="Produtos em Estoque", padding=10)
        table_frame.pack(fill=BOTH, expand=YES)

        self.col_headers = [
            {"text": "ID", "stretch": False, "width": 50},
            {"text": "Produto", "stretch": True},
            {"text": "Categoria", "stretch": True},
            {"text": "Marca/Fornecedor", "stretch": True},
            {"text": "Qtd Total", "stretch": False, "width": 80},
            {"text": "Qtd Granel", "stretch": False, "width": 80},
            {"text": "Valor Granel", "stretch": False, "width": 90},
            {"text": "Valor Total", "stretch": False, "width": 90},
            {"text": "Validade", "stretch": False, "width": 100},
            {"text": "Movimento", "stretch": False, "width": 90},
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
        
        produtos = self.db.get_produtos_estoque()
        # Agora vamos usar todos os dados, exceto o último (data_movimento)
        # O formato da tupla do DB é (id, produto, categoria, ..., tipo_movimento, data_movimento)
        table_data = [row[:-1] for row in produtos]
        self.table.build_table_data(self.col_headers, table_data) # Reusa os headers definidos
        self.table.autofit_columns()

    def on_row_select(self, event=None):
        """Preenche o formulário quando uma linha da tabela é selecionada."""
        try:
            selected_row = self.table.view.item(self.table.view.selection()[0])['values']
        except IndexError:
            return # Nenhuma linha selecionada

        self.clear_form()
        
        # O ID está na primeira coluna (índice 0)
        self.selected_item_id = selected_row[0]

        self.produto_entry.insert(END, selected_row[1])
        self.categoria_combo.set(selected_row[2])
        self.marca_entry.insert(END, selected_row[3])
        self.qtd_total_entry.insert(END, selected_row[4])
        self.qtd_granel_entry.insert(END, selected_row[5])
        self.valor_granel_entry.insert(END, selected_row[6])
        
        # Preenche o valor total
        self.valor_total_entry.config(state="normal")
        self.valor_total_entry.delete(0, END)
        self.valor_total_entry.insert(0, selected_row[7])
        self.valor_total_entry.config(state="readonly")

        self.validade_entry.entry.delete(0, END)
        self.validade_entry.entry.insert(0, selected_row[8])
        self.movimento_combo.set(selected_row[9])
    
    def calculate_total_value(self, event=None):
        """Calcula o valor total com base na Qtd. Total e Valor Granel."""
        try:
            qtd = int(self.qtd_total_entry.get())
            valor_unitario = float(self.valor_granel_entry.get())
            total = qtd * valor_unitario
            
            self.valor_total_entry.config(state="normal")
            self.valor_total_entry.delete(0, END)
            self.valor_total_entry.insert(0, f"{total:.2f}")
            self.valor_total_entry.config(state="readonly")
        except (ValueError, tk.TclError):
            # Se os campos estiverem vazios ou com valor inválido, limpa o total
            self.valor_total_entry.config(state="normal")
            self.valor_total_entry.delete(0, END)
            self.valor_total_entry.config(state="readonly")

    def get_form_data(self):
        """Coleta e valida os dados do formulário."""
        produto = self.produto_entry.get()
        if not produto:
            messagebox.showwarning("Campo Obrigatório", "O nome do produto é obrigatório.")
            return None

        return (
            produto,
            self.categoria_combo.get(),
            self.marca_entry.get(),
            int(self.qtd_total_entry.get() or 0),
            float(self.qtd_granel_entry.get() or 0.0),
            float(self.valor_granel_entry.get() or 0.0),
            float(self.valor_total_entry.get() or 0.0), # Pega o valor total calculado
            self.validade_entry.entry.get(),
            self.movimento_combo.get()
        )

    def add_produto(self):
        """Adiciona um novo produto ao banco de dados."""
        data = self.get_form_data()
        if data:
            self.db.add_produto_estoque(data)
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            self.clear_form()
            self.populate_table()

    def update_produto(self):
        """Atualiza um produto selecionado."""
        if not hasattr(self, 'selected_item_id'):
            messagebox.showwarning("Aviso", "Selecione um produto na tabela para atualizar.")
            return

        data = self.get_form_data()
        if data:
            self.db.update_produto_estoque(self.selected_item_id, data)
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.clear_form()
            self.populate_table()

    def delete_produto(self):
        """Exclui um produto selecionado."""
        if not hasattr(self, 'selected_item_id'):
            messagebox.showwarning("Aviso", "Selecione um produto na tabela para excluir.")
            return

        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir o produto selecionado?"):
            self.db.delete_produto_estoque(self.selected_item_id)
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            self.clear_form()
            self.populate_table()

    def clear_form(self):
        """Limpa todos os campos do formulário."""
        self.produto_entry.delete(0, END)
        self.categoria_combo.set('')
        self.marca_entry.delete(0, END)
        self.qtd_total_entry.delete(0, END)
        self.qtd_granel_entry.delete(0, END)
        self.valor_granel_entry.delete(0, END)
        self.valor_total_entry.config(state="normal")
        self.valor_total_entry.delete(0, END)
        self.valor_total_entry.config(state="readonly")
        self.validade_entry.entry.delete(0, END)
        self.movimento_combo.set("Entrada")
        self.produto_entry.focus_set()
        if hasattr(self, 'selected_item_id'):
            del self.selected_item_id