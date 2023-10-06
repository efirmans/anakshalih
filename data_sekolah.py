import streamlit as st
from siswa import * 
from akademik import *
from jemputan import *
from dana_pendidikan import *

conn = st.experimental_connection('mysql', type='sql' )

def intro():
    import streamlit as st

    st.write("# YPI Imam Ahmad bin Hanbal ")
    st.sidebar.success("Pilih Kategori data")

    st.markdown(
        """
        Data Warehouse Project mencakup 

        - Data umum siswa
        - Data Pembayaran Pendidikan
        - Data Akademik
        - Data Jemputan
        - Data UKS
        - Data perpustakaan
          
        ### Tahap awal

        - Data Umum Siswa , Pembayaran pendidikan , dan  Jemputan (Agustus - September 2023)
        - Data Akademik (Oktober-November 2023)
        - Data Perpustakaan, UKS (Oktober- Desember 2023)
        
    """
    )



page_names_to_funcs = {
    "-":intro,
    "Data siswa":data_siswa,
    "Jemputan":jemputan,
    "Biaya Pendidikan" :biaya_pendidikan,
    "Akademik": akademik ,
    }

kategori = st.sidebar.selectbox("pilih kategori", page_names_to_funcs.keys())
page_names_to_funcs[kategori]()





