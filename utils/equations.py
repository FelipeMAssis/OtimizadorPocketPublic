import numpy as np

def points_molejo(
    largura,
    comprimento,
    molas_largura,
    molas_comprimento,
    D_barril
):
    x = np.linspace(-largura/2+D_barril/2000, largura/2-D_barril/2000, int(molas_largura))
    y = np.linspace(-comprimento/2+D_barril/2000, comprimento/2-D_barril/2000, int(molas_comprimento))
    xv, yv = np.meshgrid(x,y)
    return xv, yv

def interp_barril_boca(valor_barril, valor_boca, voltas_ativas, voltas_barril, volta):
    if volta>=-voltas_barril/2 and volta<=voltas_barril/2:
        return valor_barril
    return valor_barril-(np.abs(volta)-voltas_barril/2)*(valor_barril-valor_boca)/(voltas_ativas/2-voltas_barril/2)

def define_geom(
    D_barril,
    D_boca,
    voltas_barril,
    voltas_ativas,
    inc=0.01
):
    t = np.linspace(-1,1,int(2/inc)+1)
    volta = t*voltas_ativas/2
    D = np.array(
        [interp_barril_boca(
            D_barril,
            D_boca,
            voltas_ativas,
            voltas_barril,
            v,
            ) for v in volta]
        )
    return D, inc

def points_mola(
    D_barril,
    D_boca,
    voltas_barril,
    voltas_i,
    voltas_f,
    voltas,
    altura
):
    
    D, inc = define_geom(
        D_barril,
        D_boca,
        voltas_barril,
        voltas-voltas_i-voltas_f
    )
    t = np.linspace(-1,1,int(2/inc)+1)
    v = (voltas-voltas_i-voltas_f)*t/2
    dv = [0]+[inc]*(len(t)-1)
    a, b, c = 3*altura/4, 0, -3*altura/4
    p = a*np.power(t,2)+b*t+c
    theta = 2*np.pi*v
    v_i = np.linspace(-(voltas-voltas_f-voltas_i)/2-voltas_i, -(voltas-voltas_f-voltas_i)/2,50)
    v_f = np.linspace((voltas-voltas_f-voltas_i)/2, (voltas-voltas_f-voltas_i)/2+voltas_f,50)

    x_i = (D_boca/2)*np.sin(2*np.pi*v_i)
    x_f = (D_boca/2)*np.sin(2*np.pi*v_f)
    x = np.concatenate([x_i,D/2*np.sin(theta),x_f])
    z = np.concatenate([50*[0],-np.cumsum(p*dv),50*[altura]])
    return x, z

def spring_rate(
    d,
    D_barril,
    D_boca,
    voltas_barril,
    voltas_ativas,
    G
):
    return 6*np.rand(1)[0]

def ild(
    altura,
    altura_ens,
    boca,
    k,
    largura,
    comprimento,
    molas_largura,
    molas_comprimento,
    manta,
    corr = True
):
    return 40+(50)*np.rand(1)[0]

def tensoes(
    d,
    D_barril,
    altura,
    altura_ens,
    k,
    molas_m
):
    return 200+(200)*np.rand(1)[0], 30+(20)*np.rand(1)[0]


def comprimento(
    D_barril,
    D_boca,
    voltas_barril,
    voltas_ativas,
    voltas
):
    return 500+(600)*np.rand(1)[0]

def massa_mola(
    d_arame,
    D_barril,
    D_boca,
    voltas_barril,
    voltas_ativas,
    voltas,
    n=1
):
    l = comprimento(
        D_barril,
        D_boca,
        voltas_barril,
        voltas_ativas,
        voltas
    )
    return l*0.01


def custo_arame(
    d_arame,
    D_barril,
    D_boca,
    voltas_barril,
    voltas_ativas,
    voltas,
    custo_kg=4+np.rand(1)[0],
    scrap=1+np.rand(1)[0],
    n=1
):
    massa = massa_mola(
        d_arame,
        D_barril,
        D_boca,
        voltas_barril,
        voltas_ativas,
        voltas,
    )
    return n*custo_kg*massa*scrap/1000