import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Função para conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('usuario.db')  # Alterado o nome do banco de dados para usuario.db
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT)''')
    conn.commit()
    return conn, cursor

# Função para salvar os dados no banco de dados
def salvar_dados():
    nome = entry_nome.get()
    email = entry_email.get()

    if not nome or not email:
        messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos!")
        return

    conn, cursor = conectar_banco()

    cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', (nome, email))
    conn.commit()

    messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Função para exibir os dados do banco de dados
def exibir_dados():
    conn, cursor = conectar_banco()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()

    for i in tree.get_children():
        tree.delete(i)

    for usuario in usuarios:
        tree.insert("", tk.END, values=(usuario[1], usuario[2]))

    conn.close()

# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Cadastro de Usuários")

# Configuração do formulário
tk.Label(root, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Email:").grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=10, pady=10)

# Botões
btn_salvar = tk.Button(root, text="Salvar", command=salvar_dados)
btn_salvar.grid(row=2, column=0, columnspan=2, pady=10)

# Configuração da Tabela para exibir os dados
tree = ttk.Treeview(root, columns=("Nome", "Email"), show="headings")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Botão para exibir os dados
btn_exibir = tk.Button(root, text="Exibir Dados", command=exibir_dados)
btn_exibir.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
