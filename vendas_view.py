import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview


class VendasView(ttk.Frame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.pack(fill=BOTH, expand=YES)

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        """Cria os widgets da tela de vendas: formulário e tabela."""
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # --- Formulário de Cadastro ---
        form_frame = ttk.LabelFrame(main_frame, text="Registrar Venda", padding=15)
        form_frame.pack(fill=X, pady=(0, 20))

        # Linha 1
        ttk.Label(form_frame, text="Produto:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.produto_entry = ttk.Entry(form_frame)
        self.produto_entry.grid(row=1, column=0, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Valor Total (R$):").grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.valor_total_entry = ttk.Entry(form_frame)
        self.valor_total_entry.grid(row=1, column=1, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Valor Granel (kg):").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.valor_granel_entry = ttk.Entry(form_frame)
        self.valor_granel_entry.grid(row=1, column=2, padx=5, pady=5, sticky=EW)

        # Linha 2
        ttk.Label(form_frame, text="Tipo de Pagamento:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        pagamentos = ["Cartão de Crédito", "Cartão de Débito", "Pix", "Dinheiro"]
        self.pagamento_combo = ttk.Combobox(form_frame, values=pagamentos)
        self.pagamento_combo.grid(row=3, column=0, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Brindes:").grid(row=2, column=1, padx=5, pady=5, sticky=W)
        self.brindes_entry = ttk.Entry(form_frame)
        self.brindes_entry.grid(row=3, column=1, padx=5, pady=5, sticky=EW)

        ttk.Label(form_frame, text="Desconto (%):").grid(row=2, column=2, padx=5, pady=5, sticky=W)
        self.desconto_spinbox = ttk.Spinbox(form_frame, from_=0, to=20)
        self.desconto_spinbox.grid(row=3, column=2, padx=5, pady=5, sticky=EW)

        # Linha 3
        self.fiado_var = tk.IntVar()
        self.fiado_check = ttk.Checkbutton(form_frame, text="Venda a Fiado", variable=self.fiado_var, bootstyle="primary")
        self.fiado_check.grid(row=4, column=0, padx=5, pady=10, sticky=W)

        form_frame.columnconfigure((0, 1, 2), weight=1)

        # --- Botões de Ação ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)
        ttk.Button(btn_frame, text="Adicionar Venda", command=self.add_venda, bootstyle=SUCCESS).pack(side=LEFT, padx=5)

        # --- Tabela de Vendas ---
        table_frame = ttk.LabelFrame(main_frame, text="Vendas Recentes", padding=10)
        table_frame.pack(fill=BOTH, expand=YES)

        self.col_headers = [
            {"text": "ID", "stretch": False, "width": 50},
            {"text": "Produto", "stretch": True},
            {"text": "Valor Total", "stretch": False},
            {"text": "Pagamento", "stretch": True},
            {"text": "Fiado", "stretch": False},
            {"text": "Data", "stretch": True},
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

    def populate_table(self):
        """Busca os dados do banco e preenche a tabela de vendas."""
        for row in self.table.get_children():
            self.table.delete(row)
        
        vendas = self.db.get_vendas()
        # Formata os dados para exibição (ex: 'Sim'/'Não' para fiado)
        formatted_vendas = [(v[0], v[1], f"R$ {v[2]:.2f}", v[3], "Sim" if v[4] else "Não", v[5]) for v in vendas]
        self.table.build_table_data(self.col_headers, formatted_vendas)
        self.table.autofit_columns()

    def get_form_data(self):
        """Coleta e valida os dados do formulário de vendas."""
        produto = self.produto_entry.get()
        if not produto:
            messagebox.showwarning("Campo Obrigatório", "O nome do produto é obrigatório.")
            return None

        return (
            produto,
            float(self.valor_total_entry.get() or 0.0),
            float(self.valor_granel_entry.get() or 0.0),
            self.pagamento_combo.get(),
            self.brindes_entry.get(),
            float(self.desconto_spinbox.get() or 0.0),
            self.fiado_var.get()
        )

    def add_venda(self):
        """Adiciona uma nova venda ao banco de dados."""
        data = self.get_form_data()
        if data:
            self.db.add_venda(data)
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            self.clear_form()
            self.populate_table()

    def clear_form(self):
        """Limpa todos os campos do formulário de vendas."""
        self.produto_entry.delete(0, END)
        self.valor_total_entry.delete(0, END)
        self.valor_granel_entry.delete(0, END)
        self.pagamento_combo.set('')
        self.brindes_entry.delete(0, END)
        self.desconto_spinbox.set(0)
        self.fiado_var.set(0)
        self.produto_entry.focus_set()


def add_venda(self):
    """Adiciona uma nova venda ao banco de dados."""
    data = self.get_form_data()
    if data:
        # Nota: Precisaremos criar a função add_venda() no database.py
        # self.db.add_venda(data)
        messagebox.showinfo("Sucesso", "Venda registrada com sucesso! (Simulação)")
        self.populate_table()
        # Limpar formulário aqui
        self.produto_entry.delete(0, END)
        # ... limpar outros campos

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from estoque_view import EstoqueView
from vendas_view import VendasView

class MainView(ttk.Window):
    def __init__(self, db, view_name="Vendas"):
        self.clear_content_frame()
        if view_name == "Estoque":
            self.current_view = EstoqueView(self.content_frame, self.db)
        elif view_name == "Vendas":
            self.current_view = VendasView(self.content_frame, self.db)
        else:
            # Placeholder para outras telas
            ttk.Label(self.content_frame, text=f"Tela de {view_name}", font=("Helvetica", 18)).pack(pady=20)
