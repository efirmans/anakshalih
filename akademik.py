import streamlit as st
import pandas as pd

conn = st.experimental_connection('mysql', type='sql' )

def akademik():
    
    st.write("# Data Akademik")
    sub_kategori ={"wali kelas":wali_kelas,"penilaian siswa":penilaian}
    sub_kat = st.sidebar.selectbox('sub kategori', sub_kategori.keys())
    sub_kategori[sub_kat]()

def wali_kelas():
    st.text("wali kelas")
    
    walas = conn.query (F"call walas")
    walas.index +=1
    walas.index.rename('No', inplace=True)
    
    st.write(walas)

def penilaian():
    st.text("penilaian")
