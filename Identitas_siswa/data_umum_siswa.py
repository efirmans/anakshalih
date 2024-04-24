import streamlit as st
import pandas as pd
import extra_streamlit_components as stx

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
        st.session_state
        tab = stx.tab_bar(data=[
        stx.TabBarItemData(id="cari", title="Cari", description="nama alumni"),
        stx.TabBarItemData(id="tahun", title="tahun", description="kelulusan")])

        if tab == "cari":
            df = pd.DataFrame(alumniData)
            st.session_state
            cari  = st.text_input('Berdasarkan nama , NIS, nama orang tua',placeholder='silahkan input nama / nis / nama orang tua',key='carialumni' )
            if cari :
                nama_siswa = df[df['nama lengkap'].str.contains(cari, regex=False, case=False) | df['nis'].str.contains(cari, regex=False, case=False) 
                | df['nama ayah'].str.contains(cari, regex=False, case=False) | df['nama ibu'].str.contains(cari, regex=False, case=False)]

                nama_siswa.reset_index(inplace=True, drop=True)
                nama_siswa.index += 1
                nama_siswa.index.rename('No', inplace=True)
                st.dataframe(nama_siswa, use_container_width=True)          

        elif tab == "tahun":
            alumni()



                
    with tab5:
        st.header('Info detail siswa')    
        detail()

# Pencarian Siswa
def pencarian():
    # # Initialize session state for search input if not already set
    # if 'search_input' not in st.session_state:
    #     st.session_state.search_input = ''

    # add_radio = st.radio(
    #     "cari siswa berdasarkan ",
    #     ("nama siswa", "NIS", "nama orang tua"), horizontal=True
    # )
    # df = pd.DataFrame(siswaData)
    
    # # Use session state to store and retrieve the current search input
    # st.session_state.search_input = st.text_input('input ' + add_radio, max_chars=40, value=st.session_state.search_input)
    
    # if st.session_state.search_input == '':
    #     pass
    # else:
    #     if add_radio == "nama siswa":
    #         nama_siswa = df[df['Nama siswa'].str.contains(st.session_state.search_input, regex=False, case=False)]
        
    #     elif add_radio == "NIS":
    #         nama_siswa = df[df['NIS'].str.contains(st.session_state.search_input, regex=False, case=False)]
            
    #     else:
    #         nama_siswa = df[df['Nama Ayah'].str.contains(st.session_state.search_input, regex=False, case=False) | 
    #                         df['Nama Ibu'].str.contains(st.session_state.search_input, regex=False, case=False)]

    #     nama_siswa.reset_index(inplace=True, drop=True)
    #     nama_siswa.index += 1
    #     nama_siswa.index.rename('No', inplace=True)
    
    #     st.dataframe(nama_siswa, use_container_width=True)


#baru
    df = pd.DataFrame(siswaData)
    st.session_state
    cari  = st.text_input('Berdasarkan nama siswa, NIS, nama orang tua',placeholder='silahkan input nama siswa / nis / nama orang tua' )
    if cari :
        nama_siswa = df[df['Nama siswa'].str.contains(cari, regex=False, case=False) | df['NIS'].str.contains(cari, regex=False, case=False) 
        | df['Nama Ayah'].str.contains(cari, regex=False, case=False) | df['Nama Ibu'].str.contains(cari, regex=False, case=False)]

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
        adplus = ad[['tahun lulus','nis', 'nama lengkap']]
        daftarThnLulus = adplus['tahun lulus'].unique().tolist()
        pilihTahunLulus = st.multiselect('tahun lulus',daftarThnLulus,placeholder='pilih tahun lulus')
        mat = adplus["tahun lulus"].isin(pilihTahunLulus)    
        if pilihTahunLulus == []:
            st.session_state
            pass
        else:
            st.dataframe(adplus[mat],use_container_width=True,hide_index=True)

def detail():
    df = pd.DataFrame(detailSiswa)
    detail_nis = st.text_input('input NIS')
    df2 = df[df['nis'].str.contains(detail_nis,regex=False,case=False)]
    if detail_nis == '':
        pass  
    else:   
        df2_display = df2.reset_index(drop=True).T
        st.table(df2_display)