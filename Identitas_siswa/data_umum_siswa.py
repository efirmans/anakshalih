import streamlit as st
import pandas as pd

conn = st.connection('mysql', type='sql' )
siswaData = conn.query("select * from cari_siswa")
historisKelas = conn.query("select * from historis_kelas")
alumniData = conn.query("SELECT * FROM alumni")
detailSiswa = conn.query("select * from detail_siswa")
def data_umum():
    st.text("Data umum siswa")
    tab1,tab2,tab3,tab4, tab5= st.tabs(['pencarian','historis', 'siswa pindah', 'alumni', 'info detail siswa'])
    with tab1:
        st.header('Pencarian  siswa')
        pencarian()
       
    with tab2:
        st.header('historis siswa')
        historis()

    with tab3:
        st.header('siswa pindah')
        siswa_pindah()

    with tab4:
        st.header('Alumni')
        alumni()

    with tab5:
        st.header('Info detail siswa')    
        detail()
# Pencarian Siswa
def pencarian():
    add_radio = st.radio(
                "cari siswa berdasarkan ",
                ("nama siswa", "NIS", "nama orang tua"),horizontal=True
            )
    df = pd.DataFrame(siswaData)
    
    
    if add_radio == "nama siswa":
        cari_siswa = st.text_input('input nama',max_chars=40)
        nama_siswa = df[df['Nama siswa'].str.contains(cari_siswa,regex=False,case=False)] 
    

    elif add_radio == "NIS":
        cari_nis = st.text_input('input NIS',max_chars=10)
        nama_siswa = df[df['NIS'].str.contains(cari_nis,regex=False,case=False)]
        
            
    else:
        cari_ortu = st.text_input('input nama orang tua',max_chars=40)
        nama_siswa = df[df['Nama Ayah'].str.contains(cari_ortu,regex=False,case=False) | df['Nama Ibu'].str.contains(cari_ortu,regex=False,case=False)] 

    nama_siswa.reset_index(inplace=True,drop=True)
    nama_siswa.index +=1
    nama_siswa.index.rename('No', inplace=True)
        
    
    st.dataframe(nama_siswa)

# mencari historis kelas
def historis():
    cari_historis = st.text_input(' ',max_chars=10)
    df = pd.DataFrame(historisKelas)
    df2 = df.query(F" nis == '{cari_historis}' ")
    df3= df[df['nis'] == cari_historis]['Nama siswa'].drop_duplicates().to_string(index=False)
    st.text('nama siswa: ' + df3 +  '\nNIS: ' + cari_historis)
    
    df2.reset_index(inplace=True,drop=True)
    df2.index +=1
    df2.index.rename('No', inplace=True)

    st.dataframe(df2[['tahun ajaran','kelas']])

#siswa pindah
def siswa_pindah():
    pindahData = conn.query("SELECT * FROM list_siswa_pindah")
    pindahData.index +=1
    pindahData.index.rename('No', inplace=True)
    st.write(pindahData)

def alumni():

    ad =pd.DataFrame(alumniData)

    daftarThnLulus = ad['tahun lulus'].unique().tolist()
    pilihTahunLulus = st.multiselect('tahun lulus',daftarThnLulus)
    mat = ad["tahun lulus"].isin(pilihTahunLulus)    
    st.write(ad[mat])

def detail():
    df = pd.DataFrame(detailSiswa)
    detail_nis = st.text_input('input NIS')
    df2 = df[df['nis'].str.contains(detail_nis,regex=False,case=False)]
    if detail_nis == '':
        st.text('input nis')    
    else:   
        st.table(df2.T)