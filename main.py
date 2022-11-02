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
    global conn, cursor
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `aluno` (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT, sobrenome TEXT, email TEXT)")
    
def cadastrar():
    if  nome.get() == "" or sobrenome.get() == ""  or email.get() == "":
        tkinter.messagebox.showinfo(title="Erro",message="Preencha todos os campos!")
    else:
        banco()
        cursor.execute("INSERT INTO `aluno` (nome, sobrenome, email) VALUES(?, ?, ?)", (str(nome.get()), str(sobrenome.get()), str(email.get())))
        conn.commit()
        nome.delete(0,"end")
        sobrenome.delete(0,"end")
        email.delete(0,"end")
        cursor.close()
        conn.close()
        tkinter.messagebox.showinfo(title="Sucesso!", message="Aluno cadastrado!")

def consultar():
    tree.delete(*tree.get_children())
    banco()
    cursor.execute("SELECT * FROM `aluno` ORDER BY `nome` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[1], data[2], data[3]))
    cursor.close()
    conn.close()
    
def sair():
    result = tkMessageBox.askquestion('Cadastro Alunos', 'Tem certeza que deseja sair?', icon="warning")
    if result == 'yes':
        principal.destroy()
        exit()

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
txt_title = Label(topo, width=600, font=('arial', 18), text = "Cadastro de alunos", background=cor2)
txt_title.pack()
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
btn_sair = Button(Buttons, width=10, text="Exit", command=sair)
btn_sair.pack(side=LEFT)

# treeview
scrollbary = Scrollbar(direita, orient=VERTICAL)
scrollbarx = Scrollbar(direita, orient=HORIZONTAL)
tree = ttk.Treeview(direita, columns=("Nome", "Sobrenome", "Email"), selectmode="extended", height=200, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Nome', text="Nome", anchor=W)
tree.heading('Sobrenome', text="Sobrenome", anchor=W)
tree.heading('Email', text="E-mail", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=80)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.pack()

principal.mainloop()
