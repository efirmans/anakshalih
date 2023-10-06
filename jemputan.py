import streamlit as st
import pandas as pd
import xlsxwriter


conn = st.experimental_connection('mysql', type='sql' )

def jemputan():
    
    st.header ("Data Jemputan")
    tab1,tab2,tab3 = st.tabs(['peserta','rute', 'kendaraan'])

    with tab1:
        peserta_jemput()

    with tab2:
        rute_jemput()

    with tab3:
        data_kendaraan()


def peserta_jemput():
    st.text('Peserta jemputan')
    cari = st.text_input('input nama peserta jemputan')
    peserta = conn.query(F"call peserta_jemput(  '{cari}') ")
    peserta.index +=1
    peserta.index.rename('No', inplace=True)
    df = peserta
    
    st.write(df)

def rute_jemput():
    st.text('rute jemputan')
    pilih_rute = st.selectbox("pilih rute",
    (conn.query(F"select no_rute FROM rute ") ))
    sopir = conn.query(F"call driver('{pilih_rute}') ")
    df=pd.DataFrame(sopir)
    ubah = df.values.tolist()
    satu = str(ubah).replace("[['","") 

    st.write('nama sopir: '+ str(satu).replace("']]",""))

    rut_jem = conn.query(F"call rute_jemputan(  '{pilih_rute}') ") 
    df = rut_jem
    df.index +=1
    df.index.rename('No', inplace=True)
    st.write(df)
    
    
def data_kendaraan():
    st.text('data kendaraan')
   
    
    mobil = conn.query(F"select * FROM kendaraan ") 
    df=pd.DataFrame(mobil)
    df.drop(columns=["no_polisi"])
    df.index +=1
    df.index.rename('No', inplace=True)
    
    df1=df.drop(columns=['id_kendaraan'])  
    
         
    st.write(df1)
    for column_headers in df.columns: 
        st.write(column_headers)
    

