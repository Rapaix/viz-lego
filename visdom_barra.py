import visdom
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def gerar_barras(entrada):
    quantidade = len(entrada)
    position_x = []
    valorbar = []
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))

    for i in range(0, quantidade):
        position_x.append(i)
        valorbar.append(entrada[i]["Height"])

    barlist = plt.bar(position_x, valorbar)
    for i in range(0, quantidade):
        barlist[i].set_color(entrada[i]["color"])

    vis = visdom.Visdom()
    vis.close(win=None)
    return vis.matplot(plt)
