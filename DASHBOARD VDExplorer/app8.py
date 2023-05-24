# # # # # # import streamlit as st
# # # # # # import pandas as pd
# # # # # # import plotly.express as px
# # # # # # from google.cloud import bigquery
# # # # # # from google.oauth2 import service_account
# # # # # # import datetime
# # # # # # import uuid

# # # # # # def add_entry(area, line, machine, date, comment):
# # # # # #     # Generowanie unikalnego id
# # # # # #     new_id = str(uuid.uuid4())

# # # # # #     # Tworzenie DataFrame z nowymi danymi
# # # # # #     new_data = pd.DataFrame({
# # # # # #         'areas': [area],
# # # # # #         'lines': [line],
# # # # # #         'level7': [machine],
# # # # # #         'time': [date],
# # # # # #         'KOMENTARZ': [comment],
# # # # # #         'id': [new_id]
# # # # # #     })

# # # # # #     # Zapisywanie DataFrame do BigQuery
# # # # # #     new_data['time'] = pd.to_datetime(new_data['time'])
# # # # # #     dataset_id = 'kellogg'
# # # # # #     table_id = 'kellog_set_3'
# # # # # #     table_ref = client.dataset(dataset_id).table(table_id)
# # # # # #     job = client.load_table_from_dataframe(new_data, table_ref, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
# # # # # #     job.result()  # Czekaj na zakończenie operacji
# # # # # #     st.success("Wpis został dodany.")
    


# # # # # # credentials = service_account.Credentials.from_service_account_file(r'icareolsztyn-d0b9397da7a5.json')

# # # # # # project_id = 'icareolsztyn'
# # # # # # client = bigquery.Client(credentials=credentials, project=project_id)
# # # # # # st.set_page_config(layout="wide")

# # # # # # st.title("VDExplorer 0.1")

# # # # # # def fetch_data_from_bigquery():
# # # # # #     query = """
# # # # # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # # # # #         FROM kellogg.kellog_set_3
# # # # # #         WHERE meas_id IS NULL
# # # # # #         """
# # # # # #     data_selection = client.query(query).to_dataframe()

# # # # # #     # Usuń wiersze z brakującymi datami
# # # # # #     data_selection = data_selection.dropna(subset=['time'])

# # # # # #     return data_selection


# # # # # # def fetch_other_data_from_bigquery_meas():
# # # # # #     query_meas = """
# # # # # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # # # # #         FROM kellogg.kellog_set_3
# # # # # #         """
# # # # # #     data_selection_meas = client.query(query_meas).to_dataframe()

# # # # # #     return data_selection_meas

# # # # # # def update_record_in_bigquery(record_id, updated_comment):
# # # # # #     query = """
# # # # # #         UPDATE kellogg.kellog_set_3
# # # # # #         SET KOMENTARZ_ZWROTNY = @updated_comment
# # # # # #         WHERE id = @record_id
# # # # # #     """
# # # # # #     job_config = bigquery.QueryJobConfig(
# # # # # #         query_parameters=[
# # # # # #             bigquery.ScalarQueryParameter("updated_comment", "STRING", updated_comment),
# # # # # #             bigquery.ScalarQueryParameter("record_id", "STRING", record_id),
# # # # # #         ]
# # # # # #     )
# # # # # #     client.query(query, job_config=job_config)


# # # # # # def save_changes(rows_to_update):
# # # # # #     for row in rows_to_update:
# # # # # #         record_id = row.id
# # # # # #         updated_comment = row.KOMENTARZ_ZWROTNY
# # # # # #         update_record_in_bigquery(record_id, updated_comment)
# # # # # #     st.success("Zmiany zostały zapisane.")

# # # # # # df = fetch_data_from_bigquery()

# # # # # # # Przekształcenie kolumny "Data" na format daty
# # # # # # df['time'] = pd.to_datetime(df['time']).dt.date

# # # # # # # Dodawanie przejść do innych stron w sidebarze
# # # # # # page_selection = st.sidebar.selectbox("Przejdź do:", ["Raporty", "Dane pomiarowe", "Trzecia strona"])
# # # # # # selected_time_start = None
# # # # # # selected_time_end = None
# # # # # # date_range_start = None
# # # # # # date_range_end = None

# # # # # # if page_selection == "Raporty":
# # # # # #     col0, col1, col2, col3, col4, col5 = st.columns(6)
# # # # # #     with col0:
# # # # # #         # Wybór obszaru
# # # # # #         selected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key='selected_area_key')
# # # # # #     with col1:
# # # # # #         # Wybór obszaru
# # # # # #         selected_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == selected_area, 'lines'].unique().tolist()) if selected_area else [""], key='selected_line_key')
# # # # # #     with col2:
# # # # # #         # Wybór maszyny
# # # # # #         selected_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == selected_area) & (df['lines'] == selected_line), 'level7'].unique().tolist()) if selected_area and selected_line else [""], key='selected_machine_key')
# # # # # #     with col3:
# # # # # #         # Wybór statusu
# # # # # #         status_values = [x for x in df['STATUS'].unique().tolist() if x is not None]
# # # # # #         selected_status = st.selectbox("Wybierz status:", [""] + sorted(status_values), key='selected_status_key')
# # # # # #     with col4:
# # # # # #         # Wybór zakresu dat
# # # # # #         date_range_start = st.date_input("Wybierz początek zakresu dat:", value=(date_range_start or df['time'].min()), key='date_range_start_key')
# # # # # #     with col5:
# # # # # #         # Wybór zakresu dat
# # # # # #         date_range_end = st.date_input("Wybierz koniec zakresu dat:", value=(date_range_end or df['time'].max()), key='date_range_end_key')

# # # # # #     if 'selected_area_key' not in st.session_state:
# # # # # #         st.session_state['selected_area_key'] = ""
# # # # # #         elected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key=st.session_state['selected_area_key'])

# # # # # #     if st.button("Resetuj filtry"):
# # # # # #         st.session_state['selected_area_key'] = ""
# # # # # #         selected_line = ""
# # # # # #         selected_machine = ""
# # # # # #         selected_status = ""
# # # # # #         date_range_start = None
# # # # # #         date_range_end = None

# # # # # #         selected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key=st.session_state['selected_area_key'])

# # # # # #     if 'selected_area_key' not in st.session_state:
# # # # # #         st.session_state['selected_area_key'] = ""
# # # # # #         st.session_state['selected_line_key'] = ""
# # # # # #         st.session_state['selected_machine_key'] = ""
# # # # # #         st.session_state['selected_status_key'] = ""
# # # # # #         st.session_state['date_range_start_key'] = None
# # # # # #         st.session_state['date_range_end_key'] = None
        


# # # # # #     filtered_df = df[
# # # # # #     ((df['areas'] == selected_area) if selected_area else True) &
# # # # # #     ((df['lines'] == selected_line) if selected_line else True) &
# # # # # #     ((df['level7'] == selected_machine) if selected_machine else True) &
# # # # # #     ((df['STATUS'] == selected_status) if selected_status else True) &
# # # # # #     ((df['time'] >= date_range_start) if date_range_start else True) &
# # # # # #     ((df['time'] <= date_range_end) if date_range_end else True)
# # # # # #     ]


# # # # # #     # Wyświetl tabelę raportów
# # # # # #        # Wyświetl tabelę raportów
# # # # # #     st.experimental_data_editor(filtered_df)

# # # # # #     # Wyświetl wykres kołowy dla STATUS
# # # # # #     status_counts = filtered_df['STATUS'].value_counts()
# # # # # #     fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Rozkład statusów')
# # # # # #     st.plotly_chart(fig)

# # # # # #     rows_to_update = []

# # # # # #     for row in filtered_df.itertuples(index=False):
# # # # # #         if getattr(row, "KOMENTARZ_ZWROTNY") != getattr(row, "KOMENTARZ_ZWROTNY", None):
# # # # # #             rows_to_update.append(row)

# # # # # #     if st.button("Zapisz"):
# # # # # #         save_changes(rows_to_update)

# # # # # # # Dodaj ten kod w miejscu, gdzie chcesz, aby pojawił się expander do dodawania wpisów.
# # # # # # # W tym przypadku dodaję go zaraz po wykresie kołowym.

# # # # # #     expander = st.expander("Dodaj wpis")
# # # # # #     with expander:
# # # # # #         # Dla wyboru obszaru
# # # # # #         new_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key="new_area_select")

# # # # # #         # Dla wyboru linii/podobszaru
# # # # # #         new_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == new_area, 'lines'].unique().tolist()) if new_area else [""], key="new_line_select")

# # # # # #         # Dla wyboru maszyny
# # # # # #         new_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == new_area) & (df['lines'] == new_line), 'level7'].unique().tolist()) if new_area and new_line else [""], key="new_machine_select")
 
# # # # # #         new_date = st.date_input("Wybierz datę:")
# # # # # #         new_comment = st.text_input("Wpisz komentarz:")
# # # # # #         if st.button("Dodaj wpis"):
# # # # # #             add_entry(new_area, new_line, new_machine, new_date, new_comment)

# # # # # # elif page_selection == "Dane pomiarowe":
# # # # # #     # Kod dla strony "Dane pomiarowe"
# # # # # #     # st.write("Tu będzie zawartość strony Dane pomiarowe")  # Usuwamy ten wiersz
# # # # # #     st.markdown(
# # # # # #         f'<iframe width="1400" height="1050" src="https://lookerstudio.google.com/embed/reporting/fe1fe97e-c903-4a68-9547-e070ff846367/page/p_74qqhk3h4c" frameborder="0" style="border:0" allowfullscreen></iframe>', 
# # # # # #         unsafe_allow_html=True
# # # # # #     )

# # # # # # elif page_selection == "Trzecia strona":
# # # # # #     other_df = fetch_other_data_from_bigquery_meas()

# # # # # #     # Przekształcenie kolumny "time" na format daty
# # # # # #     other_df['time'] = pd.to_datetime(other_df['time']).dt.date

# # # # # #     # Filtruj dane na podstawie wybranych opcji
# # # # # #     selected_level7 = st.selectbox("Wybierz level7:", [""] + sorted(other_df['level7'].unique().tolist()))
# # # # # #     filtered_other_df = other_df[other_df['level7'] == selected_level7]

# # # # # #     ten_years_ago = datetime.datetime.now() - datetime.timedelta(years=10)
# # # # # #     selected_time_start = st.date_input("Wybierz początek zakresu Time:", value=(selected_time_start or filtered_other_df['time'].min()), min_value=ten_years_ago)
# # # # # #     selected_time_end = st.date_input("Wybierz koniec zakresu Time:", value=(selected_time_end or filtered_other_df['time'].max()))

# # # # # #     filtered_other_df = filtered_other_df[
# # # # # #         (filtered_other_df['time'] >= selected_time_start) |
# # # # # #         (selected_time_start is None)
# # # # # #     ]
# # # # # #     filtered_other_df = filtered_other_df[
# # # # # #         (filtered_other_df['time'] <= selected_time_end) |
# # # # # #         (selected_time_end is None)
# # # # # #     ]

# # # # # #     # Przekształcenie wartości "value" dla type_x = "obr/min"
# # # # # #     filtered_other_df.loc[filtered_other_df['type_x'] == 'obr/min', 'value'] *= 60

# # # # # #     # Dodaj wykres liniowy dla "value" (type_x: mm/s)
# # # # # #     fig_mm_s = px.line(filtered_other_df[filtered_other_df['type_x'] == 'mm/s'], x="time", y="value", title='Wykres liniowy dla Value (mm/s)')
# # # # # #     fig_mm_s.update_traces(mode='markers+lines', hovertemplate=None)
# # # # # #     fig_mm_s.update_layout(hovermode='closest')
# # # # # #     fig_mm_s.update_traces(textposition='top center')
# # # # # #     fig_mm_s.update_traces(hovertemplate='Value: %{y}')
# # # # # #     fig_mm_s.update_layout(
# # # # # #         xaxis=dict(
# # # # # #             rangeselector=dict(
# # # # # #                 buttons=list([
# # # # # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # # # # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # # # # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # # # # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # # # # #                     dict(step="all")
# # # # # #                 ])
# # # # # #             ),
# # # # # #             rangeslider=dict(visible=True),
# # # # # #             type="date"
# # # # # #         )
# # # # # #     )

# # # # # #     # Dodaj wykres liniowy dla "value" (type_x: obr/min)
# # # # # #     fig_obr_min = px.line(filtered_other_df[filtered_other_df['type_x'] == 'obr/min'], x="time", y="value", title='Wykres liniowy dla Value (obr/min)')
# # # # # #     fig_obr_min.update_traces(mode='markers+lines', hovertemplate=None)
# # # # # #     fig_obr_min.update_layout(hovermode='closest')
# # # # # #     fig_obr_min.update_traces(textposition='top center')
# # # # # #     fig_obr_min.update_traces(hovertemplate='Value: %{y}')
# # # # # #     fig_obr_min.update_layout(
# # # # # #         xaxis=dict(
# # # # # #             rangeselector=dict(
# # # # # #                 buttons=list([
# # # # # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # # # # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # # # # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # # # # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # # # # #                     dict(step="all")
# # # # # #                 ])
# # # # # #             ),
# # # # # #             rangeslider=dict(visible=True),
# # # # # #             type="date"
# # # # # #         )
# # # # # #     )

# # # # # #     col0, col1 = st.columns(2)
# # # # # #     with col0:
# # # # # #         # Wyświetl tabelę
# # # # # #         st.write(filtered_other_df)

# # # # # #     with col1:
# # # # # #         # Wyświetl wykresy
# # # # # #         st.plotly_chart(fig_mm_s)
# # # # # #         st.plotly_chart(fig_obr_min)

# # # # # import streamlit as st
# # # # # import pandas as pd
# # # # # import plotly.express as px
# # # # # from google.cloud import bigquery
# # # # # from google.oauth2 import service_account
# # # # # import datetime
# # # # # import uuid

# # # # # def add_entry(area, line, machine, date, comment):
# # # # #     # Generowanie unikalnego id
# # # # #     new_id = str(uuid.uuid4())

# # # # #     # Tworzenie DataFrame z nowymi danymi
# # # # #     new_data = pd.DataFrame({
# # # # #         'areas': [area],
# # # # #         'lines': [line],
# # # # #         'level7': [machine],
# # # # #         'time': [date],
# # # # #         'KOMENTARZ': [comment],
# # # # #         'id': [new_id]
# # # # #     })

# # # # #     # Zapisywanie DataFrame do BigQuery
# # # # #     new_data['time'] = pd.to_datetime(new_data['time'])
# # # # #     dataset_id = 'kellogg'
# # # # #     table_id = 'kellog_set_3'
# # # # #     table_ref = client.dataset(dataset_id).table(table_id)
# # # # #     job = client.load_table_from_dataframe(new_data, table_ref, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
# # # # #     job.result()  # Czekaj na zakończenie operacji
# # # # #     st.success("Wpis został dodany.")

# # # # # credentials = service_account.Credentials.from_service_account_file(r'icareolsztyn-d0b9397da7a5.json')
# # # # # project_id = 'icareolsztyn'
# # # # # client = bigquery.Client(credentials=credentials, project=project_id)
# # # # # st.set_page_config(layout="wide")

# # # # # st.title("VDExplorer 0.1")

# # # # # def fetch_data_from_bigquery():
# # # # #     query = """
# # # # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # # # #         FROM kellogg.kellog_set_3
# # # # #         WHERE meas_id IS NULL
# # # # #         """
# # # # #     data_selection = client.query(query).to_dataframe()

# # # # #     # Usuń wiersze z brakującymi datami
# # # # #     data_selection = data_selection.dropna(subset=['time'])

# # # # #     return data_selection


# # # # # def fetch_other_data_from_bigquery_meas():
# # # # #     query_meas = """
# # # # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # # # #         FROM kellogg.kellog_set_3
# # # # #         """
# # # # #     data_selection_meas = client.query(query_meas).to_dataframe()

# # # # #     return data_selection_meas

# # # # # def update_record_in_bigquery(record_id, updated_comment):
# # # # #     query = """
# # # # #         UPDATE kellogg.kellog_set_3
# # # # #         SET KOMENTARZ_ZWROTNY = @updated_comment
# # # # #         WHERE id = @record_id
# # # # #     """
# # # # #     job_config = bigquery.QueryJobConfig(
# # # # #         query_parameters=[
# # # # #             bigquery.ScalarQueryParameter("updated_comment", "STRING", updated_comment),
# # # # #             bigquery.ScalarQueryParameter("record_id", "STRING", record_id),
# # # # #         ]
# # # # #     )
# # # # #     client.query(query, job_config=job_config)


# # # # # def save_changes(rows_to_update):
# # # # #     for row in rows_to_update:
# # # # #         record_id = row.id
# # # # #         updated_comment = row.KOMENTARZ_ZWROTNY
# # # # #         update_record_in_bigquery(record_id, updated_comment)
# # # # #     st.success("Zmiany zostały zapisane.")

# # # # # df = fetch_data_from_bigquery()

# # # # # # Przekształcenie kolumny "Data" na format daty
# # # # # df['time'] = pd.to_datetime(df['time']).dt.date

# # # # # # Dodawanie przejść do innych stron w sidebarze
# # # # # page_selection = st.sidebar.selectbox("Przejdź do:", ["Raporty", "Dane pomiarowe", "Trzecia strona"])
# # # # # selected_time_start = None
# # # # # selected_time_end = None
# # # # # date_range_start = None
# # # # # date_range_end = None

# # # # # if page_selection == "Raporty":
# # # # #     col0, col1, col2, col3, col4, col5 = st.columns(6)
# # # # #     with col0:
# # # # #         # Wybór obszaru
# # # # #         if 'selected_area_key' not in st.session_state:
# # # # #             st.session_state['selected_area_key'] = ""
# # # # #         selected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key='selected_area_key')

# # # # #     with col1:
# # # # #         # Wybór lini/podobszaru
# # # # #         if 'selected_line_key' not in st.session_state:
# # # # #             st.session_state['selected_line_key'] = ""
# # # # #         selected_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == selected_area, 'lines'].unique().tolist()) if selected_area else [""], key='selected_line_key')

# # # # #     with col2:
# # # # #         # Wybór maszyny
# # # # #         if 'selected_machine_key' not in st.session_state:
# # # # #             st.session_state['selected_machine_key'] = ""
# # # # #         selected_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == selected_area) & (df['lines'] == selected_line), 'level7'].unique().tolist()) if selected_area and selected_line else [""], key='selected_machine_key')

# # # # #     with col3:
# # # # #         # Wybór statusu
# # # # #         if 'selected_status_key' not in st.session_state:
# # # # #             st.session_state['selected_status_key'] = ""
# # # # #         status_values = [x for x in df['STATUS'].unique().tolist() if x is not None]
# # # # #         selected_status = st.selectbox("Wybierz status:", [""] + sorted(status_values), key='selected_status_key')

# # # # #     with col4:
# # # # #         # Wybór zakresu dat
# # # # #         if 'date_range_start_key' not in st.session_state:
# # # # #             st.session_state['date_range_start_key'] = None
# # # # #         date_range_start = st.date_input("Wybierz początek zakresu dat:", value=(date_range_start or df['time'].min()), key='date_range_start_key')

# # # # #     with col5:
# # # # #         # Wybór zakresu dat
# # # # #         if 'date_range_end_key' not in st.session_state:
# # # # #             st.session_state['date_range_end_key'] = None
# # # # #         date_range_end = st.date_input("Wybierz koniec zakresu dat:", value=(date_range_end or df['time'].max()), key='date_range_end_key')

# # # # #     if st.button("Resetuj filtry"):
# # # # #         st.session_state['selected_area_key'] = ""
# # # # #         st.session_state['selected_line_key'] = ""
# # # # #         st.session_state['selected_machine_key'] = ""
# # # # #         st.session_state['selected_status_key'] = ""
# # # # #         st.session_state['date_range_start_key'] = None
# # # # #         st.session_state['date_range_end_key'] = None

# # # # #     filtered_df = df[
# # # # #         ((df['areas'] == selected_area) if selected_area else True) &
# # # # #         ((df['lines'] == selected_line) if selected_line else True) &
# # # # #         ((df['level7'] == selected_machine) if selected_machine else True) &
# # # # #         ((df['STATUS'] == selected_status) if selected_status else True) &
# # # # #         ((df['time'] >= date_range_start) if date_range_start else True) &
# # # # #         ((df['time'] <= date_range_end) if date_range_end else True)
# # # # #     ]

# # # # #     # Wyświetl tabelę raportów
# # # # #     st.experimental_data_editor(filtered_df)

# # # # #     # Wyświetl wykres kołowy dla STATUS
# # # # #     status_counts = filtered_df['STATUS'].value_counts()
# # # # #     fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Rozkład statusów')
# # # # #     st.plotly_chart(fig)

# # # # #     rows_to_update = []

# # # # #     for row in filtered_df.itertuples(index=False):
# # # # #         if getattr(row, "KOMENTARZ_ZWROTNY") != getattr(row, "KOMENTARZ_ZWROTNY", None):
# # # # #             rows_to_update.append(row)

# # # # #     if st.button("Zapisz"):
# # # # #         save_changes(rows_to_update)

# # # # #     # Dodaj ten kod w miejscu, gdzie chcesz, aby pojawił się expander do dodawania wpisów.
# # # # #     # W tym przypadku dodaję go zaraz po wykresie kołowym.
# # # # #     expander = st.expander("Dodaj wpis")
# # # # #     with expander:
# # # # #         # Dla wyboru obszaru
# # # # #         new_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key="new_area_select")

# # # # #         # Dla wyboru linii/podobszaru
# # # # #         new_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == new_area, 'lines'].unique().tolist()) if new_area else [""], key="new_line_select")

# # # # #         # Dla wyboru maszyny
# # # # #         new_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == new_area) & (df['lines'] == new_line), 'level7'].unique().tolist()) if new_area and new_line else [""], key="new_machine_select")
 
# # # # #         new_date = st.date_input("Wybierz datę:")
# # # # #         new_comment = st.text_input("Wpisz komentarz:")
# # # # #         if st.button("Dodaj wpis"):
# # # # #             add_entry(new_area, new_line, new_machine, new_date, new_comment)

# # # # # elif page_selection == "Dane pomiarowe":
# # # # #     # Kod dla strony "Dane pomiarowe"
# # # # #     # st.write("Tu będzie zawartość strony Dane pomiarowe")  # Usuwamy ten wiersz
# # # # #     st.markdown(
# # # # #         f'<iframe width="1400" height="1050" src="https://lookerstudio.google.com/embed/reporting/fe1fe97e-c903-4a68-9547-e070ff846367/page/p_74qqhk3h4c" frameborder="0" style="border:0" allowfullscreen></iframe>', 
# # # # #         unsafe_allow_html=True
# # # # #     )

# # # # # elif page_selection == "Trzecia strona":
# # # # #     other_df = fetch_other_data_from_bigquery_meas()

# # # # #     # Przekształcenie kolumny "time" na format daty
# # # # #     other_df['time'] = pd.to_datetime(other_df['time']).dt.date

# # # # #     # Filtruj dane na podstawie wybranych opcji
# # # # #     selected_level7 = st.selectbox("Wybierz level7:", [""] + sorted(other_df['level7'].unique().tolist()))
# # # # #     filtered_other_df = other_df[other_df['level7'] == selected_level7]

# # # # #     ten_years_ago = datetime.datetime.now() - datetime.timedelta(years=10)
# # # # #     selected_time_start = st.date_input("Wybierz początek zakresu Time:", value=(selected_time_start or filtered_other_df['time'].min()), min_value=ten_years_ago)
# # # # #     selected_time_end = st.date_input("Wybierz koniec zakresu Time:", value=(selected_time_end or filtered_other_df['time'].max()))

# # # # #     filtered_other_df = filtered_other_df[
# # # # #         (filtered_other_df['time'] >= selected_time_start) |
# # # # #         (selected_time_start is None)
# # # # #     ]
# # # # #     filtered_other_df = filtered_other_df[
# # # # #         (filtered_other_df['time'] <= selected_time_end) |
# # # # #         (selected_time_end is None)
# # # # #     ]

# # # # #     # Przekształcenie wartości "value" dla type_x = "obr/min"
# # # # #     filtered_other_df.loc[filtered_other_df['type_x'] == 'obr/min', 'value'] *= 60

# # # # #     # Dodaj wykres liniowy dla "value" (type_x: mm/s)
# # # # #     fig_mm_s = px.line(filtered_other_df[filtered_other_df['type_x'] == 'mm/s'], x="time", y="value", title='Wykres liniowy dla Value (mm/s)')
# # # # #     fig_mm_s.update_traces(mode='markers+lines', hovertemplate=None)
# # # # #     fig_mm_s.update_layout(hovermode='closest')
# # # # #     fig_mm_s.update_traces(textposition='top center')
# # # # #     fig_mm_s.update_traces(hovertemplate='Value: %{y}')
# # # # #     fig_mm_s.update_layout(
# # # # #         xaxis=dict(
# # # # #             rangeselector=dict(
# # # # #                 buttons=list([
# # # # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # # # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # # # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # # # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # # # #                     dict(step="all")
# # # # #                 ])
# # # # #             ),
# # # # #             rangeslider=dict(visible=True),
# # # # #             type="date"
# # # # #         )
# # # # #     )

# # # # #     # Dodaj wykres liniowy dla "value" (type_x: obr/min)
# # # # #     fig_obr_min = px.line(filtered_other_df[filtered_other_df['type_x'] == 'obr/min'], x="time", y="value", title='Wykres liniowy dla Value (obr/min)')
# # # # #     fig_obr_min.update_traces(mode='markers+lines', hovertemplate=None)
# # # # #     fig_obr_min.update_layout(hovermode='closest')
# # # # #     fig_obr_min.update_traces(textposition='top center')
# # # # #     fig_obr_min.update_traces(hovertemplate='Value: %{y}')
# # # # #     fig_obr_min.update_layout(
# # # # #         xaxis=dict(
# # # # #             rangeselector=dict(
# # # # #                 buttons=list([
# # # # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # # # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # # # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # # # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # # # #                     dict(step="all")
# # # # #                 ])
# # # # #             ),
# # # # #             rangeslider=dict(visible=True),
# # # # #             type="date"
# # # # #         )
# # # # #     )

# # # # #     col0, col1 = st.columns(2)
# # # # #     with col0:
# # # # #         # Wyświetl tabelę
# # # # #         st.write(filtered_other_df)

# # # # #     with col1:
# # # # #         # Wyświetl wykresy
# # # # #         st.plotly_chart(fig_mm_s)
# # # # #         st.plotly_chart(fig_obr_min)

# # # # # import streamlit as st
# # # # # import pandas as pd
# # # # # import plotly.express as px
# # # # # from google.cloud import bigquery
# # # # # from google.oauth2 import service_account
# # # # # import datetime
# # # # # import uuid

# # # # # def add_entry(area, line, machine, date, comment):
# # # # #     # Generowanie unikalnego id
# # # # #     new_id = str(uuid.uuid4())

# # # # #     # Tworzenie DataFrame z nowymi danymi
# # # # #     new_data = pd.DataFrame({
# # # # #         'areas': [area],
# # # # #         'lines': [line],
# # # # #         'level7': [machine],
# # # # #         'time': [date],
# # # # #         'KOMENTARZ': [comment],
# # # # #         'id': [new_id]
# # # # #     })

# # # # #     # Zapisywanie DataFrame do BigQuery
# # # # #     new_data['time'] = pd.to_datetime(new_data['time'])
# # # # #     dataset_id = 'kellogg'
# # # # #     table_id = 'kellog_set_3'
# # # # #     table_ref = client.dataset(dataset_id).table(table_id)
# # # # #     job = client.load_table_from_dataframe(new_data, table_ref, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
# # # # #     job.result()  # Czekaj na zakończenie operacji
# # # # #     st.success("Wpis został dodany.")

# # # # # credentials = service_account.Credentials.from_service_account_file(r'icareolsztyn-d0b9397da7a5.json')

# # # # # project_id = 'icareolsztyn'
# # # # # client = bigquery.Client(credentials=credentials, project=project_id)
# # # # # st.set_page_config(layout="wide")

# # # # # st.title("VDExplorer 0.1")

# # # # # def fetch_data_from_bigquery():
# # # # #     query = """
# # # # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # # # #         FROM kellogg.kellog_set_3
# # # # #         WHERE meas_id IS NULL
# # # # #         """
# # # # #     data_selection = client.query(query).to_dataframe()

# # # # #     # Usuń wiersze z brakującymi datami
# # # # #     data_selection = data_selection.dropna(subset=['time'])

# # # # #     return data_selection


# # # # # def fetch_other_data_from_bigquery_meas():
# # # # #     query_meas = """
# # # # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # # # #         FROM kellogg.kellog_set_3
# # # # #         """
# # # # #     data_selection_meas = client.query(query_meas).to_dataframe()

# # # # #     return data_selection_meas

# # # # # def update_record_in_bigquery(record_id, updated_comment):
# # # # #     query = """
# # # # #         UPDATE kellogg.kellog_set_3
# # # # #         SET KOMENTARZ_ZWROTNY = @updated_comment
# # # # #         WHERE id = @record_id
# # # # #     """
# # # # #     job_config = bigquery.QueryJobConfig(
# # # # #         query_parameters=[
# # # # #             bigquery.ScalarQueryParameter("updated_comment", "STRING", updated_comment),
# # # # #             bigquery.ScalarQueryParameter("record_id", "STRING", record_id),
# # # # #         ]
# # # # #     )
# # # # #     client.query(query, job_config=job_config)


# # # # # def save_changes(rows_to_update):
# # # # #     for row in rows_to_update:
# # # # #         record_id = row.id
# # # # #         updated_comment = row.KOMENTARZ_ZWROTNY
# # # # #         update_record_in_bigquery(record_id, updated_comment)
# # # # #     st.success("Zmiany zostały zapisane.")

# # # # # df = fetch_data_from_bigquery()

# # # # # # Przekształcenie kolumny "Data" na format daty
# # # # # df['time'] = pd.to_datetime(df['time']).dt.date

# # # # # # Dodawanie przejść do innych stron w sidebarze
# # # # # page_selection = st.sidebar.selectbox("Przejdź do:", ["Raporty", "Dane pomiarowe", "Trzecia strona"])
# # # # # selected_time_start = None
# # # # # selected_time_end = None
# # # # # date_range_start = None
# # # # # date_range_end = None

# # # # # if page_selection == "Raporty":
# # # # #     col0, col1, col2, col3, col4, col5 = st.columns(6)
# # # # #     with col0:
# # # # #         if 'selected_area_key' not in st.session_state:
# # # # #             st.session_state['selected_area_key'] = ""
# # # # #         # Wybór obszaru
# # # # #         selected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key=st.session_state['selected_area_key'])
# # # # #     with col1:
# # # # #         # Wybór obszaru
# # # # #         selected_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == selected_area, 'lines'].unique().tolist()) if selected_area else [""], key='selected_line_key')
# # # # #     with col2:
# # # # #         # Wybór maszyny
# # # # #         selected_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == selected_area) & (df['lines'] == selected_line), 'level7'].unique().tolist()) if selected_area and selected_line else [""], key='selected_machine_key')
# # # # #     with col3:
# # # # #         # Wybór statusu
# # # # #         status_values = [x for x in df['STATUS'].unique().tolist() if x is not None]
# # # # #         selected_status = st.selectbox("Wybierz status:", [""] + sorted(status_values), key='selected_status_key')
# # # # #     with col4:
# # # # #         # Wybór zakresu dat
# # # # #         date_range_start = st.date_input("Wybierz początek zakresu dat:", value=(date_range_start or df['time'].min()), key='date_range_start_key')
# # # # #     with col5:
# # # # #         # Wybór zakresu dat
# # # # #         date_range_end = st.date_input("Wybierz koniec zakresu dat:", value=(date_range_end or df['time'].max()), key='date_range_end_key')


# # # # #     filtered_df = df[
# # # # #         ((df['areas'] == selected_area) if selected_area else True) &
# # # # #         ((df['lines'] == selected_line) if selected_line else True) &
# # # # #         ((df['level7'] == selected_machine) if selected_machine else True) &
# # # # #         ((df['STATUS'] == selected_status) if selected_status else True) &
# # # # #         ((df['time'] >= date_range_start) if date_range_start else True) &
# # # # #         ((df['time'] <= date_range_end) if date_range_end else True)
# # # # #     ]

# # # # #     # Wyświetl tabelę raportów
# # # # #     st.experimental_data_editor(filtered_df)

# # # # #     # Wyświetl wykres kołowy dla STATUS
# # # # #     status_counts = filtered_df['STATUS'].value_counts()
# # # # #     fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Rozkład statusów')
# # # # #     st.plotly_chart(fig)

# # # # #     rows_to_update = []

# # # # #     for row in filtered_df.itertuples(index=False):
# # # # #         if getattr(row, "KOMENTARZ_ZWROTNY") != getattr(row, "KOMENTARZ_ZWROTNY", None):
# # # # #             rows_to_update.append(row)

# # # # #     if st.button("Zapisz"):
# # # # #         save_changes(rows_to_update)

# # # # #     # Dodaj ten kod w miejscu, gdzie chcesz, aby pojawił się expander do dodawania wpisów.
# # # # #     # W tym przypadku dodaję go zaraz po wykresie kołowym.

# # # # #     expander = st.expander("Dodaj wpis")
# # # # #     with expander:
# # # # #         # Dla wyboru obszaru
# # # # #         new_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key="new_area_select")

# # # # #         # Dla wyboru linii/podobszaru
# # # # #         new_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == new_area, 'lines'].unique().tolist()) if new_area else [""], key="new_line_select")

# # # # #         # Dla wyboru maszyny
# # # # #         new_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == new_area) & (df['lines'] == new_line), 'level7'].unique().tolist()) if new_area and new_line else [""], key="new_machine_select")

# # # # #         new_date = st.date_input("Wybierz datę:")
# # # # #         new_comment = st.text_input("Wpisz komentarz:")
# # # # #         if st.button("Dodaj wpis"):
# # # # #             add_entry(new_area, new_line, new_machine, new_date, new_comment)

# # # # # elif page_selection == "Dane pomiarowe":
# # # # #     # Kod dla strony "Dane pomiarowe"
# # # # #     # st.write("Tu będzie zawartość strony Dane pomiarowe")  # Usuwamy ten wiersz
# # # # #     st.markdown(
# # # # #         f'<iframe width="1400" height="1050" src="https://lookerstudio.google.com/embed/reporting/fe1fe97e-c903-4a68-9547-e070ff846367/page/p_74qqhk3h4c" frameborder="0" style="border:0" allowfullscreen></iframe>', 
# # # # #         unsafe_allow_html=True
# # # # #     )

# # # # # elif page_selection == "Trzecia strona":
# # # # #     other_df = fetch_other_data_from_bigquery_meas()

# # # # #     # Przekształcenie kolumny "time" na format daty
# # # # #     other_df['time'] = pd.to_datetime(other_df['time']).dt.date

# # # # #     # Filtruj dane na podstawie wybranych opcji
# # # # #     selected_level7 = st.selectbox("Wybierz level7:", [""] + sorted(other_df['level7'].unique().tolist()))
# # # # #     filtered_other_df = other_df[other_df['level7'] == selected_level7]

# # # # #     ten_years_ago = datetime.datetime.now() - datetime.timedelta(years=10)
# # # # #     selected_time_start = st.date_input("Wybierz początek zakresu Time:", value=(selected_time_start or filtered_other_df['time'].min()), min_value=ten_years_ago)
# # # # #     selected_time_end = st.date_input("Wybierz koniec zakresu Time:", value=(selected_time_end or filtered_other_df['time'].max()))

# # # # #     filtered_other_df = filtered_other_df[
# # # # #         (filtered_other_df['time'] >= selected_time_start) |
# # # # #         (selected_time_start is None)
# # # # #     ]
# # # # #     filtered_other_df = filtered_other_df[
# # # # #         (filtered_other_df['time'] <= selected_time_end) |
# # # # #         (selected_time_end is None)
# # # # #     ]

# # # # #     # Przekształcenie wartości "value" dla type_x = "obr/min"
# # # # #     filtered_other_df.loc[filtered_other_df['type_x'] == 'obr/min', 'value'] *= 60

# # # # #     # Dodaj wykres liniowy dla "value" (type_x: mm/s)
# # # # #     fig_mm_s = px.line(filtered_other_df[filtered_other_df['type_x'] == 'mm/s'], x="time", y="value", title='Wykres liniowy dla Value (mm/s)')
# # # # #     fig_mm_s.update_traces(mode='markers+lines', hovertemplate=None)
# # # # #     fig_mm_s.update_layout(hovermode='closest')
# # # # #     fig_mm_s.update_traces(textposition='top center')
# # # # #     fig_mm_s.update_traces(hovertemplate='Value: %{y}')
# # # # #     fig_mm_s.update_layout(
# # # # #         xaxis=dict(
# # # # #             rangeselector=dict(
# # # # #                 buttons=list([
# # # # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # # # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # # # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # # # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # # # #                     dict(step="all")
# # # # #                 ])
# # # # #             ),
# # # # #             rangeslider=dict(visible=True),
# # # # #             type="date"
# # # # #         )
# # # # #     )

# # # # #     # Dodaj wykres liniowy dla "value" (type_x: obr/min)
# # # # #     fig_obr_min = px.line(filtered_other_df[filtered_other_df['type_x'] == 'obr/min'], x="time", y="value", title='Wykres liniowy dla Value (obr/min)')
# # # # #     fig_obr_min.update_traces(mode='markers+lines', hovertemplate=None)
# # # # #     fig_obr_min.update_layout(hovermode='closest')
# # # # #     fig_obr_min.update_traces(textposition='top center')
# # # # #     fig_obr_min.update_traces(hovertemplate='Value: %{y}')
# # # # #     fig_obr_min.update_layout(
# # # # #         xaxis=dict(
# # # # #             rangeselector=dict(
# # # # #                 buttons=list([
# # # # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # # # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # # # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # # # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # # # #                     dict(step="all")
# # # # #                 ])
# # # # #             ),
# # # # #             rangeslider=dict(visible=True),
# # # # #             type="date"
# # # # #         )
# # # # #     )

# # # # #     col0, col1 = st.columns(2)
# # # # #     with col0:
# # # # #         # Wyświetl tabelę
# # # # #         st.write(filtered_other_df)

# # # # #     with col1:
# # # # #         # Wyświetl wykresy
# # # # #         st.plotly_chart(fig_mm_s)
# # # # #         st.plotly_chart(fig_obr_min)
# # # # import streamlit as st
# # # # import pandas as pd
# # # # import plotly.express as px
# # # # from google.cloud import bigquery
# # # # from google.oauth2 import service_account
# # # # import datetime
# # # # import uuid

# # # # def add_entry(area, line, machine, date, comment):
# # # #     # Generowanie unikalnego id
# # # #     new_id = str(uuid.uuid4())

# # # #     # Tworzenie DataFrame z nowymi danymi
# # # #     new_data = pd.DataFrame({
# # # #         'areas': [area],
# # # #         'lines': [line],
# # # #         'level7': [machine],
# # # #         'time': [date],
# # # #         'KOMENTARZ': [comment],
# # # #         'id': [new_id]
# # # #     })

# # # #     # Zapisywanie DataFrame do BigQuery
# # # #     new_data['time'] = pd.to_datetime(new_data['time'])
# # # #     dataset_id = 'kellogg'
# # # #     table_id = 'kellog_set_3'
# # # #     table_ref = client.dataset(dataset_id).table(table_id)
# # # #     job = client.load_table_from_dataframe(new_data, table_ref, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
# # # #     job.result()  # Czekaj na zakończenie operacji
# # # #     st.success("Wpis został dodany.")

# # # # credentials = service_account.Credentials.from_service_account_file(r'icareolsztyn-d0b9397da7a5.json')

# # # # project_id = 'icareolsztyn'
# # # # client = bigquery.Client(credentials=credentials, project=project_id)
# # # # st.set_page_config(layout="wide")

# # # # st.title("VDExplorer 0.1")

# # # # def fetch_data_from_bigquery():
# # # #     query = """
# # # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # # #         FROM kellogg.kellog_set_3
# # # #         WHERE meas_id IS NULL
# # # #         """
# # # #     data_selection = client.query(query).to_dataframe()

# # # #     # Usuń wiersze z brakującymi datami
# # # #     data_selection = data_selection.dropna(subset=['time'])

# # # #     return data_selection


# # # # def fetch_other_data_from_bigquery_meas():
# # # #     query_meas = """
# # # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # # #         FROM kellogg.kellog_set_3
# # # #         """
# # # #     data_selection_meas = client.query(query_meas).to_dataframe()

# # # #     return data_selection_meas

# # # # def update_record_in_bigquery(record_id, updated_comment):
# # # #     query = """
# # # #         UPDATE kellogg.kellog_set_3
# # # #         SET KOMENTARZ_ZWROTNY = @updated_comment
# # # #         WHERE id = @record_id
# # # #     """
# # # #     job_config = bigquery.QueryJobConfig(
# # # #         query_parameters=[
# # # #             bigquery.ScalarQueryParameter("updated_comment", "STRING", updated_comment),
# # # #             bigquery.ScalarQueryParameter("record_id", "STRING", record_id),
# # # #         ]
# # # #     )
# # # #     client.query(query, job_config=job_config)


# # # # def save_changes(rows_to_update):
# # # #     for row in rows_to_update:
# # # #         record_id = row.id
# # # #         updated_comment = row.KOMENTARZ_ZWROTNY
# # # #         update_record_in_bigquery(record_id, updated_comment)
# # # #     st.success("Zmiany zostały zapisane.")

# # # # df = fetch_data_from_bigquery()

# # # # # Przekształcenie kolumny "Data" na format daty
# # # # df['time'] = pd.to_datetime(df['time']).dt.date

# # # # # Dodawanie przejść do innych stron w sidebarze
# # # # page_selection = st.sidebar.selectbox("Przejdź do:", ["Raporty", "Dane pomiarowe", "Trzecia strona"])
# # # # selected_time_start = None
# # # # selected_time_end = None
# # # # date_range_start = None
# # # # date_range_end = None

# # # # if page_selection == "Raporty":
# # # #     col0, col1, col2, col3, col4, col5 = st.columns(6)
# # # #     with col0:
# # # #         # Wybór obszaru
# # # #         selected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key='selected_area_key')
# # # #     with col1:
# # # #         # Wybór obszaru
# # # #         selected_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == selected_area, 'lines'].unique().tolist()) if selected_area else [""], key='selected_line_key')
# # # #     with col2:
# # # #         # Wybór maszyny
# # # #         selected_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == selected_area) & (df['lines'] == selected_line), 'level7'].unique().tolist()) if selected_area and selected_line else [""], key='selected_machine_key')
# # # #     with col3:
# # # #         # Wybór statusu
# # # #         status_values = [x for x in df['STATUS'].unique().tolist() if x is not None]
# # # #         selected_status = st.selectbox("Wybierz status:", [""] + sorted(status_values), key='selected_status_key')
# # # #     with col4:
# # # #         # Wybór zakresu dat
# # # #         date_range_start = st.date_input("Wybierz początek zakresu dat:", value=(date_range_start or df['time'].min()), key='date_range_start_key')
# # # #     with col5:
# # # #         # Wybór zakresu dat
# # # #         date_range_end = st.date_input("Wybierz koniec zakresu dat:", value=(date_range_end or df['time'].max()), key='date_range_end_key')

# # # #     filtered_df = df[
# # # #         ((df['areas'] == selected_area) if selected_area else True) &
# # # #         ((df['lines'] == selected_line) if selected_line else True) &
# # # #         ((df['level7'] == selected_machine) if selected_machine else True) &
# # # #         ((df['STATUS'] == selected_status) if selected_status else True) &
# # # #         ((df['time'] >= date_range_start) if date_range_start else True) &
# # # #         ((df['time'] <= date_range_end) if date_range_end else True)
# # # #     ]

# # # #     # Wyświetl tabelę raportów
# # # #     st.experimental_data_editor(filtered_df)

# # # #     # Wyświetl wykres kołowy dla STATUS
# # # #     status_counts = filtered_df['STATUS'].value_counts()
# # # #     fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Rozkład statusów')
# # # #     st.plotly_chart(fig)

# # # #     rows_to_update = []

# # # #     for row in filtered_df.itertuples(index=False):
# # # #         if getattr(row, "KOMENTARZ_ZWROTNY") != getattr(row, "KOMENTARZ_ZWROTNY", None):
# # # #             rows_to_update.append(row)

# # # #     if st.button("Zapisz"):
# # # #         save_changes(rows_to_update)

# # # #     # Dodaj ten kod w miejscu, gdzie chcesz, aby pojawił się expander do dodawania wpisów.
# # # #     # W tym przypadku dodaję go zaraz po wykresie kołowym.

# # # #     expander = st.expander("Dodaj wpis")
# # # #     with expander:
# # # #         # Dla wyboru obszaru
# # # #         new_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key="new_area_select")

# # # #         # Dla wyboru linii/podobszaru
# # # #         new_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == new_area, 'lines'].unique().tolist()) if new_area else [""], key="new_line_select")

# # # #         # Dla wyboru maszyny
# # # #         new_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == new_area) & (df['lines'] == new_line), 'level7'].unique().tolist()) if new_area and new_line else [""], key="new_machine_select")

# # # #         new_date = st.date_input("Wybierz datę:")
# # # #         new_comment = st.text_input("Wpisz komentarz:")
# # # #         if st.button("Dodaj wpis"):
# # # #             add_entry(new_area, new_line, new_machine, new_date, new_comment)

# # # # elif page_selection == "Dane pomiarowe":
# # # #     # Kod dla strony "Dane pomiarowe"
# # # #     # st.write("Tu będzie zawartość strony Dane pomiarowe")  # Usuwamy ten wiersz
# # # #     st.markdown(
# # # #         f'<iframe width="1400" height="1050" src="https://lookerstudio.google.com/embed/reporting/fe1fe97e-c903-4a68-9547-e070ff846367/page/p_74qqhk3h4c" frameborder="0" style="border:0" allowfullscreen></iframe>', 
# # # #         unsafe_allow_html=True
# # # #     )

# # # # elif page_selection == "Trzecia strona":
# # # #     other_df = fetch_other_data_from_bigquery_meas()

# # # #     # Przekształcenie kolumny "time" na format daty
# # # #     other_df['time'] = pd.to_datetime(other_df['time']).dt.date

# # # #     # Filtruj dane na podstawie wybranych opcji
# # # #     selected_level7 = st.selectbox("Wybierz level7:", [""] + sorted(other_df['level7'].unique().tolist()))
# # # #     filtered_other_df = other_df[other_df['level7'] == selected_level7]

# # # #     ten_years_ago = datetime.datetime.now() - datetime.timedelta(years=10)
# # # #     selected_time_start = st.date_input("Wybierz początek zakresu Time:", value=(selected_time_start or filtered_other_df['time'].min()), min_value=ten_years_ago)
# # # #     selected_time_end = st.date_input("Wybierz koniec zakresu Time:", value=(selected_time_end or filtered_other_df['time'].max()))

# # # #     filtered_other_df = filtered_other_df[
# # # #         (filtered_other_df['time'] >= selected_time_start) |
# # # #         (selected_time_start is None)
# # # #     ]
# # # #     filtered_other_df = filtered_other_df[
# # # #         (filtered_other_df['time'] <= selected_time_end) |
# # # #         (selected_time_end is None)
# # # #     ]

# # # #     # Przekształcenie wartości "value" dla type_x = "obr/min"
# # # #     filtered_other_df.loc[filtered_other_df['type_x'] == 'obr/min', 'value'] *= 60

# # # #     # Dodaj wykres liniowy dla "value" (type_x: mm/s)
# # # #     fig_mm_s = px.line(filtered_other_df[filtered_other_df['type_x'] == 'mm/s'], x="time", y="value", title='Wykres liniowy dla Value (mm/s)')
# # # #     fig_mm_s.update_traces(mode='markers+lines', hovertemplate=None)
# # # #     fig_mm_s.update_layout(hovermode='closest')
# # # #     fig_mm_s.update_traces(textposition='top center')
# # # #     fig_mm_s.update_traces(hovertemplate='Value: %{y}')
# # # #     fig_mm_s.update_layout(
# # # #         xaxis=dict(
# # # #             rangeselector=dict(
# # # #                 buttons=list([
# # # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # # #                     dict(step="all")
# # # #                 ])
# # # #             ),
# # # #             rangeslider=dict(visible=True),
# # # #             type="date"
# # # #         )
# # # #     )

# # # #     # Dodaj wykres liniowy dla "value" (type_x: obr/min)
# # # #     fig_obr_min = px.line(filtered_other_df[filtered_other_df['type_x'] == 'obr/min'], x="time", y="value", title='Wykres liniowy dla Value (obr/min)')
# # # #     fig_obr_min.update_traces(mode='markers+lines', hovertemplate=None)
# # # #     fig_obr_min.update_layout(hovermode='closest')
# # # #     fig_obr_min.update_traces(textposition='top center')
# # # #     fig_obr_min.update_traces(hovertemplate='Value: %{y}')
# # # #     fig_obr_min.update_layout(
# # # #         xaxis=dict(
# # # #             rangeselector=dict(
# # # #                 buttons=list([
# # # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # # #                     dict(step="all")
# # # #                 ])
# # # #             ),
# # # #             rangeslider=dict(visible=True),
# # # #             type="date"
# # # #         )
# # # #     )

# # # #     col0, col1 = st.columns(2)
# # # #     with col0:
# # # #         # Wyświetl tabelę
# # # #         st.write(filtered_other_df)

# # # #     with col1:
# # # #         # Wyświetl wykresy
# # # #         st.plotly_chart(fig_mm_s)
# # # #         st.plotly_chart(fig_obr_min)

# # # import streamlit as st
# # # import pandas as pd
# # # import plotly.express as px
# # # from google.cloud import bigquery
# # # from google.oauth2 import service_account
# # # import datetime
# # # import uuid

# # # def add_entry(area, line, machine, date, comment):
# # #     # Generowanie unikalnego id
# # #     new_id = str(uuid.uuid4())

# # #     # Tworzenie DataFrame z nowymi danymi
# # #     new_data = pd.DataFrame({
# # #         'areas': [area],
# # #         'lines': [line],
# # #         'level7': [machine],
# # #         'time': [date],
# # #         'KOMENTARZ': [comment],
# # #         'id': [new_id]
# # #     })

# # #     # Zapisywanie DataFrame do BigQuery
# # #     new_data['time'] = pd.to_datetime(new_data['time'])
# # #     dataset_id = 'kellogg'
# # #     table_id = 'kellog_set_3'
# # #     table_ref = client.dataset(dataset_id).table(table_id)
# # #     job = client.load_table_from_dataframe(new_data, table_ref, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
# # #     job.result()  # Czekaj na zakończenie operacji
# # #     st.success("Wpis został dodany.")

# # # def update_record_in_bigquery(record_id, updated_comment):
# # #     query = """
# # #         UPDATE kellogg.kellog_set_3
# # #         SET KOMENTARZ_ZWROTNY = @updated_comment
# # #         WHERE id = @record_id
# # #     """
# # #     job_config = bigquery.QueryJobConfig(
# # #         query_parameters=[
# # #             bigquery.ScalarQueryParameter("updated_comment", "STRING", updated_comment),
# # #             bigquery.ScalarQueryParameter("record_id", "STRING", record_id),
# # #         ]
# # #     )
# # #     client.query(query, job_config=job_config)

# # # def save_changes(rows_to_update):
# # #     for row in rows_to_update:
# # #         record_id = row.id
# # #         updated_comment = row.KOMENTARZ_ZWROTNY
# # #         update_record_in_bigquery(record_id, updated_comment)
# # #     st.success("Zmiany zostały zapisane.")

# # # def fetch_data_from_bigquery():
# # #     query = """
# # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # #         FROM kellogg.kellog_set_3
# # #         WHERE meas_id IS NULL
# # #         """
# # #     data_selection = client.query(query).to_dataframe()

# # #     # Usuń wiersze z brakującymi datami
# # #     data_selection = data_selection.dropna(subset=['time'])

# # #     return data_selection

# # # def fetch_other_data_from_bigquery_meas():
# # #     query_meas = """
# # #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# # #         FROM kellogg.kellog_set_3
# # #         """
# # #     data_selection_meas = client.query(query_meas).to_dataframe()

# # #     return data_selection_meas

# # # credentials = service_account.Credentials.from_service_account_file(r'icareolsztyn-d0b9397da7a5.json')

# # # project_id = 'icareolsztyn'
# # # client = bigquery.Client(credentials=credentials, project=project_id)
# # # st.set_page_config(layout="wide")

# # # st.title("VDExplorer 0.1")

# # # df = fetch_data_from_bigquery()

# # # # Przekształcenie kolumny "Data" na format daty
# # # df['time'] = pd.to_datetime(df['time']).dt.date

# # # # Dodawanie przejść do innych stron w sidebarze
# # # page_selection = st.sidebar.selectbox("Przejdź do:", ["Raporty", "Dane pomiarowe", "Trzecia strona"])
# # # selected_time_start = None
# # # selected_time_end = None
# # # date_range_start = None
# # # date_range_end = None

# # # if page_selection == "Raporty":
# # #     col0, col1, col2, col3, col4, col5 = st.columns(6)
# # #     with col0:
# # #         if 'selected_area_key' not in st.session_state:
# # #             st.session_state['selected_area_key'] = ""
# # #         # Wybór obszaru
# # #         selected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key=st.session_state['selected_area_key'])
# # #     with col1:
# # #         # Wybór obszaru
# # #         selected_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == selected_area, 'lines'].unique().tolist()) if selected_area else [""], key='selected_line_key')
# # #     with col2:
# # #         # Wybór maszyny
# # #         selected_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == selected_area) & (df['lines'] == selected_line), 'level7'].unique().tolist()) if selected_area and selected_line else [""], key='selected_machine_key')
# # #     with col3:
# # #         # Wybór statusu
# # #         status_values = [x for x in df['STATUS'].unique().tolist() if x is not None]
# # #         selected_status = st.selectbox("Wybierz status:", [""] + sorted(status_values), key='selected_status_key')
# # #     with col4:
# # #         # Wybór zakresu dat
# # #         date_range_start = st.date_input("Wybierz początek zakresu dat:", value=(date_range_start or df['time'].min()), key='date_range_start_key')
# # #     with col5:
# # #         # Wybór zakresu dat
# # #         date_range_end = st.date_input("Wybierz koniec zakresu dat:", value=(date_range_end or df['time'].max()), key='date_range_end_key')

# # #     def reset_filters():
# # #         st.session_state['selected_area_key'] = ""
# # #         st.session_state['selected_line_key'] = ""
# # #         st.session_state['selected_machine_key'] = ""
# # #         st.session_state['selected_status_key'] = ""
# # #         st.session_state['date_range_start_key'] = None
# # #         st.session_state['date_range_end_key'] = None

# # #     if st.button("Resetuj filtry"):
# # #         reset_filters()

# # #     filtered_df = df[
# # #         ((df['areas'] == selected_area) if selected_area else True) &
# # #         ((df['lines'] == selected_line) if selected_line else True) &
# # #         ((df['level7'] == selected_machine) if selected_machine else True) &
# # #         ((df['STATUS'] == selected_status) if selected_status else True) &
# # #         ((df['time'] >= date_range_start) if date_range_start else True) &
# # #         ((df['time'] <= date_range_end) if date_range_end else True)
# # #     ]

# # #     # Wyświetl tabelę raportów
# # #     st.experimental_data_editor(filtered_df)

# # #     # Wyświetl wykres kołowy dla STATUS
# # #     status_counts = filtered_df['STATUS'].value_counts()
# # #     fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Rozkład statusów')
# # #     st.plotly_chart(fig)

# # #     rows_to_update = []

# # #     for row in filtered_df.itertuples(index=False):
# # #         if getattr(row, "KOMENTARZ_ZWROTNY") != getattr(row, "KOMENTARZ_ZWROTNY", None):
# # #             rows_to_update.append(row)

# # #     if st.button("Zapisz"):
# # #         save_changes(rows_to_update)

# # #     # Dodaj ten kod w miejscu, gdzie chcesz, aby pojawił się expander do dodawania wpisów.
# # #     # W tym przypadku dodaję go zaraz po wykresie kołowym.

# # #     expander = st.expander("Dodaj wpis")
# # #     with expander:
# # #         # Dla wyboru obszaru
# # #         new_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key="new_area_select")

# # #         # Dla wyboru linii/podobszaru
# # #         new_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == new_area, 'lines'].unique().tolist()) if new_area else [""], key="new_line_select")

# # #         # Dla wyboru maszyny
# # #         new_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == new_area) & (df['lines'] == new_line), 'level7'].unique().tolist()) if new_area and new_line else [""], key="new_machine_select")

# # #         new_date = st.date_input("Wybierz datę:")
# # #         new_comment = st.text_input("Wpisz komentarz:")
# # #         if st.button("Dodaj wpis"):
# # #             add_entry(new_area, new_line, new_machine, new_date, new_comment)

# # # elif page_selection == "Dane pomiarowe":
# # #     # Kod dla strony "Dane pomiarowe"
# # #     # st.write("Tu będzie zawartość strony Dane pomiarowe")  # Usuwamy ten wiersz
# # #     st.markdown(
# # #         f'<iframe width="1400" height="1050" src="https://lookerstudio.google.com/embed/reporting/fe1fe97e-c903-4a68-9547-e070ff846367/page/p_74qqhk3h4c" frameborder="0" style="border:0" allowfullscreen></iframe>', 
# # #         unsafe_allow_html=True
# # #     )

# # # elif page_selection == "Trzecia strona":
# # #     other_df = fetch_other_data_from_bigquery_meas()

# # #     # Przekształcenie kolumny "time" na format daty
# # #     other_df['time'] = pd.to_datetime(other_df['time']).dt.date

# # #     # Filtruj dane na podstawie wybranych opcji
# # #     selected_level7 = st.selectbox("Wybierz level7:", [""] + sorted(other_df['level7'].unique().tolist()))
# # #     filtered_other_df = other_df[other_df['level7'] == selected_level7]

# # #     ten_years_ago = datetime.datetime.now() - datetime.timedelta(years=10)
# # #     selected_time_start = st.date_input("Wybierz początek zakresu Time:", value=(selected_time_start or filtered_other_df['time'].min()), min_value=ten_years_ago)
# # #     selected_time_end = st.date_input("Wybierz koniec zakresu Time:", value=(selected_time_end or filtered_other_df['time'].max()))

# # #     filtered_other_df = filtered_other_df[
# # #         (filtered_other_df['time'] >= selected_time_start) |
# # #         (selected_time_start is None)
# # #     ]
# # #     filtered_other_df = filtered_other_df[
# # #         (filtered_other_df['time'] <= selected_time_end) |
# # #         (selected_time_end is None)
# # #     ]

# # #     # Przekształcenie wartości "value" dla type_x = "obr/min"
# # #     filtered_other_df.loc[filtered_other_df['type_x'] == 'obr/min', 'value'] *= 60

# # #     # Dodaj wykres liniowy dla "value" (type_x: mm/s)
# # #     fig_mm_s = px.line(filtered_other_df[filtered_other_df['type_x'] == 'mm/s'], x="time", y="value", title='Wykres liniowy dla Value (mm/s)')
# # #     fig_mm_s.update_traces(mode='markers+lines', hovertemplate=None)
# # #     fig_mm_s.update_layout(hovermode='closest')
# # #     fig_mm_s.update_traces(textposition='top center')
# # #     fig_mm_s.update_traces(hovertemplate='Value: %{y}')
# # #     fig_mm_s.update_layout(
# # #         xaxis=dict(
# # #             rangeselector=dict(
# # #                 buttons=list([
# # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # #                     dict(step="all")
# # #                 ])
# # #             ),
# # #             rangeslider=dict(visible=True),
# # #             type="date"
# # #         )
# # #     )

# # #     # Dodaj wykres liniowy dla "value" (type_x: obr/min)
# # #     fig_obr_min = px.line(filtered_other_df[filtered_other_df['type_x'] == 'obr/min'], x="time", y="value", title='Wykres liniowy dla Value (obr/min)')
# # #     fig_obr_min.update_traces(mode='markers+lines', hovertemplate=None)
# # #     fig_obr_min.update_layout(hovermode='closest')
# # #     fig_obr_min.update_traces(textposition='top center')
# # #     fig_obr_min.update_traces(hovertemplate='Value: %{y}')
# # #     fig_obr_min.update_layout(
# # #         xaxis=dict(
# # #             rangeselector=dict(
# # #                 buttons=list([
# # #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# # #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# # #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# # #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# # #                     dict(step="all")
# # #                 ])
# # #             ),
# # #             rangeslider=dict(visible=True),
# # #             type="date"
# # #         )
# # #     )

# # #     col0, col1 = st.columns(2)
# # #     with col0:
# # #         # Wyświetl tabelę
# # #         st.write(filtered_other_df)

# # #     with col1:
# # #         # Wyświetl wykresy
# # #         st.plotly_chart(fig_mm_s)
# # #         st.plotly_chart(fig_obr_min)


# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # from google.cloud import bigquery
# # from google.oauth2 import service_account
# # import datetime
# # import uuid

# # def add_entry(area, line, machine, date, comment):
# #     # Generowanie unikalnego id
# #     new_id = str(uuid.uuid4())

# #     # Tworzenie DataFrame z nowymi danymi
# #     new_data = pd.DataFrame({
# #         'areas': [area],
# #         'lines': [line],
# #         'level7': [machine],
# #         'time': [date],
# #         'KOMENTARZ': [comment],
# #         'id': [new_id]
# #     })

# #     # Zapisywanie DataFrame do BigQuery
# #     new_data['time'] = pd.to_datetime(new_data['time'])
# #     dataset_id = 'kellogg'
# #     table_id = 'kellog_set_3'
# #     table_ref = client.dataset(dataset_id).table(table_id)
# #     job = client.load_table_from_dataframe(new_data, table_ref, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
# #     job.result()  # Czekaj na zakończenie operacji
# #     st.success("Wpis został dodany.")

# # credentials = service_account.Credentials.from_service_account_file(r'icareolsztyn-d0b9397da7a5.json')

# # project_id = 'icareolsztyn'
# # client = bigquery.Client(credentials=credentials, project=project_id)
# # st.set_page_config(layout="wide")

# # st.title("VDExplorer 0.1")

# # def fetch_data_from_bigquery():
# #     query = """
# #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# #         FROM kellogg.kellog_set_3
# #         WHERE meas_id IS NULL
# #         """
# #     data_selection = client.query(query).to_dataframe()

# #     # Usuń wiersze z brakującymi datami
# #     data_selection = data_selection.dropna(subset=['time'])

# #     return data_selection


# # def fetch_other_data_from_bigquery_meas():
# #     query_meas = """
# #         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
# #         FROM kellogg.kellog_set_3
# #         """
# #     data_selection_meas = client.query(query_meas).to_dataframe()

# #     return data_selection_meas

# # def update_record_in_bigquery(record_id, updated_comment):
# #     query = """
# #         UPDATE kellogg.kellog_set_3
# #         SET KOMENTARZ_ZWROTNY = @updated_comment
# #         WHERE id = @record_id
# #     """
# #     job_config = bigquery.QueryJobConfig(
# #         query_parameters=[
# #             bigquery.ScalarQueryParameter("updated_comment", "STRING", updated_comment),
# #             bigquery.ScalarQueryParameter("record_id", "STRING", record_id),
# #         ]
# #     )
# #     client.query(query, job_config=job_config)


# # def save_changes(rows_to_update):
# #     for row in rows_to_update:
# #         record_id = row.id
# #         updated_comment = row.KOMENTARZ_ZWROTNY
# #         update_record_in_bigquery(record_id, updated_comment)
# #     st.success("Zmiany zostały zapisane.")

# # df = fetch_data_from_bigquery()

# # # Przekształcenie kolumny "Data" na format daty
# # df['time'] = pd.to_datetime(df['time']).dt.date

# # # Dodawanie przejść do innych stron w sidebarze
# # page_selection = st.sidebar.selectbox("Przejdź do:", ["Raporty", "Dane pomiarowe", "Trzecia strona"])
# # selected_time_start = None
# # selected_time_end = None
# # date_range_start = None
# # date_range_end = None

# # if page_selection == "Raporty":
# #     col0, col1, col2, col3, col4 = st.columns(5)
# #     with col0:
# #         if 'selected_area_key' not in st.session_state:
# #             st.session_state['selected_area_key'] = ""
# #         # Wybór obszaru
# #         selected_area = st.sidebar.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key=st.session_state['selected_area_key'])
# #     with col1:
# #         # Wybór obszaru
# #         selected_line = st.sidebar.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == selected_area, 'lines'].unique().tolist()) if selected_area else [""], key='selected_line_key')
# #     with col2:
# #         # Wybór maszyny
# #         selected_machine = st.sidebar.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == selected_area) & (df['lines'] == selected_line), 'level7'].unique().tolist()) if selected_area and selected_line else [""], key='selected_machine_key')
# #     with col3:
# #         # Wybór statusu
# #         status_values = [x for x in df['STATUS'].unique().tolist() if x is not None]
# #         selected_status = st.sidebar.selectbox("Wybierz status:", [""] + sorted(status_values), key='selected_status_key')
# #     with col4:
# #         # Wybór zakresu dat
# #         date_range_start = st.sidebar.date_input("Wybierz początek zakresu dat:", value=(date_range_start or df['time'].min()), key='date_range_start_key')
# #         date_range_end = st.sidebar.date_input("Wybierz koniec zakresu dat:", value=(date_range_end or df['time'].max()), key='date_range_end_key')
# #         st.sidebar.button("Resetuj filtry", on_click=reset_filters)

# #     filtered_df = df[
# #         ((df['areas'] == selected_area) if selected_area else True) &
# #         ((df['lines'] == selected_line) if selected_line else True) &
# #         ((df['level7'] == selected_machine) if selected_machine else True) &
# #         ((df['STATUS'] == selected_status) if selected_status else True) &
# #         ((df['time'] >= date_range_start) if date_range_start else True) &
# #         ((df['time'] <= date_range_end) if date_range_end else True)
# #     ]

# #     # Wyświetl tabelę raportów
# #     st.experimental_data_editor(filtered_df)

# #     # Wyświetl wykres kołowy dla STATUS
# #     status_counts = filtered_df['STATUS'].value_counts()
# #     fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Rozkład statusów')
# #     st.plotly_chart(fig)

# #     rows_to_update = []

# #     for row in filtered_df.itertuples(index=False):
# #         if getattr(row, "KOMENTARZ_ZWROTNY") != getattr(row, "KOMENTARZ_ZWROTNY", None):
# #             rows_to_update.append(row)

# #     if st.button("Zapisz"):
# #         save_changes(rows_to_update)

# #     # Dodaj ten kod w miejscu, gdzie chcesz, aby pojawił się expander do dodawania wpisów.
# #     # W tym przypadku dodaję go zaraz po wykresie kołowym.

# #     expander = st.expander("Dodaj wpis")
# #     with expander:
# #         # Dla wyboru obszaru
# #         new_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key="new_area_select")

# #         # Dla wyboru linii/podobszaru
# #         new_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == new_area, 'lines'].unique().tolist()) if new_area else [""], key="new_line_select")

# #         # Dla wyboru maszyny
# #         new_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == new_area) & (df['lines'] == new_line), 'level7'].unique().tolist()) if new_area and new_line else [""], key="new_machine_select")

# #         new_date = st.date_input("Wybierz datę:")
# #         new_comment = st.text_input("Wpisz komentarz:")
# #         if st.button("Dodaj wpis"):
# #             add_entry(new_area, new_line, new_machine, new_date, new_comment)

# # elif page_selection == "Dane pomiarowe":
# #     # Kod dla strony "Dane pomiarowe"
# #     # st.write("Tu będzie zawartość strony Dane pomiarowe")  # Usuwamy ten wiersz
# #     st.markdown(
# #         f'<iframe width="1400" height="1050" src="https://lookerstudio.google.com/embed/reporting/fe1fe97e-c903-4a68-9547-e070ff846367/page/p_74qqhk3h4c" frameborder="0" style="border:0" allowfullscreen></iframe>', 
# #         unsafe_allow_html=True
# #     )

# # elif page_selection == "Trzecia strona":
# #     other_df = fetch_other_data_from_bigquery_meas()

# #     # Przekształcenie kolumny "time" na format daty
# #     other_df['time'] = pd.to_datetime(other_df['time']).dt.date

# #     # Filtruj dane na podstawie wybranych opcji
# #     selected_level7 = st.selectbox("Wybierz level7:", [""] + sorted(other_df['level7'].unique().tolist()))
# #     filtered_other_df = other_df[other_df['level7'] == selected_level7]

# #     ten_years_ago = datetime.datetime.now() - datetime.timedelta(years=10)
# #     selected_time_start = st.date_input("Wybierz początek zakresu Time:", value=(selected_time_start or filtered_other_df['time'].min()), min_value=ten_years_ago)
# #     selected_time_end = st.date_input("Wybierz koniec zakresu Time:", value=(selected_time_end or filtered_other_df['time'].max()))

# #     filtered_other_df = filtered_other_df[
# #         (filtered_other_df['time'] >= selected_time_start) |
# #         (selected_time_start is None)
# #     ]
# #     filtered_other_df = filtered_other_df[
# #         (filtered_other_df['time'] <= selected_time_end) |
# #         (selected_time_end is None)
# #     ]

# #     # Przekształcenie wartości "value" dla type_x = "obr/min"
# #     filtered_other_df.loc[filtered_other_df['type_x'] == 'obr/min', 'value'] *= 60

# #     # Dodaj wykres liniowy dla "value" (type_x: mm/s)
# #     fig_mm_s = px.line(filtered_other_df[filtered_other_df['type_x'] == 'mm/s'], x="time", y="value", title='Wykres liniowy dla Value (mm/s)')
# #     fig_mm_s.update_traces(mode='markers+lines', hovertemplate=None)
# #     fig_mm_s.update_layout(hovermode='closest')
# #     fig_mm_s.update_traces(textposition='top center')
# #     fig_mm_s.update_traces(hovertemplate='Value: %{y}')
# #     fig_mm_s.update_layout(
# #         xaxis=dict(
# #             rangeselector=dict(
# #                 buttons=list([
# #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# #                     dict(step="all")
# #                 ])
# #             ),
# #             rangeslider=dict(visible=True),
# #             type="date"
# #         )
# #     )

# #     # Dodaj wykres liniowy dla "value" (type_x: obr/min)
# #     fig_obr_min = px.line(filtered_other_df[filtered_other_df['type_x'] == 'obr/min'], x="time", y="value", title='Wykres liniowy dla Value (obr/min)')
# #     fig_obr_min.update_traces(mode='markers+lines', hovertemplate=None)
# #     fig_obr_min.update_layout(hovermode='closest')
# #     fig_obr_min.update_traces(textposition='top center')
# #     fig_obr_min.update_traces(hovertemplate='Value: %{y}')
# #     fig_obr_min.update_layout(
# #         xaxis=dict(
# #             rangeselector=dict(
# #                 buttons=list([
# #                     dict(count=1, label="1d", step="day", stepmode="backward"),
# #                     dict(count=7, label="1w", step="day", stepmode="backward"),
# #                     dict(count=1, label="1m", step="month", stepmode="backward"),
# #                     dict(count=6, label="6m", step="month", stepmode="backward"),
# #                     dict(step="all")
# #                 ])
# #             ),
# #             rangeslider=dict(visible=True),
# #             type="date"
# #         )
# #     )

# #     col0, col1 = st.columns(2)
# #     with col0:
# #         # Wyświetl tabelę
# #         st.write(filtered_other_df)

# #     with col1:
# #         # Wyświetl wykresy
# #         st.plotly_chart(fig_mm_s)
# #         st.plotly_chart(fig_obr_min)

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from google.cloud import bigquery
# from google.oauth2 import service_account
# import datetime
# import uuid

# def add_entry(area, line, machine, date, comment):
#     # Generowanie unikalnego id
#     new_id = str(uuid.uuid4())

#     # Tworzenie DataFrame z nowymi danymi
#     new_data = pd.DataFrame({
#         'areas': [area],
#         'lines': [line],
#         'level7': [machine],
#         'time': [date],
#         'KOMENTARZ': [comment],
#         'id': [new_id]
#     })

#     # Zapisywanie DataFrame do BigQuery
#     new_data['time'] = pd.to_datetime(new_data['time'])
#     dataset_id = 'kellogg'
#     table_id = 'kellog_set_3'
#     table_ref = client.dataset(dataset_id).table(table_id)
#     job = client.load_table_from_dataframe(new_data, table_ref, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
#     job.result()  # Czekaj na zakończenie operacji
#     st.success("Wpis został dodany.")

# def reset_filters():
#     st.session_state['selected_area_key'] = ""
#     st.session_state['selected_line_key'] = ""
#     st.session_state['selected_machine_key'] = ""
#     st.session_state['selected_status_key'] = ""
#     st.session_state['date_range_start_key'] = None
#     st.session_state['date_range_end_key'] = None

# credentials = service_account.Credentials.from_service_account_file(r'icareolsztyn-d0b9397da7a5.json')

# project_id = 'icareolsztyn'
# client = bigquery.Client(credentials=credentials, project=project_id)
# st.set_page_config(layout="wide")

# st.title("VDExplorer 0.1")

# def fetch_data_from_bigquery():
#     query = """
#         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
#         FROM kellogg.kellog_set_3
#         WHERE meas_id IS NULL
#         """
#     data_selection = client.query(query).to_dataframe()

#     # Usuń wiersze z brakującymi datami
#     data_selection = data_selection.dropna(subset=['time'])

#     return data_selection


# def fetch_other_data_from_bigquery_meas():
#     query_meas = """
#         SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
#         FROM kellogg.kellog_set_3
#         """
#     data_selection_meas = client.query(query_meas).to_dataframe()

#     return data_selection_meas

# def update_record_in_bigquery(record_id, updated_comment):
#     query = """
#         UPDATE kellogg.kellog_set_3
#         SET KOMENTARZ_ZWROTNY = @updated_comment
#         WHERE id = @record_id
#     """
#     job_config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter("updated_comment", "STRING", updated_comment),
#             bigquery.ScalarQueryParameter("record_id", "STRING", record_id),
#         ]
#     )
#     client.query(query, job_config=job_config)


# def save_changes(rows_to_update):
#     for row in rows_to_update:
#         record_id = row.id
#         updated_comment = row.KOMENTARZ_ZWROTNY
#         update_record_in_bigquery(record_id, updated_comment)
#     st.success("Zmiany zostały zapisane.")

# df = fetch_data_from_bigquery()

# # Przekształcenie kolumny "Data" na format daty
# df['time'] = pd.to_datetime(df['time']).dt.date

# # Dodawanie przejść do innych stron w sidebarze
# page_selection = st.sidebar.selectbox("Przejdź do:", ["Raporty", "Dane pomiarowe", "Trzecia strona"])
# selected_time_start = None
# selected_time_end = None
# date_range_start = None
# date_range_end = None

# if page_selection == "Raporty":
#     col0, col1, col2, col3, col4, col5 = st.columns(6)
#     with col0:
#         if 'selected_area_key' not in st.session_state:
#             st.session_state['selected_area_key'] = ""
#         # Wybór obszaru
#         selected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key=st.session_state['selected_area_key'])
#     with col1:
#         # Wybór obszaru
#         selected_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == selected_area, 'lines'].unique().tolist()) if selected_area else [""], key='selected_line_key')
#     with col2:
#         # Wybór maszyny
#         selected_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == selected_area) & (df['lines'] == selected_line), 'level7'].unique().tolist()) if selected_area and selected_line else [""], key='selected_machine_key')
#     with col3:
#         # Wybór statusu
#         status_values = [x for x in df['STATUS'].unique().tolist() if x is not None]
#         selected_status = st.selectbox("Wybierz status:", [""] + sorted(status_values), key='selected_status_key')
#     with col4:
#         # Wybór zakresu dat
#         date_range_start = st.date_input("Wybierz początek zakresu dat:", value=(date_range_start or df['time'].min()), key='date_range_start_key')
#     with col5:
#         # Wybór zakresu dat
#         date_range_end = st.date_input("Wybierz koniec zakresu dat:", value=(date_range_end or df['time'].max()), key='date_range_end_key')

#     filtered_df = df[
#         ((df['areas'] == selected_area) if selected_area else True) &
#         ((df['lines'] == selected_line) if selected_line else True) &
#         ((df['level7'] == selected_machine) if selected_machine else True) &
#         ((df['STATUS'] == selected_status) if selected_status else True) &
#         ((df['time'] >= date_range_start) if date_range_start else True) &
#         ((df['time'] <= date_range_end) if date_range_end else True)
#     ]

#     # Wyświetl tabelę raportów
#     st.experimental_data_editor(filtered_df)


#     # Dodaj ten kod w miejscu, gdzie chcesz, aby pojawił się expander do dodawania wpisów.
#     # W tym przypadku dodaję go zaraz po wykresie kołowym.
#     col0, col1 = st.columns(2)
#     with col0:
#             # Wyświetl wykres kołowy dla STATUS
#         status_counts = filtered_df['STATUS'].value_counts()
#         fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Rozkład statusów')
#         st.plotly_chart(fig)
        
#     with col1:
#         expander = st.expander("Dodaj wpis")
#         with expander:
#             # Dla wyboru obszaru
#             new_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key="new_area_select")

#             # Dla wyboru linii/podobszaru
#             new_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == new_area, 'lines'].unique().tolist()) if new_area else [""], key="new_line_select")

#             # Dla wyboru maszyny
#             new_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == new_area) & (df['lines'] == new_line), 'level7'].unique().tolist()) if new_area and new_line else [""], key="new_machine_select")

#             new_date = st.date_input("Wybierz datę:")
#             new_comment = st.text_input("Wpisz komentarz:")
#             if st.button("Dodaj wpis"):
#                 add_entry(new_area, new_line, new_machine, new_date, new_comment)

# elif page_selection == "Dane pomiarowe":
#     # Kod dla strony "Dane pomiarowe"
#     # st.write("Tu będzie zawartość strony Dane pomiarowe")  # Usuwamy ten wiersz
#     st.markdown(
#         f'<iframe width="1400" height="1050" src="https://lookerstudio.google.com/embed/reporting/fe1fe97e-c903-4a68-9547-e070ff846367/page/p_74qqhk3h4c" frameborder="0" style="border:0" allowfullscreen></iframe>', 
#         unsafe_allow_html=True
#     )

# elif page_selection == "Trzecia strona":
#     other_df = fetch_other_data_from_bigquery_meas()

#     # Przekształcenie kolumny "time" na format daty
#     other_df['time'] = pd.to_datetime(other_df['time']).dt.date

#     # Filtruj dane na podstawie wybranych opcji
#     selected_level7 = st.selectbox("Wybierz level7:", [""] + sorted(other_df['level7'].unique().tolist()))
#     filtered_other_df = other_df[other_df['level7'] == selected_level7]

#     ten_years_ago = datetime.datetime.now() - datetime.timedelta(years=10)
#     selected_time_start = st.date_input("Wybierz początek zakresu Time:", value=(selected_time_start or filtered_other_df['time'].min()), min_value=ten_years_ago)
#     selected_time_end = st.date_input("Wybierz koniec zakresu Time:", value=(selected_time_end or filtered_other_df['time'].max()))

#     filtered_other_df = filtered_other_df[
#         (filtered_other_df['time'] >= selected_time_start) |
#         (selected_time_start is None)
#     ]
#     filtered_other_df = filtered_other_df[
#         (filtered_other_df['time'] <= selected_time_end) |
#         (selected_time_end is None)
#     ]

#     # Przekształcenie wartości "value" dla type_x = "obr/min"
#     filtered_other_df.loc[filtered_other_df['type_x'] == 'obr/min', 'value'] *= 60

#     # Dodaj wykres liniowy dla "value" (type_x: mm/s)
#     fig_mm_s = px.line(filtered_other_df[filtered_other_df['type_x'] == 'mm/s'], x="time", y="value", title='Wykres liniowy dla Value (mm/s)')
#     fig_mm_s.update_traces(mode='markers+lines', hovertemplate=None)
#     fig_mm_s.update_layout(hovermode='closest')
#     fig_mm_s.update_traces(textposition='top center')
#     fig_mm_s.update_traces(hovertemplate='Value: %{y}')
#     fig_mm_s.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1, label="1d", step="day", stepmode="backward"),
#                     dict(count=7, label="1w", step="day", stepmode="backward"),
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(visible=True),
#             type="date"
#         )
#     )

#     # Dodaj wykres liniowy dla "value" (type_x: obr/min)
#     fig_obr_min = px.line(filtered_other_df[filtered_other_df['type_x'] == 'obr/min'], x="time", y="value", title='Wykres liniowy dla Value (obr/min)')
#     fig_obr_min.update_traces(mode='markers+lines', hovertemplate=None)
#     fig_obr_min.update_layout(hovermode='closest')
#     fig_obr_min.update_traces(textposition='top center')
#     fig_obr_min.update_traces(hovertemplate='Value: %{y}')
#     fig_obr_min.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1, label="1d", step="day", stepmode="backward"),
#                     dict(count=7, label="1w", step="day", stepmode="backward"),
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(visible=True),
#             type="date"
#         )
#     )

#     col0, col1 = st.columns(2)
#     with col0:
#         # Wyświetl tabelę
#         st.write(filtered_other_df)

#     with col1:
#         # Wyświetl wykresy
#         st.plotly_chart(fig_mm_s)
#         st.plotly_chart(fig_obr_min)


import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery
from google.oauth2 import service_account
import datetime
import uuid
from dateutil.relativedelta import relativedelta


def add_entry(area, line, machine, date, comment):
    # Generowanie unikalnego id
    new_id = str(uuid.uuid4())

    # Tworzenie DataFrame z nowymi danymi
    new_data = pd.DataFrame({
        'areas': [area],
        'lines': [line],
        'level7': [machine],
        'time': [date],
        'KOMENTARZ': [comment],
        'id': [new_id]
    })

    # Zapisywanie DataFrame do BigQuery
    new_data['time'] = pd.to_datetime(new_data['time'])
    dataset_id = 'kellogg'
    table_id = 'kellog_set_3'
    table_ref = client.dataset(dataset_id).table(table_id)
    job = client.load_table_from_dataframe(new_data, table_ref, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
    job.result()  # Czekaj na zakończenie operacji
    st.success("Wpis został dodany.")

def reset_filters():
    st.session_state['selected_area_key'] = ""
    st.session_state['selected_line_key'] = ""
    st.session_state['selected_machine_key'] = ""
    st.session_state['selected_status_key'] = ""
    st.session_state['date_range_start_key'] = None
    st.session_state['date_range_end_key'] = None

credentials = service_account.Credentials.from_service_account_file(r'icareolsztyn-d0b9397da7a5.json')

project_id = 'icareolsztyn'
client = bigquery.Client(credentials=credentials, project=project_id)
st.set_page_config(layout="wide")

st.title("VDExplorer 0.1")

def fetch_data_from_bigquery():
    query = """
        SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
        FROM kellogg.kellog_set_3
        WHERE meas_id IS NULL
        """
    data_selection = client.query(query).to_dataframe()

    # Usuń wiersze z brakującymi datami
    data_selection = data_selection.dropna(subset=['time'])

    return data_selection


def fetch_other_data_from_bigquery_meas():
    query_meas = """
        SELECT meas_id, type_x, value, time, level7, name, areas, lines, STATUS_NB, STATUS, KOMENTARZ, ELEMENT, KOMENTARZ_ZWROTNY, id
        FROM kellogg.kellog_set_3
        """
    data_selection_meas = client.query(query_meas).to_dataframe()

    return data_selection_meas

def update_record_in_bigquery(record_id, updated_comment):
    query = """
        UPDATE kellogg.kellog_set_3
        SET KOMENTARZ_ZWROTNY = @updated_comment
        WHERE id = @record_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("updated_comment", "STRING", updated_comment),
            bigquery.ScalarQueryParameter("record_id", "STRING", record_id),
        ]
    )
    client.query(query, job_config=job_config)


def save_changes(rows_to_update):
    for row in rows_to_update:
        record_id = row.id
        updated_comment = row.KOMENTARZ_ZWROTNY
        update_record_in_bigquery(record_id, updated_comment)
    st.success("Zmiany zostały zapisane.")

df = fetch_data_from_bigquery()

# Przekształcenie kolumny "Data" na format daty
df['time'] = pd.to_datetime(df['time']).dt.date

# Dodawanie przejść do innych stron w sidebarze
page_selection = st.sidebar.selectbox("Przejdź do:", ["Raporty", "Dane pomiarowe"])
selected_time_start = None
selected_time_end = None
date_range_start = None
date_range_end = None

if page_selection == "Raporty":
    col0, col1, col2, col3, col4, col5 = st.columns(6)
    with col0:
        if 'selected_area_key' not in st.session_state:
            st.session_state['selected_area_key'] = ""
        # Wybór obszaru
        selected_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key=st.session_state['selected_area_key'])
    with col1:
        # Wybór obszaru
        selected_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == selected_area, 'lines'].unique().tolist()) if selected_area else [""], key='selected_line_key')
    with col2:
        # Wybór maszyny
        selected_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == selected_area) & (df['lines'] == selected_line), 'level7'].unique().tolist()) if selected_area and selected_line else [""], key='selected_machine_key')
    with col3:
        # Wybór statusu
        status_values = [x for x in df['STATUS'].unique().tolist() if x is not None]
        selected_status = st.selectbox("Wybierz status:", [""] + sorted(status_values), key='selected_status_key')
    with col4:
        # Wybór zakresu dat
        date_range_start = st.date_input("Wybierz początek zakresu dat:", value=(date_range_start or df['time'].min()), key='date_range_start_key')
    with col5:
        # Wybór zakresu dat
        date_range_end = st.date_input("Wybierz koniec zakresu dat:", value=(date_range_end or df['time'].max()), key='date_range_end_key')

    filtered_df = df[
        ((df['areas'] == selected_area) if selected_area else True) &
        ((df['lines'] == selected_line) if selected_line else True) &
        ((df['level7'] == selected_machine) if selected_machine else True) &
        ((df['STATUS'] == selected_status) if selected_status else True) &
        ((df['time'] >= date_range_start) if date_range_start else True) &
        ((df['time'] <= date_range_end) if date_range_end else True)
    ]

    # Wyświetl tabelę raportów
    st.experimental_data_editor(filtered_df)

    # Dodaj przycisk resetujący filtry do sidebaru
    reset_button_key = "reset_filters"
    if st.sidebar.button("Resetuj filtry", key=reset_button_key):
        reset_filters()

    # Dodaj ten kod w miejscu, gdzie chcesz, aby pojawił się expander do dodawania wpisów.
    # W tym przypadku dodaję go zaraz po wykresie kołowym.
    col0, col1 = st.columns(2)
    with col0:
            # Wyświetl wykres kołowy dla STATUS
        status_counts = filtered_df['STATUS'].value_counts()
        fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Rozkład statusów')
        st.plotly_chart(fig)
        
    with col1:
        expander = st.expander("Dodaj wpis")
        with expander:
            # Dla wyboru obszaru
            new_area = st.selectbox("Wybierz obszar:", [""] + sorted(df['areas'].unique().tolist()), key="new_area_select")

            # Dla wyboru linii/podobszaru
            new_line = st.selectbox("Wybierz linię/podobszar:", [""] + sorted(df.loc[df['areas'] == new_area, 'lines'].unique().tolist()) if new_area else [""], key="new_line_select")

            # Dla wyboru maszyny
            new_machine = st.selectbox("Wybierz maszynę:", [""] + sorted(df.loc[(df['areas'] == new_area) & (df['lines'] == new_line), 'level7'].unique().tolist()) if new_area and new_line else [""], key="new_machine_select")

            new_date = st.date_input("Wybierz datę:")
            new_comment = st.text_input("Wpisz komentarz:")
            if st.button("Dodaj wpis"):
                add_entry(new_area, new_line, new_machine, new_date, new_comment)

elif page_selection == "Dane pomiarowe":
    # Kod dla strony "Dane pomiarowe"
    # st.write("Tu będzie zawartość strony Dane pomiarowe")  # Usuwamy ten wiersz
    st.markdown(
        f'<iframe width="1400" height="1050" src="https://lookerstudio.google.com/embed/reporting/fe1fe97e-c903-4a68-9547-e070ff846367/page/p_74qqhk3h4c" frameborder="0" style="border:0" allowfullscreen></iframe>', 
        unsafe_allow_html=True
    )

# elif page_selection == "Trzecia strona":
#     other_df = fetch_other_data_from_bigquery_meas()

#     # Przekształcenie kolumny "time" na format daty
#     other_df['time'] = pd.to_datetime(other_df['time']).dt.date

#     # Filtruj dane na podstawie wybranych opcji
#     selected_level7 = st.selectbox("Wybierz level7:", [""] + sorted(other_df['level7'].unique().tolist()))
#     filtered_other_df = other_df[other_df['level7'] == selected_level7]

#     ten_years_ago = datetime.datetime.now() - relativedelta(years=10)
#     selected_time_start = st.date_input("Wybierz początek zakresu Time:", value=(selected_time_start or filtered_other_df['time'].min()), min_value=ten_years_ago.date() if ten_years_ago else None)
#     selected_time_end = st.date_input("Wybierz koniec zakresu Time:", value=(selected_time_end or filtered_other_df['time'].max()), min_value=ten_years_ago.date() if ten_years_ago else None)


#     filtered_other_df = filtered_other_df[
#         (filtered_other_df['time'] >= selected_time_start) |
#         (selected_time_start is None)
#     ]
#     filtered_other_df = filtered_other_df[
#         (filtered_other_df['time'] <= selected_time_end) |
#         (selected_time_end is None)
#     ]

#     # Przekształcenie wartości "value" dla type_x = "obr/min"
#     filtered_other_df.loc[filtered_other_df['type_x'] == 'obr/min', 'value'] *= 60

#     # Dodaj wykres liniowy dla "value" (type_x: mm/s)
#     fig_mm_s = px.line(filtered_other_df[filtered_other_df['type_x'] == 'mm/s'], x="time", y="value", title='Wykres liniowy dla Value (mm/s)')
#     fig_mm_s.update_traces(mode='markers+lines', hovertemplate=None)
#     fig_mm_s.update_layout(hovermode='closest')
#     fig_mm_s.update_traces(textposition='top center')
#     fig_mm_s.update_traces(hovertemplate='Value: %{y}')
#     fig_mm_s.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1, label="1d", step="day", stepmode="backward"),
#                     dict(count=7, label="1w", step="day", stepmode="backward"),
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(visible=True),
#             type="date"
#         )
#     )

#     # Dodaj wykres liniowy dla "value" (type_x: obr/min)
#     fig_obr_min = px.line(filtered_other_df[filtered_other_df['type_x'] == 'obr/min'], x="time", y="value", title='Wykres liniowy dla Value (obr/min)')
#     fig_obr_min.update_traces(mode='markers+lines', hovertemplate=None)
#     fig_obr_min.update_layout(hovermode='closest')
#     fig_obr_min.update_traces(textposition='top center')
#     fig_obr_min.update_traces(hovertemplate='Value: %{y}')
#     fig_obr_min.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1, label="1d", step="day", stepmode="backward"),
#                     dict(count=7, label="1w", step="day", stepmode="backward"),
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(visible=True),
#             type="date"
#         )
#     )

#     col0, col1 = st.columns(2)
#     with col0:
#         # Wyświetl tabelę
#         st.write(filtered_other_df)

#     with col1:
#         # Wyświetl wykresy
#         st.plotly_chart(fig_mm_s)
#         st.plotly_chart(fig_obr_min)
# ##############################################