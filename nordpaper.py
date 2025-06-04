import streamlit as st
import pandas as pd


st.set_page_config(
    page_title = "NordPaper : indicateurs machine",
    # page_icon="🚲",
    layout="wide",
)

nb_callback = 0

def data_sheets():
    file_name = st.session_state.file_name
    sheet_names = pd.ExcelFile(file_name).sheet_names
    data_sheet_list = list()
    for sheet in sheet_names:
        sheet_as_list = sheet.split("_")
        if sheet_as_list[0] == 'data':
            data_sheet_list.append(sheet)
    st.session_state.data_sheet_list = data_sheet_list

def load_file(file_name = 'trg_simu.xlsx'):
    st.session_state.file_name = file_name
    st.write("Etat Machine")

    full_sheet_df = pd.read_excel(file_name)
    return full_sheet_df

def display_data(file_name = 'trg_simu.xlsx'):
    columns=['Annee', 'Mois', 'M2_trg', 'M2_prime','M4_trg', 'M4_prime','M6_trg', 'M6_prime',]
    base_data_2024 = pd.read_excel(file_name, sheet_name='data_2024')
    base_data_2024 = base_data_2024.set_axis(columns, axis=1)
    st.session_state.base_data = base_data_2024
    st.write("base data 2024")
    st.write(base_data_2024)
    
def get_all_calculated_data():
    if 'data_sheet_list' not in st.session_state:
        print("data_sheet_list not available")
    else:
        sheets_data = dict()
        for sheet in st.session_state.data_sheet_list:
            sheets_data[sheet] = get_calculated_data(sheet)
        return sheets_data
    
def get_all_edited_data():
    if 'data_sheet_list' not in st.session_state:
        print("data_sheet_list not available")
    else:
        sheets_data = dict()
        for sheet in st.session_state.data_sheet_list:
            sheets_data[sheet] = get_edited_data(sheet)
        return sheets_data
    
def get_all_aggregated_data():
    if 'data_sheet_list' not in st.session_state:
        print("data_sheet_list not available")
    else:
        sheets_data = dict()
        summary = list()
        for sheet in st.session_state.data_sheet_list:
            sheets_data[sheet], row_year = get_aggregated_data(sheet)
            summary.append(row_year)
            st.session_state.summary = summary
        return sheets_data
    
def get_calculated_data(sheet):
    file_name = st.session_state.file_name
    columns=['Annee', 'Mois', 'M2_trg', 'M2_prime','M4_trg', 'M4_prime','M6_trg', 'M6_prime',]
    base_data = pd.read_excel(file_name, sheet_name=sheet)
    base_data = base_data.set_axis(columns, axis=1)
    calculated_data = base_data.copy()
    bonus = table_bonus_by_trg(file_name)
    for row_index in range(len(calculated_data)):
        m2_trg_prime = 0
        m4_trg_prime = 0
        m6_trg_prime = 0
        m2_trg_effectif = calculated_data.iloc[row_index]['M2_trg']
        m4_trg_effectif = calculated_data.iloc[row_index]['M4_trg']
        m6_trg_effectif = calculated_data.iloc[row_index]['M6_trg']
        for bonus_row_index in range(len(bonus)):
            if m2_trg_effectif >= bonus.iloc[bonus_row_index]['M2_trg']:
                m2_trg_prime = bonus.iloc[bonus_row_index]['M2_prime']
            if m4_trg_effectif >= bonus.iloc[bonus_row_index]['M4_trg']:
                m4_trg_prime = bonus.iloc[bonus_row_index]['M4_prime']
            if m6_trg_effectif >= bonus.iloc[bonus_row_index]['M6_trg']:
                m6_trg_prime = bonus.iloc[bonus_row_index]['M6_prime']
        calculated_data.at[row_index, 'M2_prime'] = m2_trg_prime
        calculated_data.at[row_index, 'M4_prime'] = m4_trg_prime
        calculated_data.at[row_index, 'M6_prime'] = m6_trg_prime
    st.session_state.calculated_data = dict()
    st.session_state.calculated_data[sheet] = calculated_data
    return calculated_data
    
def get_edited_data(sheet):
    file_name = st.session_state.file_name
    bonus = st.session_state.dynamic_data
    columns=['Annee', 'Mois', 'M2_trg', 'M2_prime_proposee','M4_trg', 'M4_prime_proposee','M6_trg', 'M6_prime_proposee',]
    base_data = pd.read_excel(file_name, sheet_name=sheet)
    base_data = base_data.set_axis(columns, axis=1)
    edited_data = base_data.copy()
    for row_index in range(len(edited_data)):
        m2_trg_prime = 0
        m4_trg_prime = 0
        m6_trg_prime = 0
        m2_trg_effectif = edited_data.iloc[row_index]['M2_trg']
        m4_trg_effectif = edited_data.iloc[row_index]['M4_trg']
        m6_trg_effectif = edited_data.iloc[row_index]['M6_trg']
        for bonus_row_index in range(len(bonus)):
            if m2_trg_effectif >= bonus.iloc[bonus_row_index]['M2_trg']:
                m2_trg_prime = bonus.iloc[bonus_row_index]['M2_prime']
            if m4_trg_effectif >= bonus.iloc[bonus_row_index]['M4_trg']:
                m4_trg_prime = bonus.iloc[bonus_row_index]['M4_prime']
            if m6_trg_effectif >= bonus.iloc[bonus_row_index]['M6_trg']:
                m6_trg_prime = bonus.iloc[bonus_row_index]['M6_prime']
        edited_data.at[row_index, 'M2_prime_proposee'] = m2_trg_prime
        edited_data.at[row_index, 'M4_prime_proposee'] = m4_trg_prime
        edited_data.at[row_index, 'M6_prime_proposee'] = m6_trg_prime
    st.session_state.edited_data = dict()
    st.session_state.edited_data[sheet] = edited_data
    return edited_data
    
def table_bonus_by_trg(file_name = 'trg_simu.xlsx'):
    columns=['M2_trg', 'M2_prime','M4_trg', 'M4_prime','M6_trg', 'M6_prime',]
    bonus = pd.read_excel(file_name, sheet_name='calcul_prime')
    bonus = bonus.set_axis(columns, axis=1)
    return bonus

# def display_bonus_by_trg(bonus):
#     st.write("calcul des primes par machine et TRG")
#     st.write(bonus)
    
def get_result_aggregate():
    all_years_aggregate_df = get_all_aggregated_data()
    get_summary_frame = get_summary()
    st.write("aggregate : ")
    for sheet, aggregate in all_years_aggregate_df.items():
        st.write("Année "+sheet.split('_')[1]+" : ")
        st.dataframe(aggregate)
        #     aggregate.apply(
        #         'background-color : red',
        #         axis=1,
        #         subset=["M2_prime_evolution"],
        #     )
        # )
    
def display_editable_bonus():
    bonus = table_bonus_by_trg(st.session_state.file_name)
    st.write("editer des primes par machine et TRG")
    st.session_state.dynamic_data = st.data_editor(bonus, num_rows="dynamic")
    objectif()
    if st.button("charger donnees dans tableau"):
        get_result_aggregate()
        pass

def display_editated_data():
    get_edited_data()
    st.dataframe(st.session_state.edited_data)

def add_visualization_data(data_frame):
    print("dans add visualization data")
    m2_prime_proposee = data_frame['M2_prime_proposee'] - data_frame['M2_prime']
    data_frame.insert(5, 'M2_prime_evolution', m2_prime_proposee)
    m4_prime_proposee = data_frame['M4_prime_proposee'] - data_frame['M4_prime']
    data_frame.insert(9, 'M4_prime_evolution', m4_prime_proposee)
    m6_prime_proposee = data_frame['M6_prime_proposee'] - data_frame['M6_prime']
    data_frame.insert(13, 'M6_prime_evolution', m6_prime_proposee)
    evolution_toutes_machine = m2_prime_proposee + m4_prime_proposee + m6_prime_proposee
    data_frame.insert(14, 'prime_evolution_toutes_machine', evolution_toutes_machine)
    
    # st.dataframe(df.style.applymap(color_survived, subset=['Survived']))
    
    col_list= list(data_frame)
    
    columns_without_sum = ['Annee', 'Mois', 'M2_trg', 'M4_trg', 'M6_trg']
    print(f"col list {col_list}")
    data_frame.loc['total annee'] = data_frame.sum(numeric_only=True)
    
    columns_without_sum = ['Annee', 'Mois', 'M2_trg', 'M4_trg', 'M6_trg']
    data_frame.loc[data_frame.index[-1], columns_without_sum] = None
    return data_frame

    
def get_aggregated_data(sheet):
    if f'edited_data[{sheet}]' not in st.session_state:
        get_edited_data(sheet)
    if f'calculated_data[{sheet}]' not in st.session_state:
        get_calculated_data(sheet)
        
    edited_data = st.session_state.edited_data[sheet].copy()
    calculated_data = st.session_state.calculated_data[sheet].copy()
        
    columns_to_drop = ['Annee', 'Mois', 'M2_trg', 'M4_trg', 'M6_trg',]
    
    edited_data = edited_data.drop(columns_to_drop, axis=1)
    new_df = pd.concat([calculated_data, edited_data], axis=1).reindex(calculated_data.index)
    columns_order = [0, 1, 2, 3, 8, 4, 5, 9 , 6, 7, 10]
    aggregate_df = new_df.iloc[:, columns_order]
    aggregate_df = add_visualization_data(aggregate_df)
    row_total = aggregate_df[12::1]
    row_total.at["total annee", 'Annee'] = sheet.split("_")[1]
    return aggregate_df, row_total

def upload_file():
    uploaded_file = st.file_uploader("Choisissez un fichier a traiter", type="xlsx")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        load_file(uploaded_file)
        
    
def add_ecart_objectif(data_frame):
    prime = 0 if data_frame['prime_evolution_toutes_machine'] is None else data_frame['prime_evolution_toutes_machine']
    objectif = 0 if data_frame['Objectif'] is None else data_frame['Objectif']
    ecart = abs(objectif - prime)
    data_frame.insert(12, 'Ecart Objectif', ecart)
    return data_frame

def color_survived(val):
    color = 'green' if val>500000 else 'red'
    return f'background-color: {color}'

def color_evolution(val):
    color = 'white'
    if val > 0:
        color = '#CCFF99'
    if val > 100:
        color = '#99FF33'
    if val > 200:
        color = '#66CC00'
    if val < 0:
        color = '#FF9999'
    if val < -100:
        color = '#FF3333'
    if val < -200:
        color = '#CC0000'
    css = f'background-color: {color}'
    return css

def get_summary():
    if 'summary' not in st.session_state:
        print("probleme with summary")
    else:
        summary = st.session_state.summary
        summary_frame = pd.concat(summary)
        columns_to_drop = ['Mois', 'M2_trg', 'M4_trg', 'M6_trg',]
    
        summary_frame = summary_frame.drop(columns_to_drop, axis=1)
        summary_frame["Objectif"] = int(st.session_state.objectif)
        summary_frame = add_ecart_objectif(summary_frame)
        summary_frame.loc['Total'] = summary_frame.sum(numeric_only=True)
        summary_frame.loc[summary_frame.index[-1], 'Annee'] = 'Total sur '+str(len(st.session_state.data_sheet_list))+' ans'
        st.write("Resumé : ")
        summary_frame.reset_index(inplace=True)
        summary_frame = summary_frame.style.map(color_evolution, subset=['M4_prime_evolution', 'M2_prime_evolution', 'M6_prime_evolution', 'prime_evolution_toutes_machine'])
        
        st.dataframe(summary_frame, column_config={
            'M2_prime': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'M2_prime_proposee': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'M4_prime': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'M4_prime_proposee': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'M6_prime': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'M6_prime_proposee': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'prime_evolution_toutes_machine': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'Objectif': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'Ecart Objectif': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'M2_prime_evolution': st.column_config.NumberColumn(step=1, format='%.2f'),
            'M4_prime_evolution': st.column_config.NumberColumn(step=2, format='%.2f' ),
            'M6_prime_evolution': st.column_config.NumberColumn(step=2, format='%.2f' ),
            }
        )
    pass

def objectif():
    objectif = st.text_input("Definissez votre objectif par mois (attention, chiffre en negatif pour une reduction des primes)")
    if objectif:
        st.session_state.objectif = int(objectif) * 12
        get_result_aggregate()

def main():
    st.session_state.objectif = 0
    file_name = load_file('trg_simu.xlsx')
    
    data_sheets()
    display_editable_bonus()
    # upload_file()
    
if __name__ == '__main__':
    main()