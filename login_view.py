# c:/Users/aryel/OneDrive/Documents/Projetos/nutri-agro/login_view.py
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class LoginView(ttk.Window):
    def __init__(self, db, on_login_success):
        super().__init__(themename="litera")
        self.db = db
        self.on_login_success = on_login_success

        self.title("Login - NutriAgro")
        self.geometry("400x300")
        self.resizable(False, False)
        self.place_window_center()

        self.create_widgets()

    def create_widgets(self):
        """Cria e posiciona os widgets na tela de login."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=BOTH)

        ttk.Label(main_frame, text="Acesso ao Sistema", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

        # Campo Usuário
        ttk.Label(main_frame, text="Usuário:").pack(fill=X, pady=(0, 5))
        self.user_entry = ttk.Entry(main_frame)
        self.user_entry.pack(fill=X, pady=(0, 10))
        self.user_entry.focus_set()

        # Campo Senha
        ttk.Label(main_frame, text="Senha:").pack(fill=X, pady=(0, 5))
        self.pass_entry = ttk.Entry(main_frame, show="*")
        self.pass_entry.pack(fill=X, pady=(0, 20))
        
        # Botão de Login
        login_button = ttk.Button(main_frame, text="Entrar", command=self.handle_login, bootstyle=SUCCESS)
        login_button.pack(fill=X, ipady=5)
        
        # Permite usar a tecla Enter para logar
        self.bind('<Return>', self.handle_login)

    def handle_login(self, event=None):
        """Valida as credenciais do usuário."""
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if not username or not password:
            messagebox.showerror("Erro de Login", "Usuário e senha são obrigatórios.")
            return

        if self.db.check_user(username, password):
            self.destroy()  # Fecha a janela de login
            self.on_login_success()  # Chama a função para abrir a tela principal
        else:
            messagebox.showerror("Erro de Login", "Credenciais inválidas.")

