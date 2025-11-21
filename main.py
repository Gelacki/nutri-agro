# c:/Users/aryel/OneDrive/Documents/Projetos/nutri-agro/main.py
from database import Database
from login_view import LoginView
from main_view import MainView

class Application:
    def __init__(self):
        self.db = Database()
        # O usuário padrão é 'admin' com senha 'admin'
        self.show_login_screen()

    def show_login_screen(self):
        """Exibe a tela de login."""
        login_app = LoginView(db=self.db, on_login_success=self.show_main_screen)
        login_app.mainloop()

    def show_main_screen(self):
        """Exibe a tela principal após o login bem-sucedido."""
        main_app = MainView(db=self.db)
        main_app.mainloop()

    def run(self):
        """Inicia o ciclo da aplicação."""
        # O fluxo é controlado pelas janelas, então este método pode ser simples.
        # A aplicação termina quando a janela principal for fechada.
        self.db.close()

if __name__ == "__main__":
    app = Application()
    # O fluxo de janelas já é iniciado no __init__
