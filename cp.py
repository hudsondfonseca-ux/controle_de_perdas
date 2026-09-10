import csv
from datetime import datetime
import sqlite3
from tkinter import filedialog
import customtkinter as ctk
import matplotlib.pyplot as plt

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ------------------------------------------------------------------
# 1. BANCO DE DADOS E EXPORTAÇÃO
# ------------------------------------------------------------------
def criar_banco_de_dados():
  conexao = sqlite3.connect("perdas.db")
  cursor = conexao.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            operador TEXT NOT NULL,
            maquina TEXT NOT NULL,
            amostras INTEGER NOT NULL,
            kilos REAL NOT NULL,
            peso_perdido REAL NOT NULL,
            porcentagem REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)
  conexao.commit()
  conexao.close()


def salvar_registro(
    operador, maquina, amostras, kilos, peso_perdido, porcentagem, status
):
  conexao = sqlite3.connect("perdas.db")
  cursor = conexao.cursor()
  data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

  cursor.execute(
      """
        INSERT INTO registros (data_hora, operador, maquina, amostras, kilos, peso_perdido, porcentagem, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
      (
          data_hora_atual,
          operador,
          maquina,
          amostras,
          kilos,
          peso_perdido,
          porcentagem,
          status,
      ),
  )

  conexao.commit()
  conexao.close()


def exportar_csv():
  try:
    conexao = sqlite3.connect("perdas.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, data_hora, operador, maquina, amostras, kilos, peso_perdido,"
        " porcentagem, status FROM registros"
    )
    registros = cursor.fetchall()
    conexao.close()

    if not registros:
      lbl_resultado.configure(
          text="Nenhum registro encontrado para exportar.", text_color="#FFCC00"
      )
      return

    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivo CSV (Excel)", "*.csv")],
        title="Salvar Relatório de Perdas",
    )

    if caminho_arquivo:
      with open(
          caminho_arquivo, mode="w", newline="", encoding="utf-8-sig"
      ) as f:
        escritor = csv.writer(f, delimiter=";")
        escritor.writerow([
            "ID",
            "Data/Hora",
            "Operador",
            "Máquina",
            "Amostras",
            "Peso p/ Amostra (kg)",
            "Peso Perdido (kg)",
            "Porcentagem (%)",
            "Status",
        ])
        escritor.writerows(registros)

      lbl_resultado.configure(
          text="Relatório exportado com sucesso!", text_color="#2FA572"
      )
  except Exception as e:
    lbl_resultado.configure(
        text=f"Erro ao exportar arquivo: {e}", text_color="red"
    )


# ------------------------------------------------------------------
# 2. DASHBOARD DE GRÁFICOS (PASSO 3)
# ------------------------------------------------------------------
def gerar_grafico():
  conexao = sqlite3.connect("perdas.db")
  cursor = conexao.cursor()
  cursor.execute(
      "SELECT data_hora, porcentagem, maquina, status FROM registros ORDER BY"
      " id DESC LIMIT 15"
  )
  registros = cursor.fetchall()
  conexao.close()

  if not registros:
    lbl_resultado.configure(
        text="Sem dados suficientes para gerar gráfico.", text_color="#FFCC00"
    )
    return

  # Inverte para exibir do mais antigo para o mais recente
  registros.reverse()

  labels = [f"{r[2]}\n({r[0].split()[0]})" for r in registros]
  porcentagens = [r[1] for r in registros]
  cores = ["#FF4D4D" if r[3] == "SEGREGADA" else "#2FA572" for r in registros]

  plt.figure(figsize=(9, 5))
  bars = plt.bar(labels, porcentagens, color=cores, width=0.5)

  plt.axhline(
      y=0.30, color="red", linestyle="--", label="Limite Tolerado (0.30%)"
  )
  plt.ylabel("Perda (%)")
  plt.title("Histórico Recente de Perdas por Máquina")
  plt.legend()
  plt.grid(axis="y", linestyle=":", alpha=0.6)

  for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 0.01,
        f"{yval:.2f}%",
        ha="center",
        va="bottom",
        fontsize=8,
    )

  plt.tight_layout()
  plt.show()


# Inicializa Banco
criar_banco_de_dados()


# ------------------------------------------------------------------
# 3. LÓGICA DO SISTEMA
# ------------------------------------------------------------------
def calcular_perda():
  try:
    operador = entry_operador.get().strip()
    maquina = combo_maquina.get()
    amostras = float(entry_amostras.get())
    kilos = float(entry_kilos.get())
    peso_perdido = float(entry_perdido.get())

    if not operador:
      lbl_resultado.configure(
          text="Informe o nome do operador.", text_color="red"
      )
      return

    peso_total = amostras * kilos

    if peso_total > 0:
      porcentagem = (peso_perdido / peso_total) * 100

      if porcentagem > 0.30:
        status = "SEGREGADA"
        mensagem = (
            f"Taxa: {porcentagem:.2f}% | A produção da {maquina} deve ser"
            " SEGREGADA!"
        )
        cor = "#FF4D4D"
      else:
        status = "APROVADA"
        mensagem = (
            f"Taxa: {porcentagem:.2f}% | A produção da {maquina} pode SEGUIR."
        )
        cor = "#2FA572"

      lbl_resultado.configure(text=mensagem, text_color=cor)

      salvar_registro(
          operador, maquina, amostras, kilos, peso_perdido, porcentagem, status
      )

    else:
      lbl_resultado.configure(
          text="O peso total deve ser maior que zero.", text_color="red"
      )
  except ValueError:
    lbl_resultado.configure(
        text="Preencha os campos numéricos corretamente.", text_color="red"
    )


# ------------------------------------------------------------------
# 4. INTERFACE GRÁFICA
# ------------------------------------------------------------------
app = ctk.CTk()
app.title("Controle de Perdas Industrial")
app.geometry("440x540")
app.resizable(False, False)

ctk.CTkLabel(
    app, text="Controle de Perdas Industrial", font=("Arial", 18, "bold")
).pack(pady=12)

# Inputs do Passo 2 (Origem)
entry_operador = ctk.CTkEntry(
    app, placeholder_text="Nome do Operador", width=300
)
entry_operador.pack(pady=5)

combo_maquina = ctk.CTkComboBox(
    app,
    values=[
        "PKD 03",
        "PKD 06",
        "PKD 08",
        "PKD 23",
   
    ],
    width=300,
)
combo_maquina.pack(pady=5)

# Inputs de Cálculo
entry_amostras = ctk.CTkEntry(
    app, placeholder_text="Quantidade de amostras", width=300
)
entry_amostras.pack(pady=5)

entry_kilos = ctk.CTkEntry(
    app, placeholder_text="Peso por amostra (kg)", width=300
)
entry_kilos.pack(pady=5)

entry_perdido = ctk.CTkEntry(
    app, placeholder_text="Quantidade perdida (kg)", width=300
)
entry_perdido.pack(pady=5)

# Botões de Ação
btn_calcular = ctk.CTkButton(
    app, text="Calcular e Registrar", command=calcular_perda, width=300
)
btn_calcular.pack(pady=8)

btn_grafico = ctk.CTkButton(
    app,
    text="Ver Dashboard / Gráfico",
    command=gerar_grafico,
    width=300,
    fg_color="#2B2B2B",
    hover_color="#3A3A3A",
    border_width=1,
)
btn_grafico.pack(pady=3)

btn_exportar = ctk.CTkButton(
    app,
    text="Exportar Relatório (Excel)",
    command=exportar_csv,
    width=300,
    fg_color="#1F538D",
    hover_color="#14375E",
)
btn_exportar.pack(pady=3)

lbl_resultado = ctk.CTkLabel(
    app, text="", font=("Arial", 12, "bold"), justify="center", wraplength=380
)
lbl_resultado.pack(pady=10)

app.mainloop()