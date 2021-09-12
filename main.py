import tkinter as tk
import tkinter.messagebox
import win32clipboard
from lxml import html
import requests
import operator



# GUI definition
app = tk.Tk()
app.geometry = ('400x400')
item = tk.StringVar()
entryItem = tk.Entry(app, width=20, textvariable=item)
entryItem.grid(column=2, row=1, padx=10)


def getInfo():
    itemName = item.get().splitlines()[1]
    chaos={0:0}
    exa={0:0}
    page = requests.get('https://poedb.tw/tw/xyz.php?rarity=unique&league=Warbands&status=1&name=' + itemName)
    tree = html.fromstring(page.content)
    text = tree.xpath("//span[@data-name='price']/text()")
    print(text)
    for x in text:
        tmp = x.split('<')
        tmp[0] = tmp[0].split('x')[0]
        tmp[-1] = tmp[-1].split('>')[-1]
        if tmp[-1] == "混沌石":
            if tmp[0] not in chaos:
                chaos[tmp[0]] = 1
            else:
                chaos[tmp[0]] = chaos[tmp[0]] + 1
        elif tmp[-1] == "崇高石":
            if tmp[0] not in exa:
                exa[tmp[0]] = 1
            else:
                exa[tmp[0]] = exa[tmp[0]] + 1

    # output the largest amount of entry in market
    highestChaos=int(max(chaos.values()))
    highestExa=int(max(exa.values()))
    if highestChaos>highestExa:
        for x in chaos:
            if chaos[x] ==highestChaos:
                output.set(str(x) + " chaos"+"\n")
    else:
        for x in exa:
            if exa[x]==highestExa:
                output.set(str(x) + " exa"+"\n")


def getAllInfo():
    output.set('')
    chaos={0:0}
    exa={0:0}
    itemName = item.get().splitlines()[1]
    page = requests.get('https://poedb.tw/tw/xyz.php?rarity=unique&league=Warbands&status=1&name=' + itemName)
    tree = html.fromstring(page.content)
    text = tree.xpath("//span[@data-name='price']/text()")
    print(len(text))
    text=[''.join(x) for x in zip(text[0::2], text[1::2])]
    for x in text:
        tmp=x.split('x')
        if tmp[-1] == "混沌石":
            if tmp[0] not in chaos:
                chaos[tmp[0]] = 1
            else:
                chaos[tmp[0]] = chaos[tmp[0]] + 1
        elif tmp[-1] == "崇高石":
            if tmp[0] not in exa:
                exa[tmp[0]] = 1
            else:
                exa[tmp[0]] = exa[tmp[0]] + 1

    # output all info
    for x in chaos:
        if x!=0:
            output.set(output.get()+str(x)+" chaos: "+str(chaos[x])+"\n")
    for x in exa:
        if x!=0:
            output.set(output.get() + str(x) + " exa: " + str(exa[x]) + "\n")


output = tk.StringVar(app)
buttonReturnName = tk.Button(app, text='Most Common', command=getInfo)
buttonReturnName.grid(column=1, row=2, pady=10)
buttonReturnAllName=tk.Button(app,text='All', command=getAllInfo)
buttonReturnAllName.grid(column=3,row=2,pady=10)
labelResult = tk.Label(app, textvariable=output)
labelResult.grid(column=2, row=3)

# driver function
app.mainloop()
