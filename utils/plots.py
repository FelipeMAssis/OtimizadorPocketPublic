import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from matplotlib.patches import Circle

# Define tema para plots
sns.set_theme()
color = sns.color_palette()

# Cria uma imagem esquemática do molejo
def plot_molejo(largura, comprimento, molas_largura, molas_comprimento, D_barril, xm, ym):
    matplotlib.rcParams.update({'font.size': 22})
    fig, axs = plt.subplots(1,2,facecolor='white', figsize=(20, 10))
    axs[0].plot([-largura/2, largura/2, largura/2, -largura/2, -largura/2], [comprimento/2, comprimento/2, -comprimento/2, -comprimento/2, comprimento/2], color='black')
    for x, y in zip(xm.flatten(), ym.flatten()):
        axs[0].add_artist(Circle((x, y), D_barril/2000, fill=False, ec='black'))
    add_cota(axs[0], True, comprimento/2, -largura/2, largura/2, (comprimento/2)+8*0.03, f'{largura:.2f} m\n({molas_largura:.0f} molas)', 0.03)
    add_cota(axs[0], False, largura/2, -comprimento/2, comprimento/2, (largura/2)+8*0.03, f'{comprimento:.2f} m\n({molas_comprimento:.0f} molas)', 0.03)
    axs[0].axis('equal')
    axs[0].axis('off')
    intercessao_diametro_barril = D_barril-int(largura*1000/int(molas_largura))
    min_D_barril = int(largura*1000/int(molas_largura))+1
    max_D_barril = 3+min_D_barril
    if D_barril>max_D_barril or D_barril<min_D_barril:
        axs[0].annotate(f'O diâmetro do barril deve ser entre {min_D_barril} mm e {max_D_barril} mm', (0,-1.1*comprimento/2), color='red', ha='center', va='top')

    x_det = [xm[0][0], xm[0][1], xm[0][0], xm[0][1]]
    y_det = [ym[0][0], ym[0][0], ym[1][0], ym[1][0]]
    axs[1].plot([x_det[0]-D_barril/2000, x_det[1]+D_barril/2000, x_det[1]+D_barril/2000, x_det[0]-D_barril/2000, x_det[0]-D_barril/2000], [y_det[0]-D_barril/2000, y_det[0]-D_barril/2000, y_det[2]+D_barril/2000, y_det[2]+D_barril/2000, y_det[0]-D_barril/2000], color='gray', linestyle='--')
    axs[1].scatter(x_det, y_det, color='gray', marker='+')
    axs[1].plot([x_det[0], x_det[0]], [y_det[0]+D_barril/2000, y_det[2]-D_barril/2000], color='black')
    axs[1].plot([x_det[1], x_det[1]], [y_det[0]+D_barril/2000, y_det[2]-D_barril/2000], color='black')
    axs[1].annotate('4 molas em detalhe:', ((x_det[0]+x_det[1])/2, y_det[2]+D_barril/2000), ha='center', va='bottom')
    for x, y in zip(x_det, y_det):
        axs[1].add_artist(Circle((x, y), D_barril/2000, fill=False, ec='black'))
    axs[1].axis('equal')
    axs[1].axis('off')
    if D_barril>max_D_barril or D_barril<min_D_barril:
        axs[1].plot([x_det[0]+D_barril/2000, x_det[1]-D_barril/2000], [y_det[0], y_det[0]], color='red', marker='.', markersize=30, linewidth=10, linestyle=':')
        axs[1].plot([x_det[0]+D_barril/2000, x_det[1]-D_barril/2000], [y_det[2], y_det[2]], color='red', marker='.', markersize=30, linewidth=10, linestyle=':')
    return fig

# Cria uma imagem da mola
def plot_mola(x, z, altura_livre, D_barril, D_boca, ens):
    matplotlib.rcParams.update({'font.size': 18})
    fig, ax = plt.subplots(facecolor='white', figsize=(5, 8))
    # ax.plot([min(x)-20, max(x)+20], [ens, ens], color = color[1], label='Altura Ensacada')
    add_cota(ax, False, D_boca/2, 0, altura_livre, D_boca/2+8*6, f'{altura_livre:.0f} mm', 6)
    add_cota(ax, True, altura_livre/2, -D_barril/2, D_barril/2, altura_livre+8*6, f'{D_barril:.0f} mm', 6)
    add_cota(ax, True, 0, -D_boca/2, D_boca/2, -8*6, f'{D_boca:.0f} mm', 6)
    ax.plot(x, z, label='Mola Livre', color='black')
    ax.axis('equal')
    # ax.legend()
    # ax.set_xlabel('Base (mm)')
    # ax.set_ylabel('Altura (mm)')
    ax.axis('off')
    return fig

def add_cota(ax, horizontal, y_face, x_start, x_end, y_arrow, text, space):
    if horizontal:
        va = 'bottom'

        if y_face>y_arrow:
            space = -space
            va = 'top'
        
        ax.plot([x_start, x_start], [y_face+space, y_arrow+3*space], color='gray')
        ax.plot([x_end, x_end], [y_face+space, y_arrow+3*space], color='gray')
        ax.arrow((x_end+x_start)/2, y_arrow, (x_end-x_start)/2-3*abs(space), 0, color='gray', head_width=abs(space), head_length=3*abs(space))
        ax.arrow((x_end+x_start)/2, y_arrow, -(x_end-x_start)/2+3*abs(space), 0, color='gray', head_width=abs(space), head_length=3*abs(space))
        ax.annotate(text, ((x_end+x_start)/2, y_arrow+space), va = va, ha = 'center', color='gray')
    
    else:
        ha = 'left'

        if y_face>y_arrow:
            space = -space
            ha = 'right'

        ax.plot([y_face+space, y_arrow+3*space], [x_start, x_start], color='gray')
        ax.plot([y_face+space, y_arrow+3*space], [x_end, x_end], color='gray')
        ax.arrow(y_arrow, (x_end+x_start)/2, 0, (x_end-x_start)/2-3*abs(space), color='gray', head_width=abs(space), head_length=3*abs(space))
        ax.arrow(y_arrow, (x_end+x_start)/2, 0, -(x_end-x_start)/2+3*abs(space), color='gray', head_width=abs(space), head_length=3*abs(space))
        ax.annotate(text, (y_arrow+space, (x_end+x_start)/2), va = 'center', ha = ha, color='gray', rotation='vertical')