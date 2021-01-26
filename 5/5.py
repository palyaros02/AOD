from ctypes import windll
from PIL import Image, ImageTk
from tkinter import Tk, Button, Entry, Frame
from tkinter.ttk import Frame, Label, Entry, LabelFrame
import networkx as nx
import matplotlib.pyplot as plt
windll.shcore.SetProcessDpiAwareness(True)

entries = [] #массив полей для отрисовки
cells = [[], []] #значения клеток
size = 0 #размер матрицы
nodes = [] #узлы
matrix = [] #матрица

def calculate():   # расчет пути
    def dijkstra(cur): #алгоритм дейкстры
        temp = norm(cur)
        while(temp != []):
            node = temp[temp.index(min(temp[1::2]))-1]
            # если узел не посещен и его вес больше потенициального
            if (G[node]['seen'] == 0 and G[node]['weight'] > G[cur]['weight'] + G[cur][node]):
                # присвоить этому узлу новый вес и путь
                G[node]['weight'] = G[cur]['weight']+G[cur][node]
                G[node]['path'] = G[cur]['path']+'-'+node
            temp.remove(G[cur][node]); temp.remove(node)
        G[cur]['seen']=1
    def norm(cur):  # функция для распаковки словаря
        out = []
        for i in G[cur].items():
            out.append(i[0])
            out.append(i[1])
        return out[6::]
    def min_():  # функция поиска непосещенного узла с минимальным весом
        t = [None, float('inf')]
        for node in nodes:
            if G[node]['seen']==0 and G[node]['weight'] < t[1]:
                t[0] = node
                t[1] = G[node]['weight']
        return(t[0])
    # создание словаря из матрицы
    G = dict.fromkeys(nodes)
    for i in range(size):
        tmpDict = {'seen': 0, 'path': '', 'weight': float('inf')}
        for j in range(size):
            if matrix[i][j] != 0:
                tmpDict[nodes[j]] = matrix[i][j]
        G[nodes[i]] = tmpDict
    # получение узлов из GUI
    first = fromEntry.get().upper()
    last = toEntry.get().upper()

    G[first]['path'] = first
    G[first]['weight'] = 0

    for i in range(size):
        dijkstra(min_())
    # запись узлов в GUI
    pathText['text'] = 'Путь: '+G[last]['path']
    lengthText['text'] = 'Длина пути: '+str(G[last]['weight'])

# переформатирование матрицы
def setSize(x):
    global size
    global matrixFrame
    size = int(x)
    matrixFrame.destroy()
    matrixFrame = Frame(leftFrame)
    matrixFrame.pack(pady=5, padx=5)
    createMatrix()

# заполнение примером из дано
def fill():
    global size
    global entries
    global cells
    setSize(9)
    letters = list("ABDGLMNRS")
             # A  #B  #D  #G  #L  #M  #N  #R  #S
    edges = [[ 0, 27,  0,  0,  0, 15,  0,  0,  0],  # A
             [27,  0,  0,  9,  7,  0,  0,  0,  0],  # B
             [ 0,  0,  0,  0,  0, 21,  0, 32, 17],  # D
             [ 0,  9,  0,  0,  0,  0,  8,  0, 11],  # G
             [ 0,  7,  0,  0,  0,  0, 10,  0,  0],  # L
             [15,  0, 21,  0,  0,  0,  0,  0, 15],  # M
             [ 0,  0,  0,  8, 10,  0,  0, 31,  0],  # N
             [ 0,  0, 32,  0,  0,  0, 31,  0,  0],  # R
             [ 0,  0, 17, 11,  0, 15,  0,  0,  0]]  # S

    for r in range(size):
        cells[0][r].delete(0, "end")
        cells[0][r].insert(0, letters[r])
        for c in range(size):
            entries[r][c].delete(0, "end")
            entries[r][c].insert(0, edges[r][c])
    update()
    drawGraph()

# отрисовка матрицы
def createMatrix():
    global entries
    global cells
    entries = []
    cells = [[], []]
    for r in range(size):
        entries.append([])
        cells[0].append(Entry(matrixFrame, width=3))
        cells[0][r].grid(row=0, column=r + 1)
        for c in range(size):
            cells[1].append(Entry(matrixFrame, width=3, state="disabled"))
            cells[1][r].grid(row=r + 1, column=0)
            entries[r].append(Entry(matrixFrame, width=3))
            entries[r][c].insert(0, '0')
            if c <= r:
                entries[r][c]['state'] = 'disabled'
            entries[r][c].grid(row=r + 1, column=c + 1)

    matrixFrame.update()
# обновление значений
def update():
    for r in range(size):
        t = cells[0][r].get().upper()
        cells[0][r].delete(0, "end")
        cells[0][r].insert(0, t)
        cells[1][r]['state'] = "normal"
        cells[1][r].delete(0, "end")
        cells[1][r].insert(0, cells[0][r].get())
        cells[1][r]['state'] = "disabled"
        for c in range(size):
            if c < r:
                entries[r][c]['state'] = "normal"
                entries[r][c].delete(0, "end")
                entries[r][c].insert(0, entries[c][r].get())
                entries[r][c]['state'] = "disabled"

# получение значений из матрицы GUI
def getMatrix():
    update()
    global nodes
    global matrix
    nodes = []
    matrix = []
    for r in range(size):
        matrix.append([])
        nodes.append(cells[0][r].get())
        for c in range(size):
            if c >= r:
                matrix[r].append(int(entries[r][c].get()))
            elif c < r:
                matrix[r].append(int(entries[c][r].get()))

# отрисовка графа
def drawGraph():
    getMatrix()
    g = []
    for i in range(size):
        for j in range(size):
            if matrix[i][j] != 0:
                g.append([[nodes[i], nodes[j]], matrix[i][j]])
    G = nx.Graph()
    for i in range(len(g)):
        G.add_edge(*g[i][0], weight=g[i][1])
    pos = nx.fruchterman_reingold_layout(G)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_nodes(G, pos, node_size=600)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.savefig('output.png')
    plt.close()

    panel.configure(image=img1)
    panel.image = img1

    img2 = ImageTk.PhotoImage(Image.open('output.png'))
    panel.configure(image=img2)
    panel.image = img2


if __name__ == '__main__':
    window = Tk()
    window.title("Графы")

    leftFrame = Frame(window)
    leftFrame.pack(side="left")
# левая панель
    Button(leftFrame, text="Граф из примера", bg='green', command=fill).pack()
    Label(leftFrame, text="Введите матрицу: ", font=('arial', 10, 'bold')).pack(side="top")
# логика
    textFrame = Frame(leftFrame); textFrame.pack()
    Label(textFrame, text="Размер:").pack(side="left")
    sizeEntry = Entry(textFrame, width=3); sizeEntry.pack(side="left")
    getSizeBtn = Button(textFrame, text="OK", width=3, command=lambda: setSize(sizeEntry.get()))
    getSizeBtn.pack(padx=10, side="left")
# матрица
    matrixFrame = Frame(leftFrame); matrixFrame.pack(pady=5, padx=5)
# кнопки
    btnsFrame = Frame(leftFrame); btnsFrame.pack(side="bottom")
    Button(btnsFrame, text="Обновить", width=10, command=update).pack(side="left")
    Button(btnsFrame, text="Отрисовать", width=10, command=drawGraph).pack(side="right")
# панель с графиком
    graphFrame = Frame(window); graphFrame.pack(side='left')
    img1 = ImageTk.PhotoImage(Image.open('plaseholder.png'))
    panel = Label(graphFrame, image=img1); panel.pack(fill='both')
# правая панель
    rightFrame = Frame(window); rightFrame.pack(side='right')
    pointsFrame = LabelFrame(rightFrame, text="Узлы:"); pointsFrame.pack()
    fromEntry = Entry(pointsFrame, width=3); fromEntry.pack(side='left')
    toEntry = Entry(pointsFrame, width=3); toEntry.pack(side='left')
    Button(pointsFrame, text='OK', command=calculate).pack(side='left')
    pathText = Label(rightFrame, text='Путь:', font=('arial', 10, 'bold')); pathText.pack()
    lengthText = Label(rightFrame, text='Длина пути:', font=('arial', 10, 'bold')); lengthText.pack()

    window.mainloop()
