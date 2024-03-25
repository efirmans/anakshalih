import streamlit as st
import pandas as pd

conn = st.connection('mysql', type='sql' )
siswaData = conn.query("select * from cari_siswa")
historisKelas = conn.query("select * from historis_kelas")
alumniData = conn.query("SELECT * FROM alumni")
detailSiswa = conn.query("select * from detail_siswa")

def data_umum():
    st.text("Data umum siswa")


    tab1,tab2,tab3,tab4, tab5= st.tabs(['pencarian','historis', 'siswa pindah', 'alumni', 'info detail siswa'],)
      
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
        st.session_state.active_tab =1
        alumni()

    with tab5:
        st.header('Info detail siswa')    
        detail()

# Pencarian Siswa
def pencarian():
    # Initialize session state for search input if not already set
    if 'search_input' not in st.session_state:
        st.session_state.search_input = ''

    add_radio = st.radio(
        "cari siswa berdasarkan ",
        ("nama siswa", "NIS", "nama orang tua"), horizontal=True
    )
    df = pd.DataFrame(siswaData)
    
    # Use session state to store and retrieve the current search input
    st.session_state.search_input = st.text_input('input ' + add_radio, max_chars=40, value=st.session_state.search_input)
    
    if st.session_state.search_input == '':
        pass
    else:
        if add_radio == "nama siswa":
            nama_siswa = df[df['Nama siswa'].str.contains(st.session_state.search_input, regex=False, case=False)]
        
        elif add_radio == "NIS":
            nama_siswa = df[df['NIS'].str.contains(st.session_state.search_input, regex=False, case=False)]
            
        else:
            nama_siswa = df[df['Nama Ayah'].str.contains(st.session_state.search_input, regex=False, case=False) | 
                            df['Nama Ibu'].str.contains(st.session_state.search_input, regex=False, case=False)]

        nama_siswa.reset_index(inplace=True, drop=True)
        nama_siswa.index += 1
        nama_siswa.index.rename('No', inplace=True)
    
        st.dataframe(nama_siswa, use_container_width=True)

# mencari historis kelas
def historis():
    cari_historis = st.text_input(' ',max_chars=10,placeholder='input nis')
    df = pd.DataFrame(historisKelas)
    df2 = df.query(F" nis == '{cari_historis}' ")
    df3= df[df['nis'] == cari_historis]['Nama siswa'].drop_duplicates().to_string(index=False)
    if cari_historis =='':
        pass
    else:
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
    pilihTahunLulus = st.multiselect('tahun lulus',daftarThnLulus,placeholder='pilih tahun lulus')
    mat = ad["tahun lulus"].isin(pilihTahunLulus)    
    if pilihTahunLulus == []:
        st.session_state
        pass
    else:
        st.dataframe(ad[mat],use_container_width=True,hide_index=True)

def detail():
    df = pd.DataFrame(detailSiswa)
    detail_nis = st.text_input('input NIS')
    df2 = df[df['nis'].str.contains(detail_nis,regex=False,case=False)]
    if detail_nis == '':
        pass  
    else:   
        df2_display = df2.reset_index(drop=True).T
        st.table(df2_display)