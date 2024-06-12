import tkinter as tk
from tkinter import messagebox
import json
import previsao

class LoginCadastro:
  def __init__(self, root):
    self.root = root
    self.root.title("Janela Inicial")

    self.frame_login = tk.Frame(root)
    self.frame_login.pack(pady=20)

    self.frame_cadastro = tk.Frame(root)

    # Variáveis de controle para os campos de entrada
    self.username = tk.StringVar()
    self.password = tk.StringVar()

    # Carregar usuários do arquivo
    self.usuarios = self.carregar_usuarios()

    self.button_login = tk.Button(self.frame_login, text="Login", command=self.janela_login)
    self.button_login.grid(row=2, columnspan=2, pady=10)

    self.button_cadastro = tk.Button(self.frame_login, text="Criar conta", command=self.janela_cadastro)
    self.button_cadastro.grid(row=3, columnspan=2)

    self.frame_login.tkraise()

  def janela_login(self):
    login = tk.Toplevel()
    login.title("Login")

    # Limpar campos de entrada ao mostrar a janela de cadastro
    self.username.set("")
    self.password.set("")

    # Interface de Login
    label_username = tk.Label(login, text="Usuário:")
    label_username.grid(row=0, column=0, sticky="e")

    entry_username = tk.Entry(login, textvariable=self.username)
    entry_username.grid(row=0, column=1)

    label_password = tk.Label(login, text="Senha:")
    label_password.grid(row=1, column=0, sticky="e")

    entry_password = tk.Entry(login, textvariable=self.password, show="*")
    entry_password.grid(row=1, column=1)

    button_enter_login = tk.Button(login, text="Login", command=self.login)
    button_enter_login.grid(row=2, columnspan=2, pady=10)

    button_voltar = tk.Button(login, text="Voltar", command= login.destroy)
    button_voltar.grid(row=3, columnspan=2)

  def login(self):
    # Lógica de login aqui
    username = self.username.get()
    password = self.password.get()
    # Verificar se o usuário e senha estão corretos
    if username in self.usuarios and self.usuarios[username] == password:
      messagebox.showinfo("Login", "Login bem-sucedido!")
      self.abrir_janela_previsao()
    else:
      messagebox.showerror("Login", "Usuário ou senha incorretos.")
  
  def abrir_janela_previsao(self):
    root_previsao = tk.Toplevel()  # Criar uma nova janela para a previsão
    previsao.PrevisaoTempoApp(root_previsao, previsao.OpenWeatherMapAPI(previsao.API_KEY))  # Inicializar a aplicação de previsão
    root_previsao.protocol("WM_DELETE_WINDOW", self.voltar_janela_inicial)  # Definir protocolo para fechar a janela

    def voltar_janela_inicial(self):
      self.root.deiconify()  # Tornar visível a janela inicial
      root_previsao.destroy()  # Destruir a janela de previsão

  def janela_cadastro(self):
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro")

    # Limpar campos de entrada ao mostrar a janela de cadastro
    self.username.set("")
    self.password.set("")

    # Interface de Cadastro
    label_cadastro_username = tk.Label(cadastro, text="Novo Usuário:")
    label_cadastro_username.grid(row=0, column=0, sticky="e")

    entry_cadastro_username = tk.Entry(cadastro, textvariable=self.username)
    entry_cadastro_username.grid(row=0, column=1)

    label_cadastro_password = tk.Label(cadastro, text="Nova Senha:")
    label_cadastro_password.grid(row=1, column=0, sticky="e")

    entry_cadastro_password = tk.Entry(cadastro, textvariable=self.password, show="*")
    entry_cadastro_password.grid(row=1, column=1)

    button_confirmar_cadastro = tk.Button(cadastro, text="Cadastrar", command=self.cadastrar)
    button_confirmar_cadastro.grid(row=2, columnspan=2, pady=10)

    button_voltar = tk.Button(cadastro, text="Voltar", command= cadastro.destroy)
    button_voltar.grid(row=3, columnspan=2)

  def cadastrar(self):
    # Lógica de cadastro aqui
    username = self.username.get()
    password = self.password.get()
    if username in self.usuarios:
      messagebox.showerror("Cadastro", "Usuário já existe.")
    else:
      self.usuarios[username] = password
      self.salvar_usuarios()
      messagebox.showinfo("Cadastro", f"Usuário {username} cadastrado com sucesso!")

  def carregar_usuarios(self):
    try:
      with open("usuarios.json", "r") as f:
          return json.load(f)
    except FileNotFoundError:
      return {}

  def salvar_usuarios(self):
    with open("usuarios.json", "w") as f:
      json.dump(self.usuarios, f)