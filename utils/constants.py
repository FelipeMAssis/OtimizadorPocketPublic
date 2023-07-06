import numpy as np

def_molejo = {
    'manta':True,
    'largura':1.23,
    'comprimento':1.83,
    'altura':165,
    'molas_largura':22,
    'molas_comprimento':21,
    'D_barril':68
}

def_mola = {
    'd_arame':2,
    'D_barril':def_molejo['D_barril'],
    'D_boca':np.nan,
    'altura_livre':np.nan,
    'altura':def_molejo['altura'],
    'voltas':np.nan,
    'voltas_barril':np.nan,
    'voltas_i':0.1,
    'voltas_f':0.2
}

def_parameters = {
    'modulo_G':80.8,
    'Delta_altura':0,
    'Delta_barril':0,
    'Delta_boca':0
}

def_firmeza = {
    'ild_esperado':0,
    'tolerancia':0.1
}

def_limites = {
    'pre_compressao':(30, 100),
    'razao_boca_barril':(0.5, 1),
    'voltas':(2,10),
    'voltas_barril':(0.3, 1.5)
}

def_restricoes = {
     'tensao_cisalhamento_med':(True, np.nan, 400),
     'tensao_cisalhamento_alt':(True, np.nan, 60),
     'pct_reducao_arame':(True, 0, 10),
     'D_boca':(False, 50, np.nan)
}

custo_kg = 6
