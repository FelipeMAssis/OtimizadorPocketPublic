# Import necessary modules and functions
import numpy as np
import pandas as pd
import gradio as gr
from utils import demo_actions
import utils.constants as consts


# Create the main Gradio interface
with gr.Blocks(theme='soft') as demo:
    gr.Markdown("# Otimizador de Molas Pocket")

    # Step 1: Molejo
    # Create an accordion for Step 1
    step1_accordion = gr.Accordion(">>> Passo 1: Molejo")
    with step1_accordion:
        gr.Markdown('---')
        # Create the input components for Step 1
        with gr.Row():
            manta_input = gr.Checkbox(label='Possui Manta', value=consts.def_molejo['manta'])
        with gr.Row():
            with gr.Column():
                largura_input = gr.Number(label='Largura (m)', value=consts.def_molejo['largura'])
                comprimento_input = gr.Number(label='Comprimento (m)', value=consts.def_molejo['comprimento'])
            with gr.Column():
                altura_input = gr.Number(label='Altura (mm)', value=consts.def_molejo['altura'])
                molas_largura_input = gr.Number(label='Molas na largura', value=consts.def_molejo['molas_largura'])
            with gr.Column():
                molas_comprimento_input = gr.Number(label='Molas no comprimento', value=consts.def_molejo['molas_comprimento'])
                D_barril_input = gr.Number(label='Diâmetro do barril (mm)', value=consts.def_molejo['D_barril'])
        # with gr.Row():
        #     modo_molejo = gr.Checkbox(label='Modo avançado', value=False)
        with gr.Row():
            visualize_molejo_button = gr.Button("Visualizar Molejo")
        with gr.Row():
            molejo_output = gr.Plot()
        with gr.Row():
            # Create the navigation buttons for Step 1
            step2_advance_button = gr.Button('Próximo', variant='primary')

    # Step 2: Mola Atual (Opcional)
    # Create an accordion for Step 2
    step2_accordion = gr.Accordion(">>> Passo 2: Mola Atual (Opcional)", open=False)
    with step2_accordion:
        gr.Markdown('---')
        # Create the input components for Step 2
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    with gr.Column():
                        d_arame_input = gr.Number(label='Diâmetro do arame (mm)', value=consts.def_mola['d_arame'])
                        D_barril_follow = gr.Number(label='Diâmetro do barril (mm)', value=consts.def_mola['D_barril'])
                        D_barril_input.change(lambda x: x, inputs=D_barril_input, outputs=D_barril_follow)
                        D_boca_input = gr.Number(label='Diâmetro da boca (mm)', value=consts.def_mola['D_boca'])
                        altura_livre_input = gr.Number(label='Altura livre (mm)', value=consts.def_mola['altura_livre'])
                        altura_follow = gr.Number(label='Altura ensacada (mm)', value=consts.def_mola['altura'])
                    with gr.Column():
                        voltas_input = gr.Number(label='Voltas', value=consts.def_mola['voltas'])
                        voltas_barril_input = gr.Number(label='Voltas com diâmetro constante no barril', value=consts.def_mola['voltas_barril'])
                        voltas_i_input = gr.Number(label='Voltas inativas no início', value=consts.def_mola['voltas_i'])
                        voltas_f_input = gr.Number(label='Voltas inativas no fim', value=consts.def_mola['voltas_f'])
                        spring_rate_input = gr.Number(label="Spring Rate medido (N/pol)", value=np.nan)
                # with gr.Row():
                #     modo_mola = gr.Checkbox(label='Modo avançado', value=False)
            with gr.Column(scale=1):
                visualize_mola_button = gr.Button("Visualizar Mola")
                # Create the output components for Step 2
                mola_output = gr.Plot()
        with gr.Row():
            # Create the navigation buttons for Step 2
            step1_return_button = gr.Button('Anterior')
            step3_advance_button = gr.Button('Próximo', variant='primary')

    # Step 3: Firmeza
    # Create an accordion for Step 3
    step3_accordion = gr.Accordion(">>> Passo 3: Firmeza", open=False)
    with step3_accordion:
        gr.Markdown('---')
        # Create the input components for Step 3
        with gr.Row():
            with gr.Column():
                modulo_G_input = gr.Number(label='Módulo de elasticidade de cisalhamento (GPa)', value=consts.def_parameters['modulo_G'])
            with gr.Column():
                Delta_altura_input = gr.Number(label='Delta altura após 10 batidas', value=consts.def_parameters['Delta_altura'])
            with gr.Column():
                Delta_barril_input = gr.Number(label='Delta barril após 10 batidas', value=consts.def_parameters['Delta_barril'])
            with gr.Column():
                Delta_boca_input = gr.Number(label='Delta boca após 10 batidas', value=consts.def_parameters['Delta_boca'])
        with gr.Row():
            calcular_firmeza_button = gr.Button("Calcular Firmeza Atual")
        with gr.Row():
            # Create the output components for Step 3
            firmeza_output = gr.DataFrame(
                pd.DataFrame(
                    {
                        '':['Informado pelo usuário', 'Calculado para a mola atual'],
                        'Spring Rate (N/pol)':[np.nan, np.nan],
                        'Firmeza (kgf)':[np.nan, np.nan]
                    }
                )
            )
            firmeza_esperada_input = gr.Number(label='Firmeza esperada', precision=2)
            tolerance_input = gr.Number(label='Tolerância (%)', value=0.1)
        with gr.Row():
            # Create the navigation buttons for Step 3
            step2_return_button = gr.Button('Anterior')
            step4_advance_button = gr.Button('Opções do Otimizador')
            optimize_button = gr.Button('Otimizar', visible=False, variant='primary')

    # Step 4: Opções do Otimizador
    # Create an accordion for Step 4
    step4_accordion = gr.Accordion(">>> Passo 4: Opções do Otimizador", open=False)
    with step4_accordion:
        gr.Markdown('---')
        # Create the input components for Step 3
        with gr.Row():
            with gr.Column():
                gr.Markdown('Limites:')
                with gr.Row():
                    gr.Markdown('Pré-compressão (Altura livre - Altura ensacada) (mm)')
                with gr.Row():
                    with gr.Column():
                        min_pre_compressao_input = gr.Number(label='Min', value=consts.def_limites['pre_compressao'][0])
                    with gr.Column():
                        max_pre_compressao_input = gr.Number(label='Max', value=consts.def_limites['pre_compressao'][1])
                with gr.Row():
                    gr.Markdown('Razão boca/barril')
                with gr.Row():
                    with gr.Column():
                        min_boca_barril_input = gr.Number(label='Min', value=consts.def_limites['razao_boca_barril'][0])
                    with gr.Column():
                        max_boca_barril_input = gr.Number(label='Max', value=consts.def_limites['razao_boca_barril'][1])
                with gr.Row():
                    gr.Markdown('Voltas')
                with gr.Row():
                    with gr.Column():
                        min_voltas_input = gr.Number(label='Min', value=consts.def_limites['voltas'][0])
                    with gr.Column():
                        max_voltas_input = gr.Number(label='Max', value=consts.def_limites['voltas'][1])
                with gr.Row():
                    gr.Markdown('Voltas com diâmetro constante no barril')
                with gr.Row():
                    with gr.Column():
                        min_voltas_barril_input = gr.Number(label='Min', value=consts.def_limites['voltas_barril'][0])
                    with gr.Column():
                        max_voltas_barril_input = gr.Number(label='Max', value=consts.def_limites['voltas_barril'][1])
            with gr.Column():
                gr.Markdown('Restrições:')
                with gr.Row():
                    with gr.Column():
                        gr.Markdown('Tensão de cisalhamento média (MPa)')
                    with gr.Column():
                        sm_active = gr.Checkbox(label='Ativo', value=consts.def_restricoes['tensao_cisalhamento_med'][0], visible=False)
                with gr.Row():
                    with gr.Column():
                        min_sm_input = gr.Number(label='Min', value=consts.def_restricoes['tensao_cisalhamento_med'][1])
                    with gr.Column():
                        max_sm_input = gr.Number(label='Max', value=consts.def_restricoes['tensao_cisalhamento_med'][2])
                with gr.Row():
                    with gr.Column():
                        gr.Markdown('Tensão de cisalhamento alternada (MPa)')
                    with gr.Column():
                        sa_active = gr.Checkbox(label='Ativo', value=consts.def_restricoes['tensao_cisalhamento_alt'][0], visible=False)
                with gr.Row():
                    with gr.Column():
                        min_sa_input = gr.Number(label='Min', value=consts.def_restricoes['tensao_cisalhamento_alt'][1])
                    with gr.Column():
                        max_sa_input = gr.Number(label='Max', value=consts.def_restricoes['tensao_cisalhamento_alt'][2])
                with gr.Row():
                    with gr.Column():
                        gr.Markdown('Percentual de redução de arame (%)')
                    with gr.Column():
                        pct_red_active = gr.Checkbox(label='Ativo', value=consts.def_restricoes['pct_reducao_arame'][0])
                with gr.Row():
                    with gr.Column():
                        min_pct_red_input = gr.Number(label='Min', value=consts.def_restricoes['pct_reducao_arame'][1])
                    with gr.Column():
                        max_pct_red_input = gr.Number(label='Max', value=consts.def_restricoes['pct_reducao_arame'][2])   
                with gr.Row():
                    with gr.Column():
                        gr.Markdown('Diâmetro da boca (mm)')
                    with gr.Column():
                        d_boca_active = gr.Checkbox(label='Ativo', value=consts.def_restricoes['D_boca'][0])
                with gr.Row():
                    with gr.Column():
                        min_d_boca_input = gr.Number(label='Min', value=consts.def_restricoes['D_boca'][1])
                    with gr.Column():
                        max_d_boca_input = gr.Number(label='Max', value=consts.def_restricoes['D_boca'][2])
        with gr.Row():
            # Create the navigation buttons for Step 4
            step3_return_button = gr.Button('Anterior')
            optimize_button_copy = gr.Button('Otimizar', visible=False, variant='primary')

    # Step 5: Resultados
    # Create an accordion for Step 5
    step5_accordion = gr.Accordion(">>> Passo 5: Resultados", open=False, visible=False)
    with step5_accordion:
        gr.Markdown('---')
        # Create output elements for Step 5
        with gr.Row():
            results_output = gr.Dataframe(interactive=False)
        with gr.Row():
            with gr.Column():
                massa_unitaria_atual_output = gr.Number(label='Massa de arame no molejo atual (kg)', precision=1)
                massa_unitaria_otim_output = gr.Number(label='Massa de arame no molejo otimizado (kg)', precision=1)
                # Create input elements for Step 5
                custo_kg_input = gr.Number(label='Custo arame (R$/kg)', value=consts.custo_kg, precision=2)
                prod_mensal_input = gr.Number(label='Produção mensal (molejos)')
            with gr.Column():
                custo_anual_button = gr.Button('Calcular custos')
                custo_output = gr.Dataframe(value = pd.DataFrame({'':['Mola atual','Mola otimizada','Redução de custo estimada'],'Valor':np.nan}))
        with gr.Row():
            # Create figures for Step 5
            with gr.Column(scale=3):
                fig_molejo = gr.Plot(label='Molejo')
            with gr.Column(scale=1):
                fig_mola_atual_output = gr.Plot(label='Mola Atual')
            with gr.Column(scale=1):
                fig_mola_otim_output = gr.Plot(label='Mola Otimizada')
        with gr.Row():
            export_button = gr.Button('Exportar desenho', variant='primary')
        with gr.Row():
            # Create the navigation buttons for Step 5
            step4_return_button = gr.Button('Voltar para opções')
            restart_button = gr.Button('Reiniciar Simulação')

    # Create lists of input elements

    molejo_input = [
        largura_input,
        comprimento_input,
        altura_input,
        molas_largura_input,
        molas_comprimento_input,
        D_barril_input
    ]

    mola_input = [
        d_arame_input,
        D_barril_input,
        D_boca_input,
        altura_livre_input,
        altura_input,
        voltas_input,
        voltas_barril_input,
        voltas_i_input,
        voltas_f_input
    ]

    firmeza_input = [
        largura_input,
        comprimento_input,
        altura_input,
        molas_largura_input,
        molas_comprimento_input,
        d_arame_input,
        D_barril_input,
        D_boca_input,
        altura_livre_input,
        voltas_input,
        voltas_barril_input,
        voltas_i_input,
        voltas_f_input,
        manta_input,
        spring_rate_input,
        modulo_G_input,
        Delta_altura_input,
        Delta_barril_input,
        Delta_boca_input
    ]

    bounds_input = [
        min_pre_compressao_input,
        max_pre_compressao_input,
        min_boca_barril_input,
        max_boca_barril_input,
        min_voltas_input,
        max_voltas_input,
        min_voltas_barril_input,
        max_voltas_barril_input
    ]

    constraints_input = [
        min_sm_input,
        max_sm_input,
        sm_active,
        min_sa_input,
        max_sa_input,
        sa_active,
        min_pct_red_input,
        max_pct_red_input,
        pct_red_active,
        min_d_boca_input,
        max_d_boca_input,
        d_boca_active
    ]

    optimize_inputs = [
        firmeza_esperada_input,
        tolerance_input,
        *bounds_input,
        *constraints_input,
        *firmeza_input,
    ]

    # Create navigation functions
    def select_accordion_1():
        s1 = step1_accordion.update(open=True)
        s2 = step2_accordion.update(open=False)
        s3 = step3_accordion.update(open=False)
        s4 = step4_accordion.update(open=False)
        s5 = step5_accordion.update(open=False)
        return s1, s2, s3, s4, s5

    def select_accordion_2():
        s1 = step1_accordion.update(open=False)
        s2 = step2_accordion.update(open=True)
        s3 = step3_accordion.update(open=False)
        s4 = step4_accordion.update(open=False)
        s5 = step5_accordion.update(open=False)
        return s1, s2, s3, s4, s5

    def select_accordion_3():
        s1 = step1_accordion.update(open=False)
        s2 = step2_accordion.update(open=False)
        s3 = step3_accordion.update(open=True)
        s4 = step4_accordion.update(open=False)
        s5 = step5_accordion.update(open=False)
        return s1, s2, s3, s4, s5
    
    def select_accordion_4():
        s1 = step1_accordion.update(open=False)
        s2 = step2_accordion.update(open=False)
        s3 = step3_accordion.update(open=False)
        s4 = step4_accordion.update(open=True)
        s5 = step5_accordion.update(open=False)
        return s1, s2, s3, s4, s5
    
    def select_accordion_5():
        s1 = step1_accordion.update(open=False)
        s2 = step2_accordion.update(open=False)
        s3 = step3_accordion.update(open=False)
        s4 = step4_accordion.update(open=False)
        s5 = step5_accordion.update(open=True, visible=True)
        return s1, s2, s3, s4, s5

    def optimize_change_page(*inputs):
        fig_molejo, fig_mola_atual_output, fig_mola_otim_output, results_output, massa_unitaria_atual, massa_unitaria_otim = demo_actions.optimize(*inputs)
        s1, s2, s3, s4, s5 = select_accordion_5()
        custo_output = pd.DataFrame({'':['Mola atual','Mola otimizada','Redução de custo estimada'],'Unitário':np.nan,'Anual':np.nan})
        return fig_molejo, fig_mola_atual_output, fig_mola_otim_output, results_output, s1, s2, s3, s4, s5, massa_unitaria_atual, massa_unitaria_otim, custo_output

    def unlock_optimize(firmeza_esperada):
        if firmeza_esperada>0 and firmeza_esperada!=None:
            opt_button = optimize_button.update(visible=True)
            opt_button_copy = optimize_button_copy.update(visible=True)
        else:
            opt_button = optimize_button.update(visible=False)
            opt_button_copy = optimize_button_copy.update(visible=False)
        return opt_button, opt_button_copy

    # Apply actions to elements
    visualize_molejo_button.click(demo_actions.visualize_molejo, inputs=molejo_input, outputs=molejo_output)

    D_barril_input.change(lambda x: x, inputs=D_barril_input, outputs=D_barril_follow)

    altura_input.change(lambda x: x, inputs=altura_input, outputs=altura_follow)

    step2_advance_button.click(select_accordion_2, outputs=[step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion])
    
    visualize_mola_button.click(demo_actions.visualize_mola, inputs=mola_input, outputs=mola_output)
    
    step1_return_button.click(select_accordion_1, outputs=[step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion])
    
    step3_advance_button.click(select_accordion_3, outputs=[step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion])
    
    calcular_firmeza_button.click(demo_actions.calcula_firmeza, inputs=firmeza_input, outputs=[firmeza_output, firmeza_esperada_input])
    
    step2_return_button.click(select_accordion_2, outputs=[step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion])
    
    step4_advance_button.click(select_accordion_4, outputs=[step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion])
    
    optimize_button.click(optimize_change_page, inputs=optimize_inputs, outputs=[fig_molejo, fig_mola_atual_output, fig_mola_otim_output, results_output, step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion, massa_unitaria_atual_output, massa_unitaria_otim_output, custo_output]) 
    
    step3_return_button.click(select_accordion_3, outputs=[step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion])
    
    optimize_button_copy.click(optimize_change_page, inputs=optimize_inputs, outputs=[fig_molejo, fig_mola_atual_output, fig_mola_otim_output, results_output, step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion, massa_unitaria_atual_output, massa_unitaria_otim_output, custo_output])
    
    custo_anual_button.click(demo_actions.calcula_custo_anual, inputs=[custo_kg_input, massa_unitaria_atual_output, massa_unitaria_otim_output, prod_mensal_input], outputs=custo_output)
    
    step4_return_button.click(select_accordion_4, outputs=[step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion]) 
    
    restart_button.click(select_accordion_1, outputs=[step1_accordion, step2_accordion, step3_accordion, step4_accordion, step5_accordion])
    
    firmeza_esperada_input.change(unlock_optimize, inputs=firmeza_esperada_input, outputs=[optimize_button, optimize_button_copy])
    
    # export_button.click(demo_actions.export_drawing, inputs=results_output)

# Launch the application
demo.launch(inbrowser=True)#, auth=("admin", "12345678"))
