from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import accounts

import searcher

root = Tk()

buscador = searcher.searcher()


def buscar():
    aux = buscador.get_data(entry.get('1.0', 'end-1c'))
    autor['text'] = "Autor: " + aux[1]
    if aux[0] != searcher.type.USER:
        info_text['text'] = "Texto: " + aux[2]
    num_temas = 4
    temas = buscador.get_k_temas_vecinos(num_temas, aux[3])
    tree_tema.delete(*tree_tema.get_children())
    tree_cuentas.delete(*tree_cuentas.get_children())
    tree_tweets.delete(*tree_tweets.get_children())
    for i in range(0, num_temas):
        tree_tema.insert("", i, values=(i+1, temas[0][i]))

    num_cuentas = 6
    cuentas = buscador.get_k_cuentas_vecinos(num_cuentas, aux[3])
    for i in range(0, num_cuentas):
        tree_cuentas.insert("", i, values=(i+1, "@"+cuentas[0][i], accounts.get_tema_by_account(cuentas[0][i])))

    num_tweets = 10
    tweets = buscador.get_k_tweets_vecinos(num_tweets, aux[3])
    for i in range(0, num_tweets):
        datos=buscador.get_tweet_data(tweets[0][i])
        tree_tweets.insert("", i, values=(i+1,"@"+datos[0],datos[1],datos[2]))


def tree_columna_numero_temas(tree):
    tree.column("#0", width=0, stretch=NO, anchor=E)
    tree.column("Numero", width=75, minwidth=50, stretch=NO, anchor=E)
    tree.heading("Numero", anchor=E)
    tree.column("Temas", minwidth=75, stretch=Y, anchor=W)
    tree.heading("Temas", text="Temas", anchor=W, )


def tree_columna_nombre(tree):
    tree.column("Nombre", width=150, minwidth=75, stretch=NO, anchor=W)
    tree.heading("Nombre", text="Nombre", anchor=W, )


root.geometry("800x600")
root.title("Buscador Twiteer")

titulo = Label(root, text="Buscador Semantico Twiiter", font=('Helvetica', 10))
titulo.pack()

frame = Frame(root, padx=5, pady=5)
frame.pack(padx=10, pady=10)
# entry = Entry(frame, width=40,height=20, font=('Helvetica', 15))
# entry.grid(row=1, column=0, columnspan=3, pady=5, padx=10)
entry = Text(frame, width=100, height=2, font=('Helvetica', 10))
entry.grid(row=0, column=0, columnspan=3, pady=5, padx=5)

button_search = Button(frame, text="Buscar", command=buscar)
button_search.grid(row=1, column=3, padx=5)

autor = Label(root, anchor="w", text=" ", font=('Helvetica', 10), justify=LEFT, )
autor.pack(padx=15, pady=5, fill="x")
# autor.grid(row=2, column=0,columnspan=3, pady=5, padx=5)
info_text = Label(root, anchor="w", wraplengt=700, text=" ", font=('Helvetica', 10), justify=LEFT)
info_text.pack(padx=15, pady=5, fill="x")


# info_text.grid(row=3, column=0,columnspan=3, pady=5, padx=5)


def motion_handler(tree, event):
    f = Font(font='TkDefaultFont')

    # A helper function that will wrap a given value based on column width
    def adjust_newlines(val, width, pad=10):
        if not isinstance(val, str):
            return val
        else:
            words = val.split()
            lines = [[], ]
            for word in words:
                line = lines[-1] + [word, ]
                if f.measure(' '.join(line)) < (width - pad):
                    lines[-1].append(word)
                else:
                    lines[-1] = ' '.join(lines[-1])
                    lines.append([word, ])

            if isinstance(lines[-1], list):
                lines[-1] = ' '.join(lines[-1])

            return '\n'.join(lines)

    if (event is None) or (tree.identify_region(event.x, event.y) == "separator"):
        # You may be able to use this to only adjust the two columns that you care about
        # print(tree.identify_column(event.x))

        col_widths = [tree.column(cid)['width'] for cid in tree['columns']]

        for iid in tree.get_children():
            new_vals = []
            for (v, w) in zip(tree.item(iid)['values'], col_widths):
                new_vals.append(adjust_newlines(v, w))
            tree.item(iid, values=new_vals)


s = ttk.Style()
s.configure('Treeview', rowheight=40)


def create_tree(pestanya):
    frame = Frame(pestanya, padx=5, pady=5)
    frame.pack(padx=10, pady=10, fill=BOTH)
    tree = ttk.Treeview(frame)
    scrollbar_vertical = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)

    # scrollbar_vertical.grid(row=0,column=1,sticky=N+S )
    tree.configure(yscrollcommand=scrollbar_vertical.set)

    tree.pack(side=LEFT, fill=BOTH)
    scrollbar_vertical.pack(side=LEFT, fill=Y)
    # tree.grid(row=0, column=0,sticky=W+E )
    tree.bind('<B1-Motion>', partial(motion_handler, tree))
    motion_handler(tree, None)  # Perform initial wrapping
    return tree


nb = ttk.Notebook(root)
nb.pack()
pestanya_temas = Frame(nb)
pestanya_cuentas = Frame(nb)
pestanya_tweets = Frame(nb)
# temas
tree_tema = create_tree(pestanya_temas)
tree_tema['columns'] = ("Numero", 'Temas', 'resto')
tree_columna_numero_temas(tree_tema)

# cuentas
tree_cuentas = create_tree(pestanya_cuentas)
tree_cuentas['columns'] = ("Numero", 'Nombre', 'Temas')
tree_columna_numero_temas(tree_cuentas)
tree_columna_nombre(tree_cuentas)

# tweets
tree_tweets = create_tree(pestanya_tweets)
tree_tweets['columns'] = ("Numero", 'Nombre', 'Temas', 'Tweet')
tree_columna_numero_temas(tree_tweets)
tree_columna_nombre(tree_tweets)
tree_tweets.column("Tweet", width=300, minwidth=200, stretch=Y, anchor=W)
tree_tweets.heading("Tweet", text="Tweet", anchor=W, )

nb.add(pestanya_temas, text="Temas ")
nb.add(pestanya_cuentas, text="Cuentas similares")
nb.add(pestanya_tweets, text="Tweets similares")

root.mainloop()
