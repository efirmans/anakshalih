import streamlit as st
import pandas as pd
import numpy as np
from dana_pendidikan import convert_df

conn = st.experimental_connection('mysql', type='sql' )
ta= conn.query(F"select thn_ajaran as ta FROM thn_ajaran order by ta desc")
unit= conn.query(F"select nama_unit  FROM unit_pendidikan ")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def data_siswa():
    st.write("# Data Siswa")

    sub_kategori ={
        "data umum siswa":data_umum,
        "statistik siswa":statistiK_siswa,
        "data keluarga siswa":data_keluarga,
        }
    sub_kat = st.sidebar.selectbox ("sub kategori",sub_kategori.keys())
    sub_kategori[sub_kat]()

def data_umum():
    tab1,tab2,tab3 = st.tabs(['pencarian','historis','alamat'])
    with tab1:
        st.header('Pencarian  siswa')
        identitas_siswa()
    
    with tab2:
        st.header('historis siswa')
        siswa_ta()

    with tab3:
        st.header('alamat siswa per kelurahan')
        alamat()

def identitas_siswa():
    
    col1,col2 = st.columns(2)
    with col1:
        pilih_ta = st.selectbox('tahun ajaran', (ta))

    add_radio = st.radio(
            "cari siswa berdasarkan ",
            ("nama siswa", "NIS", "nama orang tua"),horizontal=True
        )
    
    if add_radio == "nama siswa":
        
        cari_siswa = st.text_input('ketik nama siswa',max_chars=40,)

        nama_siswa = conn.query(F"call cari_siswa(  '{cari_siswa}','{pilih_ta}') ")
        df = pd.DataFrame(nama_siswa)
        if cari_siswa == '':
            st.info('silakan input nama_siswa')
        else:
            df.index +=1
            df.index.rename('No', inplace=True)
            st.dataframe(df)

    elif add_radio == "NIS":
        cari_NIS = st.text_input('ketik NIS',max_chars=10)
        NIS  = conn.query(F"call NIS('{cari_NIS}','{pilih_ta}') ") 
        if cari_NIS =='':
            st.info('silakan input NIS')
        else:
            df = pd.DataFrame(NIS)
            hasil = df.T
            st.table(hasil)
        
    else:
        cari_ortu = st.text_input('ketik nama ortu',max_chars=40)
        ayah_ibu = conn.query(F"call cari_ortu( '{cari_ortu}','{pilih_ta}')  " )
        if cari_ortu == '':
            st.info('silakan input nama ortu')
        else:
            df = ayah_ibu
            df.index +=1
            df.index.rename('No', inplace=True)
            st.dataframe(df)

def siswa_ta():  
    st.text("tahun ajaran")
    cari = st.text_input('input NIS',max_chars=10)
    NIS  = conn.query(F"call nis_ta('{cari}') ") 
    df = pd.DataFrame(NIS)
    df.index +=1
    df.index.rename('No',inplace=True)
    if cari=='':
        st.info('silahkan input nis')
    else:
        st.write(df[['tahun ajaran','kelas']])
        nama = df['Nama siswa'].drop_duplicates()
        st.text('nama siswa: ' + nama.values)

def alamat():
    st.text("Alamat")
    pilih_ta = st.selectbox('pilih tahun ajaran', (ta))    
    Col1, Col2 = st.columns(2)
    with Col1:
        kab_kota = conn.query(F"SELECT DISTINCT `Kab./Kota` from siswa WHERE `Kab./Kota` != ''  ")
        pilih_kota = st.selectbox('pilik kab/kota', (kab_kota))
    with Col2:
        kelurahan =  conn.query(F"SELECT DISTINCT kelurahan from siswa WHERE `Kab./Kota` = '{pilih_kota}' ")
        pilih_lurah = st.selectbox('pilik kab/kota', (kelurahan))
    
    kelurahan_mana  = conn.query(F"call alamat('{pilih_ta}','{pilih_kota}','{pilih_lurah}' ) ") 
    df =pd.DataFrame(kelurahan_mana)
    df.index +=1
    df.index.rename('No', inplace=True)
    st.write(df)

def statistiK_siswa():
    import streamlit as st
    st.text("statistik siswa")    
    tab1, tab2, tab3,tab4 = st.tabs(["per kelas", "per jenjang kelas", "jumlah kumulatif", "siswa pindah"])

    with tab1:
        st.header("Siswa per kelas")
        siswa_per_kelas()

    with tab2:
        st.header("Siswa per jenjang kelas")
        jenjang_siswa()
    
    with tab3:
        st.header("jumlah kumulatif")
        siswa_per_unit()

    with tab4:
        st.header("siswa pindah keluar")
        siswa_pindah()

def siswa_per_kelas():
    col1,col2 =st.columns(2)
    with col1:
        pilih_ta = st.selectbox( 'tahun ajaran',(ta))
    with col2:
        kelas = conn.query(F"select nama_kelas from kelas order by id_kelas")
        pilih_kelas = st.selectbox('pilih kelas', (kelas))
     
    cari_kelas  = conn.query(F"call cari_kelas('{pilih_ta}', '{pilih_kelas}') ") 
    cari_kelas.index +=1
    cari_kelas.index.rename('No', inplace=True)
    df= cari_kelas

    st.write(df)
    st.text('jumlah siswa: '+ str( len(df)))
    #jumlah row

    csv = convert_df(cari_kelas)
    st.download_button(
    label="download",
    data= csv,
    file_name="siswa per kelas.csv",
    mime="text/csv"
    )   

def jenjang_siswa():    
    pilih_ta = st.selectbox( 'tahun ',(ta))
    col1,col2 = st.columns(2)
    with col1:
        pilih_unit =st.selectbox('unit',(unit))
    with col2:
        if pilih_unit == 'SDIT':
            SDIT = conn.query(F"select DISTINCT jenjang from kelas where nama_kelas not like   'TK%' and nama_kelas not like   'KB%'")
            pilih_jenjang = st.selectbox('jenjang kelas',(SDIT))
        else:
            TKIT = conn.query(F"select DISTINCT jenjang from kelas where nama_kelas like 'TK%' or nama_kelas like 'KB%'")
            pilih_jenjang = st.selectbox('jenjang kelas',(TKIT))
        
    jenjang = conn.query(F"call jenjang_siswa('{pilih_ta}','{pilih_unit}','{pilih_jenjang}')  " ) 
    jenjang.index +=1
    jenjang.index.rename('No', inplace=True)
    st.write(jenjang)
    st.text('jumlah siswa: '+ str(len(jenjang.index )))
    
    csv = convert_df(jenjang)
    st.download_button(
    label="download",
    data= csv,
    file_name="siswa per jenjang.csv",
    mime="text/csv"
    )   

def siswa_per_unit():
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        pilih_ta = st.selectbox('pilih tahun ajaran', (ta))
        
    jmlh  = conn.query(F"call jml_siswa('{pilih_ta}') ") 
    df = pd.DataFrame(jmlh)
    df.loc[len(df.index)] = ['TOTAL',df['jumlah siswa'].sum(numeric_only=True)]  
    # df.loc['total'] = pd.Series(df.sum(numeric_only=True) )
    st.dataframe(df,hide_index=True)
    
    jmlh_perkelas  = conn.query(F"call siswa_unit_kelas('{pilih_ta}') ")
    jmlh_perkelas.index +=1
    jmlh_perkelas.index.rename('No', inplace=True)
    df = pd.DataFrame(jmlh_perkelas)
    st.write(df)
        
def siswa_pindah():
    pindah  = conn.query(F"select * from v_siswa_pindah") 
    pindah.index +=1
    pindah.index.rename('No', inplace=True)
    st.write(pindah)

def data_keluarga():
    st.text("data keluarga siswa")
    tab1,tab2 = st.tabs(['Siswa bersaudara', 'identitas orang tua'])
    with tab1:
        saudara()        

def saudara():
    pilih_ta = st.selectbox('tahun ajaran', (ta))
    st.text('jumlah anak')
    jml = conn.query(F"call jml_anak('{pilih_ta}' )")
    
    jml.index +=1
    jml.index.rename('No', inplace=True)
    st.write(jml)
    
    st.text('detail jumlah anak')
    bersaudara  = conn.query(F"call saudara('{pilih_ta}' )")
    bersaudara.index +=1
    bersaudara.index.rename('No', inplace=True)
    st.write(bersaudara)
