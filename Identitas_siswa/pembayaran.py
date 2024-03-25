import streamlit as st
import pandas as pd
import altair as alt

from .tunggakan import nunggak

conn = st.connection('mysql', type='sql' )
historisBayar = conn.query ("SELECT * from tagihan_per_siswa")

def pembayaran():
    
    sub_kategori ={
        
        "histori pembayaran":histori,
        "tunggakan":nunggak
             }
    sub_kat = st.sidebar.selectbox('sub kategori', sub_kategori.keys())
    sub_kategori[sub_kat]()

def histori():
    st.text('histori pembayaran')

    df = pd.DataFrame(historisBayar)
    thn_ajaran = df['tahun ajaran'].unique().tolist()
    kategori_tagihan = df['kategori'].unique().tolist()
    mas
    col1,col2= st.columns(2)
    with col1:
        pilih_ta = st.selectbox('pilih tahun ajaran', thn_ajaran)
    with col2:
        kategori = st.selectbox('kategori tagihan',  kategori_tagihan,)
    
            # jenis_tagihan = df[(df['kategori'] == kategori) & (df['tahun ajaran'] == pilih_ta)]['tagihan'].drop_duplicates().tolist()
            
    cari_nis = st.text_input('input nis',max_chars=10)
    df2 = df[(df['kategori'] == kategori) & (df['tahun ajaran'] == pilih_ta) 
             & (df['nis'] == cari_nis)]

    if cari_nis =='':
        pass
    else:
        nama =  df2['nama siswa'].drop_duplicates().to_string(index=False)
        nis =  df2['nis'].drop_duplicates().to_string(index=False)
        st.write(f'Nama : {nama}  \n NIS: {nis}')
       
        st.dataframe(df2[['tagihan','total','terbayarkan','kekurangan', 'tgl bayar']],hide_index=True,use_container_width=True)




