import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import time


conn = st.connection('mysql', type='sql' )
hasil = conn.query("select * from duplikasi_data")

engine = create_engine("mysql+pymysql://efirmans:#YPIIAh2023#@192.168.1.199:3306/data_warehouse") 
# Initialize session state for button visibility if it doesn't exist


def update():
    st.header('update data')
    tab1,tab2 = st.tabs(['upload','delete duplicate'])
    with tab1:
        upload()

    with tab2:
        st.header('hapus duplikasi data')
        @st.cache_data
        def load_data():
            with engine.connect() as con:
                result = con.execute(text("select * from duplikasi_data"))
                return pd.DataFrame(result.fetchall(), columns=result.keys())

        # Display the button to refresh data
        if st.button('Refresh Data'):
            # Clear the cache
            st.cache_data.clear()
            # Re-load the data
            df = load_data()
            st.table(df)
        else:
            # Load cached data
            df = load_data()
            st.table(df)

        # Button to delete duplicates
        hapus = st.button('Hapus Duplikat')
        if hapus:
            with engine.connect() as connn:
                connn.execute(text("CALL hapus_data()"))
                connn.commit()
            st.cache_data.clear()  # Clear the cache after deleting
            st.success('Duplikasi data sudah dihapus')


def upload():
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    uploaded_file = st.file_uploader("pilih file"   )
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        df = pd.DataFrame(dataframe)
        st.dataframe(df)

        # Only show the button if it hasn't been clicked yet
        if not st.session_state.button_clicked:
            tombol = st.button('upload')
            if tombol:
                df.to_sql('dana_pendidikan', con=engine, index=False, if_exists='append')
                progress_text = "tunggu ya!, lagi di-proses."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()
                st.session_state.button_clicked = True  # Update the button state

    # Optionally, you can provide a way to reset the button state
    if st.session_state.button_clicked:
        st.success('Data sudah di-upload.')
        if st.button('Reset'):
            st.session_state.button_clicked = False
            


