import tkinter.messagebox
from tkinter import*
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

cor1 = "#B0C4DE"
cor2 = "#6959CD"
principal = Tk()
principal.title("Cadastro de usuários")
principal.config(background = cor1)
principal.geometry("700x300")


# métodos
def banco():
  global conexao, cursor
  conexao = sqlite3.connect('banco.db')
  cursor = conexao.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS `aluno` (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT, sobrenome TEXT, email TEXT)")
    
def cadastrar():
  # se houver campos em branco, exibe mensagem de erro
  if  nome.get() == "" or sobrenome.get() == ""  or email.get() == "":
    tkinter.messagebox.showinfo(title="Erro",message="Preencha todos os campos!")
  # se não, faz o registro no banco de dados
  else:
    banco()# chamar função para conectar ao banco
    cursor.execute("INSERT INTO `aluno` (nome, sobrenome, email) VALUES(?, ?, ?)", (str(nome.get()), str(sobrenome.get()), str(email.get())))
    conexao.commit() # validar inserção
    nome.delete(0,"end") # limpar campo nome
    sobrenome.delete(0,"end") # limpar campo sobrenome
    email.delete(0,"end") # limpar campo e-mail
    cursor.close() # encerrar cursor
    conexao.close() # encerrar conexão
    tkinter.messagebox.showinfo(title="Sucesso!", message="Aluno cadastrado!") # mensagem que inserção ocorreu

def consultar():
  arvore.delete(*arvore.get_children()) #limpar tree view
  banco() # chamar conexão com o banco
  cursor.execute("SELECT * FROM `aluno` ORDER BY `nome` ASC") # seleção com ordenamento por nome
  fetch = cursor.fetchall() # retorna os resultados como tuplas e armazena em fetch
  for dados in fetch: # insere tuplas do fetch na árvore
    arvore.insert('', 'end', values=(dados[0],dados[1], dados[2], dados[3]))
  cursor.close() # encerrar cursor
  conexao.close() # encerrar conexão
    
def sair():
    resultado = tkMessageBox.askquestion('Cadastro Alunos', 'Tem certeza que deseja sair?', icon="warning") #pergunta se deseja realmente sair
    if resultado == 'yes':
        principal.destroy() # fecha tela
        exit()

def deletar():
  banco()
  item = arvore.selection()[0] # recebe item selecionado na árvore
  resultado = tkinter.messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir aluno?", icon="warning")
  if resultado == 'yes':
    for item in arvore.selection():
      cursor.execute("DELETE FROM aluno WHERE id = ?", (arvore.set(item, '#1'),))
      arvore.delete(item)
  conexao.commit()
  conexao.close()

# variáveis
nome = StringVar()
sobrenome = StringVar()
email = StringVar()

# frame
topo = Frame(principal, width=600, height=50, bd=1, relief="raise")
topo.pack(side=TOP)
esquerda = Frame(principal, width=300, height=300, bd=1, relief="raise", background=cor1)
esquerda.pack(side=LEFT)
direita = Frame(principal, width=300, height=300, bd=1, relief="raise")
direita.pack(side=RIGHT)
Forms = Frame(esquerda, width=300, height=300, background=cor1)
Forms.pack(side=TOP)
Buttons = Frame(esquerda, width=100, height=100, background=cor1, relief="raise")
Buttons.pack(side=BOTTOM)

# labels
txt_titulo = Label(topo, width=600, font=('arial', 18), text = "Cadastro de alunos", background=cor2)
txt_titulo.pack()
txt_nome = Label(Forms, text="Nome:", font=('arial', 10), bd=15, background=cor1)
txt_nome.grid(row=0, stick="e")
txt_sobrenome = Label(Forms, text="Sobrenome:", font=('arial', 10), bd=15, background=cor1)
txt_sobrenome.grid(row=1, stick="e")
txt_email = Label(Forms, text="E-mail:", font=('arial', 10), bd=15, background=cor1)
txt_email.grid(row=2, stick="e")

txt_result = Label(Buttons, background=cor1)
txt_result.pack(side=TOP)

# entrys
nome = Entry(Forms, textvariable=nome, width=25)
nome.grid(row=0, column=1)
sobrenome = Entry(Forms, textvariable=sobrenome, width=25)
sobrenome.grid(row=1, column=1)
email = Entry(Forms, textvariable=email, width=25)
email.grid(row=2, column=1)


# botões
btn_cadastrar = Button(Buttons, width=10, text="Cadastrar", command=cadastrar)
btn_cadastrar.pack(side=LEFT)
btn_consultar = Button(Buttons, width=10, text="Consultar", command=consultar)
btn_consultar.pack(side=LEFT)
btn_sair = Button(Buttons, width=10, text="Excluir", command=deletar)
btn_sair.pack(side=LEFT)
btn_sair = Button(Buttons, width=10, text="Sair", command=sair)
btn_sair.pack(side=LEFT)

# treeview
scrollbary = Scrollbar(direita, orient=VERTICAL)
scrollbarx = Scrollbar(direita, orient=HORIZONTAL)
arvore = ttk.Treeview(direita, columns=("Id","Nome", "Sobrenome", "Email"), selectmode="extended", height=200, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=arvore.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=arvore.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
arvore.heading('Id', text="ID", anchor=W)
arvore.heading('Nome', text="Nome", anchor=W)
arvore.heading('Sobrenome', text="Sobrenome", anchor=W)
arvore.heading('Email', text="E-mail", anchor=W)
arvore.column('#0', stretch=NO, minwidth=0, width=0)
arvore.column('#1', stretch=NO, minwidth=0, width=80)
arvore.column('#2', stretch=NO, minwidth=0, width=80)
arvore.column('#3', stretch=NO, minwidth=0, width=80)
arvore.pack()

principal.mainloop()
