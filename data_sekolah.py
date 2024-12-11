import streamlit as st
st.set_page_config(
    page_title='Sekolah Anak Shalih',
    layout="centered")

conn = st.connection('mysql', type='sql' )

from Identitas_siswa.data_umum_siswa import data_umum
from Identitas_siswa.statistik import statistik
from Identitas_siswa.pembayaran import pembayaran


def intro():
    import streamlit as st

    st.write("# YPI Imam Ahmad bin Hanbal ")
    st.sidebar.success("Pilih Kategori data")

    st.markdown(
        """
        ### Data Warehouse Project 
          
        Tahap 1 (1.0)

        - Data Identitas Siswa
        - Pembayaran
    """
    )



def data_siswa():
    st.write("# Data Umum Siswa")

    sub_kategori ={
        "data umum siswa":data_umum,
        "statistik siswa":statistik,
        
       
        }
    sub_kat = st.sidebar.selectbox ("sub kategori",sub_kategori.keys())
    sub_kategori[sub_kat]()

page_names_to_funcs = {
    "-":intro,
    "Data siswa":data_siswa
    }
kategori = st.sidebar.selectbox("pilih kategori", page_names_to_funcs.keys())
page_names_to_funcs[kategori]()





