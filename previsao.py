import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests
from unidecode import unidecode

API_KEY = "6d6e9292b0f133dbdc75754bc58cc44f"  

class OpenWeatherMapAPI:
  def __init__(self, api_key):
      self.api_key = api_key
      self.base_url = "https://api.openweathermap.org/data/2.5"

  def buscar_previsao_atual_api(self, cidade):
    cidade = unidecode(cidade)
    link = f"{self.base_url}/weather?q={cidade}&appid={self.api_key}"
    return requests.get(link).json()

  def buscar_previsao_periodo_api(self, cidade, data_inicio, data_fim):
    cidade = unidecode(cidade)
    link = f"{self.base_url}/forecast?q={cidade}&appid={self.api_key}"
    resposta = requests.get(link).json()
    previsoes = resposta.get("list", [])
    
    temperaturas = []
    for previsao in previsoes:
      data_previsao = datetime.fromtimestamp(previsao["dt"])
      if data_inicio <= data_previsao <= data_fim:
          temperatura = previsao["main"]["temp"] # Dicionário e lista de main onde deseja-se a temp
          temperatura_celsius = temperatura - 273.15
          temperaturas.append(temperatura_celsius)

    return temperaturas

# Possui uma instância de OpenWeatherMapAPI
class PrevisaoTempoApp:
  def __init__(self, root, api):
    self.root = root
    self.api = api
    self.root.title("Previsão do Tempo")

    self.label_cidade = tk.Label(root, text="Digite o nome da cidade:")
    self.label_cidade.pack()

    self.entry_cidade = tk.Entry(root)
    self.entry_cidade.pack()

    self.label_data_inicio = tk.Label(root, text="Data de Início (AAAA-MM-DD):")
    self.label_data_inicio.pack()

    self.entry_data_inicio = tk.Entry(root)
    self.entry_data_inicio.pack()

    self.label_data_fim = tk.Label(root, text="Data de Término (AAAA-MM-DD):")
    self.label_data_fim.pack()

    self.entry_data_fim = tk.Entry(root)
    self.entry_data_fim.pack()

    self.button_buscar = tk.Button(root, text="Buscar", command=self.buscar_previsao_periodo)
    self.button_buscar.pack()

    self.button_atual = tk.Button(root, text="Tempo Agora", command=self.buscar_previsao_atual)
    self.button_atual.pack()

  def buscar_previsao_periodo(self):
    cidade = self.entry_cidade.get()
    data_inicio = self.entry_data_inicio.get()
    data_fim = self.entry_data_fim.get()

    if cidade and data_inicio and data_fim:
      try:
        data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d")
        data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d")
      except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Use o formato AAAA-MM-DD.")
        return

      if data_inicio_obj > data_fim_obj:
        messagebox.showerror("Erro", "A data de início deve ser anterior à data de término.")
        return

      temperaturas = self.api.buscar_previsao_periodo_api(cidade, data_inicio_obj, data_fim_obj) # Composição

      if temperaturas:
        temperatura_media = sum(temperaturas) / len(temperaturas)
        messagebox.showinfo("Previsão do Tempo", f"A temperatura média em {cidade} entre {data_inicio} e {data_fim} é {temperatura_media:.2f}°C")
      else:
        messagebox.showerror("Erro", "Não há previsões de temperatura para o período especificado.")
    else:
      messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

  def buscar_previsao_atual(self):
    cidade = self.entry_cidade.get()

    if cidade:
      dados = self.api.buscar_previsao_atual_api(cidade) # Composição
      if dados["cod"] == 200:
        temperatura = dados["main"]["temp"] # Dicionário e lista de main onde deseja-se a temp
        temperatura_celsius = temperatura - 273.15
        messagebox.showinfo("Previsão do Tempo Agora", f"A temperatura em {cidade} agora é {temperatura_celsius:.2f}°C")
      else:
        messagebox.showerror("Erro", "Cidade não encontrada.")
    else:
      messagebox.showerror("Erro", "Por favor, digite o nome da cidade.")