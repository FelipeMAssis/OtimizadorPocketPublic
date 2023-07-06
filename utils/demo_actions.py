import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import Bounds, NonlinearConstraint

from . import equations, plots, optimization

def visualize_molejo(
    largura,
    comprimento,
    altura,
    molas_largura,
    molas_comprimento,
    D_barril
):
    x, y = equations.points_molejo(
        largura,
        comprimento,
        molas_largura,
        molas_comprimento,
        D_barril
    )
    fig = plots.plot_molejo(
        largura,
        comprimento,
        molas_largura,
        molas_comprimento,
        D_barril,
        x,
        y
    )
    return fig


def visualize_mola(
        d_arame,
        D_barril,
        D_boca,
        altura_livre,
        altura_ensacada,
        voltas,
        voltas_barril,
        voltas_inativas_i,
        voltas_inativas_f
):
    try:
        x, z = equations.points_mola(
            D_barril-d_arame,
            D_boca-d_arame,
            voltas_barril,
            voltas_inativas_i,
            voltas_inativas_f,
            voltas,
            altura_livre-d_arame
        )
        fig = plots.plot_mola(
            x,
            z,
            altura_livre,
            D_barril,
            D_boca,
            altura_ensacada
        )
    except TypeError:
        fig, ax = plt.subplots()
        # Create a figure and set the background color to white
        fig = plt.figure(facecolor='white')

        # Set the plot dimensions to fill the entire figure
        ax = fig.add_axes([0, 0, 1, 1])

        # Remove the axes
        ax.axis('off')

        # Set the text properties
        text = 'Não foi possível gerar uma visualização\n com os parâmetros fornecidos'
        text_color = 'red'
        text_size = 14
        text_position = (0.5, 0.5)

        # Add the text to the plot
        ax.text(*text_position, text, color=text_color, ha='center', va='center', fontsize=text_size)

    return fig


def calcula_firmeza(
    largura,
    comprimento,
    altura,
    molas_largura,
    molas_comprimento,
    d_arame,
    D_barril,
    D_boca,
    altura_livre,
    voltas,
    voltas_barril,
    voltas_inativas_i,
    voltas_inativas_f,
    manta,
    spring_rate,
    G,
    delta_altura,
    delta_barril,
    delta_boca
):
    try:
        D_med_barril = D_barril-d_arame+delta_barril
        D_med_boca = D_boca-d_arame+delta_boca
        altura_livre += delta_altura
    except TypeError:
        return pd.DataFrame(
                    {
                        '':['Informado pelo usuário', 'Calculado para a mola atual'],
                        'Spring Rate (N/pol)':[np.nan, np.nan],
                        'Firmeza (kgf)':[np.nan, np.nan]
                    }
                ), 0
    try:
        ild_spring_rate_padrao = equations.ild(
            altura_livre,
            altura,
            D_med_boca,
            spring_rate,
            largura,
            comprimento,
            molas_largura,
            molas_comprimento,
            manta
        )
    except TypeError:
        ild_spring_rate_padrao = np.nan
    try:
        spring_rate_estimado = equations.spring_rate(
            d_arame,
            D_med_barril,
            D_med_boca,
            voltas_barril,
            voltas-voltas_inativas_i-voltas_inativas_f,
            G
        )
        ild_spring_rate_estimado = equations.ild(
            altura_livre,
            altura,
            D_med_boca,
            spring_rate_estimado,
            largura,
            comprimento,
            molas_largura,
            molas_comprimento,
            manta
        )
    except TypeError:
        spring_rate_estimado = np.nan
        ild_spring_rate_estimado = np.nan
    return pd.DataFrame(
        {
            '':['Informado pelo usuário:', 'Calculado para a mola atual:'],
            'Spring Rate (N/pol)':[f'{spring_rate:.2f}', f'{spring_rate_estimado:.2f}'],
            'Firmeza (kgf)':[f'{ild_spring_rate_padrao:.2f}', f'{ild_spring_rate_estimado:.2f}']
        }
    ), ild_spring_rate_estimado

def optimize(
    firmeza_esperada,
    tolerance,
    min_pre_compressao,
    max_pre_compressao,
    min_boca_barril,
    max_boca_barril,
    min_voltas,
    max_voltas,
    min_voltas_barril,
    max_voltas_barril,
    min_sm,
    max_sm,
    sm_active,
    min_sa,
    max_sa,
    sa_active,
    min_pct_red,
    max_pct_red,
    pct_red_active,
    min_d_boca,
    max_d_boca,
    d_boca_active,
    largura,
    comprimento,
    altura,
    molas_largura,
    molas_comprimento,
    d_arame,
    D_barril,
    D_boca,
    altura_livre,
    voltas,
    voltas_barril,
    voltas_inativas_i,
    voltas_inativas_f,
    manta,
    spring_rate,
    G,
    delta_altura,
    delta_barril,
    delta_boca
):
    if (molas_comprimento*molas_largura)/(comprimento*largura)>=200:
        solda = 'Simples 7 mm'
        comp_solda = 7
    else:
        solda = 'Dupla 25 mm'
        comp_solda = 25
    passo = int(11*(D_barril+comp_solda)/25.4)
    results_output = pd.DataFrame(
        {
            ' ':[
                'Dimensões (m)',
                'Configuração',
                'Com manta',
                'Altura ensacada (mm)',
                'Altura livre (mm)',
                'Diâmetro do arame (mm)',
                'Diâmetro do barril (mm)',
                'Diâmetro da boca (mm)',
                'Voltas',
                'Voltas com diâmetro constante no barril',
                'Voltas inativas',
                'Voltas inativas no início',
                'Voltas inativas no fim',
                'Solda',
                'Passo (pol)',
                'Tensão de cisalhamento média (MPa)',
                'Tensão de cisalhamento alternada',
                'Spring Rate (N/pol)',
                'Firmeza (kgf)',
                'Comprimento de arame por mola (mm)',
                'Comprimento de arame no molejo (m)',
                'Massa por mola (g)',
                'Massa de arame no molejo (kg)'
            ],
            'Mola atual':np.nan,
            'Mola otimizada':np.nan,
            'Variação':np.nan
        }
    )
    results_output.set_index(' ', drop=False, inplace=True)
    flag_reducao=True
    if None in [altura, altura_livre, D_boca, voltas, voltas_barril]:
        x0 = [40, 0.8, 5, 0.7]
        pct_red_active = False
        flag_reducao = False
    else:
        x0 = [
            altura_livre-altura,
            D_boca/D_barril,
            voltas,
            voltas_barril
        ]

        comp = equations.comprimento(
            D_barril-d_arame,
            D_boca-d_arame,
            voltas_barril,
            voltas-voltas_inativas_i-voltas_inativas_f,
            voltas
        )
        massa = equations.massa_mola(
            d_arame,
            D_barril-d_arame,
            D_boca-d_arame,
            voltas_barril,
            voltas-voltas_inativas_i-voltas_inativas_f,
            voltas
        )
        sr = equations.spring_rate(
            d_arame,
            D_barril+delta_barril-d_arame,
            D_boca+delta_boca-d_arame,
            voltas_barril,
            voltas-voltas_inativas_i-voltas_inativas_f,
            G
        )
        sm, sa = equations.tensoes(
            d_arame,
            D_barril+delta_barril-d_arame,
            altura_livre+delta_altura,
            altura,
            sr,
            molas_comprimento/comprimento
        )
        ild = equations.ild(
            altura_livre+delta_altura,
            altura,
            D_boca+delta_boca-d_arame,
            sr,
            largura,
            comprimento,
            molas_largura,
            molas_comprimento,
            manta
        )

        comp_total = (comp*molas_comprimento*molas_largura)/1000
        massa_total = (massa*molas_comprimento*molas_largura)/1000

        results_output['Mola atual'] = [
            f'{largura:.2f} x {comprimento:.2f}',
            f'{molas_largura:.0f} x {molas_comprimento:.0f}',
            f'{"Sim" if manta else "Não"}',
            f'{altura:.0f}',
            f'{altura_livre:.0f}',
            f'{d_arame:.2f}',
            f'{D_barril:.0f}',
            f'{D_boca:.0f}',
            f'{voltas:.2f}',
            f'{voltas_barril:.2f}',
            f'{voltas_inativas_i+voltas_inativas_f:.2f}',
            f'{voltas_inativas_i:.2f}',
            f'{voltas_inativas_f:.2f}',
            f'{solda}',
            f'{passo:.0f}',
            f'{sm:.0f}',
            f'{sa:.0f}',
            f'{sr:.2f}',
            f'{ild:.2f}',
            f'{comp:.0f}',
            f'{comp_total:.2f}',
            f'{massa:.1f}',
            f'{massa_total:.1f}',
        ]
    bounds = Bounds(
        [
            min_pre_compressao,
            min_boca_barril,
            min_voltas,
            min_voltas_barril
        ],
        [
            max_pre_compressao,
            max_boca_barril,
            max_voltas,
            max_voltas_barril
        ]
    )
    constraints = [
        NonlinearConstraint(
            optimization.ild,
            firmeza_esperada*(1-tolerance/100), 
            firmeza_esperada*(1+tolerance/100)
        ),
        NonlinearConstraint(
            optimization.sm,
            min_sm if min_sm!=None else -np.inf,
            max_sm if max_sm!=None else np.inf
        ),
        NonlinearConstraint(
            optimization.sa,
            min_sa if min_sa!=None else -np.inf,
            max_sa if max_sa!=None else np.inf
        ),
    ]
    if pct_red_active:
        constraints.append(
            NonlinearConstraint(
                optimization.pct_reduction,
                min_pct_red if min_pct_red!=None else -np.inf,
                max_pct_red if max_pct_red!=None else np.inf
            )
        )
    if d_boca_active:
        constraints.append(
            NonlinearConstraint(
                optimization.boca,
                min_d_boca if min_d_boca!=None else -np.inf,
                max_d_boca if max_d_boca!=None else np.inf
            )
        )

    fig_molejo = visualize_molejo(
        largura,
        comprimento,
        altura,
        molas_largura,
        molas_comprimento,
        D_barril
    )

    fig_mola_atual = visualize_mola(
        d_arame,
        D_barril,
        D_boca,
        altura_livre,
        altura,
        voltas,
        voltas_barril,
        voltas_inativas_i,
        voltas_inativas_f
    )

    x, success = optimization.optimize(
        x0,
        bounds,
        constraints,
        altura,
        d_arame,
        D_barril,
        largura,
        comprimento,
        molas_largura,
        molas_comprimento,
        manta,
        G,
        voltas_inativas_i+voltas_inativas_f,
        delta_barril,
        delta_boca,
        delta_altura
    )


    Dh = x[0]
    D_boca_barril = x[1]
    voltas_otim = x[2]
    voltas_barril_otim = x[3]

    D_boca_otim = D_barril*D_boca_barril
    altura_livre_otim = altura+Dh

    comp_otim = equations.comprimento(
        D_barril-d_arame,
        D_boca_otim-d_arame,
        voltas_barril_otim,
        voltas_otim-voltas_inativas_i-voltas_inativas_f,
        voltas_otim
    )
    massa_otim = equations.massa_mola(
        d_arame,
        D_barril-d_arame,
        D_boca_otim-d_arame,
        voltas_barril_otim,
        voltas_otim-voltas_inativas_i-voltas_inativas_f,
        voltas_otim
    )
    sr_otim = equations.spring_rate(
        d_arame,
        D_barril+delta_barril-d_arame,
        D_boca_otim+delta_boca-d_arame,
        voltas_barril_otim,
        voltas_otim-voltas_inativas_i-voltas_inativas_f,
        G
    )
    sm_otim, sa_otim = equations.tensoes(
        d_arame,
        D_barril+delta_barril-d_arame,
        altura_livre_otim+delta_altura,
        altura,
        sr_otim,
        molas_comprimento/comprimento
    )
    ild_otim = equations.ild(
        altura_livre_otim+delta_altura,
        altura,
        D_boca_otim+delta_boca-d_arame,
        sr_otim,
        largura,
        comprimento,
        molas_largura,
        molas_comprimento,
        manta
    )

    fig_mola_otim = visualize_mola(
        d_arame,
        D_barril,
        D_boca_otim,
        altura_livre_otim,
        altura,
        voltas_otim,
        voltas_barril_otim,
        voltas_inativas_i,
        voltas_inativas_f
    )

    comp_total_otim = (comp_otim*molas_comprimento*molas_largura)/1000
    massa_total_otim = (massa_otim*molas_comprimento*molas_largura)/1000

    results_output['Mola otimizada'] = [
        f'{largura:.2f} x {comprimento:.2f}',
        f'{molas_largura:.0f} x {molas_comprimento:.0f}',
        f'{"Sim" if manta else "Não"}',
        f'{altura:.0f}',
        f'{altura_livre_otim:.0f}',
        f'{d_arame:.2f}',
        f'{D_barril:.0f}',
        f'{D_boca_otim:.0f}',
        f'{voltas_otim:.2f}',
        f'{voltas_barril_otim:.2f}',
        f'{voltas_inativas_i+voltas_inativas_f:.2f}',
        f'{voltas_inativas_i:.2f}',
        f'{voltas_inativas_f:.2f}',
        f'{solda}',
        f'{passo:.0f}',
        f'{sm_otim:.0f}',
        f'{sa_otim:.0f}',
        f'{sr_otim:.2f}',
        f'{ild_otim:.2f}',
        f'{comp_otim:.0f}',
        f'{comp_total_otim:.2f}',
        f'{massa_otim:.1f}',
        f'{massa_total_otim:.1f}',
    ]

    if flag_reducao:
        results_output['Variação'] = [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            f'{(altura_livre_otim-altura_livre):.0f} ({(altura_livre_otim-altura_livre)*100/altura_livre:.0f} %)',
            np.nan,
            np.nan,
            f'{(D_boca_otim-D_boca):.0f} ({(D_boca_otim-D_boca)*100/D_boca:.0f} %)',
            f'{(voltas_otim-voltas):.2f} ({(voltas_otim-voltas)*100/voltas:.0f} %)',
            f'{(voltas_barril_otim-voltas_barril):.2f} ({(voltas_barril_otim-voltas_barril)*100/voltas_barril:.0f} %)',
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            f'{sm_otim-sm:.0f} ({(sm_otim-sm)*100/sm:.0f} %)',
            f'{(sa_otim-sa):.0f} ({(sa_otim-sa)*100/sa:.0f} %)',
            f'{(sr_otim-sr):.2f} ({(sr_otim-sr)*100/sr:.0f} %)',
            f'{(ild_otim-ild):.2f} ({(ild_otim-ild)*100/ild:.0f} %)',
            f'{(comp_otim-comp):.0f} ({(comp_otim-comp)*100/comp:.0f} %)',
            f'{(comp_total_otim-comp_total):.2f} ({(comp_total_otim-comp_total)*100/comp_total:.0f} %)',
            f'{(massa_otim-massa):.1f} ({(massa_otim-massa)*100/massa:.0f} %)',
            f'{(massa_total_otim-massa_total):.1f} ({(massa_total_otim-massa_total)*100/massa_total:.0f} %)',
        ]
    else:
        massa_total = np.nan

    return fig_molejo, fig_mola_atual, fig_mola_otim, results_output, massa_total, massa_total_otim


def calcula_custo_anual(custo_kg, massa_atual, massa_otim, prod):
    custo_atual = custo_kg*massa_atual if massa_atual!=None else np.nan
    custo_otim = custo_kg*massa_otim
    custo_anual_atual = 12*prod*custo_atual
    custo_anual_otim = 12*prod*custo_otim
    dif = custo_anual_atual - custo_anual_otim
    return pd.DataFrame({'':['Mola atual','Mola otimizada','Redução de custo estimada'],'Unitário':[f'R$ {custo_atual:,.2f}', f'R$ {custo_otim:,.2f}', f'R$ {custo_atual-custo_otim:,.2f}'],'Anual':[f'R$ {custo_anual_atual:,.2f}', f'R$ {custo_anual_otim:,.2f}', f'R$ {dif:,.2f}']})


# def export_drawing(df):

#     df.set_index(' ', inplace=True)

#     df_export = df[['Mola otimizada']].loc[[
#         'Altura livre (mm)',
#         'Altura ensacada (mm)',
#         'Diâmetro do arame (mm)',
#         'Diâmetro do barril (mm)',
#         'Diâmetro da boca (mm)',
#         'Voltas',
#         'Voltas com diâmetro constante no barril',
#         'Voltas inativas no início',
#         'Voltas inativas no fim',
#         'Spring Rate (N/pol)',
#         'Solda',
#         'Passo (pol)',
#         'Firmeza (kgf)'
#     ]]

#     df_export.to_clipboard(decimal=',', index=False, header=False)

#     path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

#     os.system(f"start EXCEL.EXE {path}\desenho.xlsm")
