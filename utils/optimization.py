from scipy.optimize import minimize

from . import equations


def J(x): # Função a ser minimizada

    global D_barril_global, d_arame_global, voltas_inativas_global

    D_boca_barril = x[1]
    voltas = x[2]
    voltas_barril = x[3]
    return equations.comprimento(
        D_barril_global-d_arame_global,
        D_boca_barril*D_barril_global-d_arame_global,
        voltas_barril,
        voltas-voltas_inativas_global,
        voltas
    )


def sm(x):

    global D_barril_global, d_arame_global, altura_global, G_global
    global molas_comprimento_global, comprimento_global, voltas_inativas_global
    global Delta_D_barril_global, Delta_D_boca_global, Delta_altura_global

    Dh = x[0]
    D_boca_barril = x[1]
    voltas = x[2]
    voltas_barril = x[3]
    return equations.tensoes(
        d_arame_global,
        D_barril_global-d_arame_global+Delta_D_barril_global,
        altura_global+Dh+Delta_altura_global,
        altura_global,
        equations.spring_rate(
            d_arame_global,
            D_barril_global-d_arame_global+Delta_D_barril_global,
            D_boca_barril*D_barril_global-d_arame_global+Delta_D_boca_global,
            voltas_barril,
            voltas-voltas_inativas_global,
            G_global
        ),
        molas_comprimento_global/comprimento_global
    )[0]

def sa(x):

    global D_barril_global, d_arame_global, altura_global, G_global
    global molas_comprimento_global, comprimento_global, voltas_inativas_global
    global Delta_D_barril_global, Delta_D_boca_global, Delta_altura_global

    Dh = x[0]
    D_boca_barril = x[1]
    voltas = x[2]
    voltas_barril = x[3]
    return equations.tensoes(
        d_arame_global,
        D_barril_global-d_arame_global+Delta_D_barril_global,
        altura_global+Dh+Delta_altura_global,
        altura_global,
        equations.spring_rate(
            d_arame_global,
            D_barril_global-d_arame_global+Delta_D_barril_global,
            D_boca_barril*D_barril_global-d_arame_global+Delta_D_boca_global,
            voltas_barril,
            voltas-voltas_inativas_global,
            G_global
        ),
        molas_comprimento_global/comprimento_global
    )[1]

def passo_med(x):
    global altura_global
    voltas = x[2]
    return altura_global/voltas

def pct_reduction(x):
    global x0_global
    return (J(x0_global)-J(x))*100/J(x0_global)

def boca(x):
    global D_barril_global
    return x[1]*D_barril_global


def ild(x):

    global altura_global, d_arame_global, D_barril_global, largura_global, comprimento_global
    global molas_largura_global, molas_comprimento_global, manta_global, G_global
    global voltas_inativas_global, Delta_D_barril_global, Delta_D_boca_global, Delta_altura_global

    Dh = x[0]
    D_boca_barril = x[1]
    voltas = x[2]
    voltas_barril = x[3]
    return equations.ild(
        altura_global+Dh+Delta_altura_global,
        altura_global,
        D_boca_barril*D_barril_global-d_arame_global,
        equations.spring_rate(
            d_arame_global,
            D_barril_global-d_arame_global+Delta_D_barril_global,
            D_boca_barril*D_barril_global-d_arame_global+Delta_D_boca_global,
            voltas_barril,
            voltas-voltas_inativas_global,
            G_global
        ),
        largura_global,
        comprimento_global,
        molas_largura_global,
        molas_comprimento_global,
        manta_global)

def optimize(
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
    voltas_inativas,
    delta_barril,
    delta_boca,
    delta_altura
):
    global altura_global, d_arame_global, D_barril_global, largura_global, comprimento_global
    global molas_largura_global, molas_comprimento_global, manta_global, G_global
    global voltas_inativas_global, Delta_D_barril_global, Delta_D_boca_global, Delta_altura_global
    global x0_global

    x0_global = x0
    altura_global = altura
    d_arame_global = d_arame
    D_barril_global = D_barril
    largura_global = largura
    comprimento_global = comprimento
    molas_largura_global = molas_largura
    molas_comprimento_global = molas_comprimento
    manta_global = manta
    G_global = G
    voltas_inativas_global = voltas_inativas
    Delta_D_barril_global = delta_barril
    Delta_D_boca_global = delta_boca
    Delta_altura_global = delta_altura

    results = minimize(J, x0, bounds=bounds, constraints=constraints)

    return results['x'], results['success']
