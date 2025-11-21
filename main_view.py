# c:/Users/aryel/OneDrive/Documents/Projetos/nutri-agro/main_view.py
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from estoque_view import EstoqueView
from vendas_view import VendasView
from cliente_view import ClienteView
from fornecedor_view import FornecedorView

class MainView(ttk.Window):
    def __init__(self, db):
        super().__init__(themename="litera")
        self.db = db
        self.title("NutriAgro - Sistema de Gestão")
        self.geometry("1024x768")
        self.place_window_center()
        self.current_view = None

        self.create_widgets()

    def create_widgets(self):
        """Cria a estrutura principal da aplicação com o menu lateral."""
        # --- Menu Superior ---
        menu_frame = ttk.Frame(self, bootstyle=SECONDARY, padding=5)
        menu_frame.pack(side=TOP, fill=X, pady=(0, 5))

        # Adiciona um título ou logo no menu
        ttk.Label(menu_frame, text="NutriAgro", font=("Helvetica", 14, "bold"), bootstyle=INVERSE + SECONDARY).pack(side=LEFT, padx=10)

        # Botões do menu baseados no checklist
        menu_buttons = ["Vendas", "Estoque", "Inventario", "Fornecedores", "NFe", "Cadastro Cliente", "Revenda", "Fluxo de Caixa"]
        for item in menu_buttons:
            command = lambda i=item: self.show_view(i)
            btn = ttk.Button(menu_frame, text=item, command=command, bootstyle=(LIGHT, "outline-toolbutton"), padding=(10, 5))
            btn.pack(side=LEFT, padx=5)

        # --- Área de Conteúdo Principal ---
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(side=BOTTOM, fill=BOTH, expand=True, padx=20, pady=10)

        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Mostra a tela de boas-vindas inicial."""
        self.clear_content_frame()
        # Título inicial
        welcome_label = ttk.Label(self.content_frame, text="Bem-vindo ao Sistema NutriAgro!", font=("Helvetica", 24, "bold"))
        welcome_label.pack(pady=(20,10))
        info_label = ttk.Label(self.content_frame, text="Selecione uma opção no menu para começar.", font=("Helvetica", 12))
        info_label.pack()
        self.current_view = [welcome_label, info_label]

    def clear_content_frame(self):
        """Limpa todos os widgets da área de conteúdo."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_view(self, view_name):
        """Carrega a view correspondente ao botão do menu clicado."""
        self.clear_content_frame()
        if view_name == "Estoque":
            self.current_view = EstoqueView(self.content_frame, self.db)
        elif view_name == "Vendas":
            self.current_view = VendasView(self.content_frame, self.db)
        elif view_name == "Cadastro Cliente":
            self.current_view = ClienteView(self.content_frame, self.db)
        elif view_name == "Fornecedores":
            self.current_view = FornecedorView(self.content_frame, self.db)
        else:
            # Placeholder para outras telas
            ttk.Label(self.content_frame, text=f"Tela de {view_name}", font=("Helvetica", 18)).pack(pady=20)
