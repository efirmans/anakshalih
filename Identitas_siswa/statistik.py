import streamlit as st
import pandas as pd
import altair as alt

conn = st.connection('mysql', type='sql' )

jml_siswa_unit  = conn.query("Select * from jumlah_siswa")
jml_siswa_per_kelas = conn.query("select * from jml_siswa_per_kelas")
siswaData = conn.query("select * from siswa_per_kelas")
bersaudara = conn.query("SELECT * FROM jumlah_anak")
alamat = conn.query("SELECT * FROM sebaran_alamat")
alamat_siapa = conn.query("SELECT * FROM alamat_siapa")

def statistik():
    st.text("statistik siswa")
    if 'tab_index' not in st.session_state:
        st.session_state.tab_index = 0
    tab1, tab2, tab3,tab4,tab5 = st.tabs(["jumlah siswa per unit", "jumlah siswa per kelas", "daftar siswa per kelas", "sebaran domisili", "siswa bersaudara"])

        # Set the current tab based on the stored index
    current_tab = st.session_state.tab_index
    
    with tab1:
        st.header("jumlah siswa per unit")
        per_unit()    

    with tab2:
        st.header("jumlah siswa per kelas")
        jml_siswa_kelas()
    
    with tab3:
        st.header("daftar siswa per kelas")
        siswaKelas()

    with tab4:
        st.header("sebaran domisili")
        sebaran()
    
    with tab5:
        st.header("siswa bersaudara")
        jumlah_anak()


    # Update the tab index in session state when a tab is selected
    if tab1:
        st.session_state.tab_index = 0
    elif tab2:
        st.session_state.tab_index = 1
    elif tab3:
        st.session_state.tab_index = 2 


    
def per_unit():
    df = pd.DataFrame(jml_siswa_unit)
    nama_unit = df['nama unit'].unique().tolist()
    pilih_unit = st.multiselect('unit pendidikan',nama_unit,placeholder='pilih unit pendidikan')

    thn_ajaran = df['tahun ajaran'].unique().tolist()
    pilih_ta = st.multiselect('tahun ajaran',thn_ajaran, placeholder='pilih tahun ajaran')
    
    filter_unit = df['nama unit'].isin(pilih_unit)
    filter_ta = df['tahun ajaran'].isin(pilih_ta)
    
    jumlah = df[filter_unit & filter_ta]
    st.session_state
    if pilih_unit == [] or pilih_ta == []:
        pass
    else:
        bars =alt.Chart(jumlah).mark_bar(size=30).encode(
        x='nama unit',
        y='sum(jumlah siswa)',
        color='nama unit',
        tooltip=['nama unit','jumlah siswa']
                                       ).properties(width=150)
    
        text = bars.mark_text(
            align='center',
            baseline='middle',
            dy=-10  # Adjust the vertical position of the labels
        ).encode(
            text='sum(jumlah siswa)'
        )

        chart = alt.layer(bars + text).facet(column='tahun ajaran')
        st.altair_chart(chart)

def jml_siswa_kelas():
    
    df = pd.DataFrame(jml_siswa_per_kelas)
    
    nama_unit = df['nama unit'].unique().tolist()
    thn_ajaran = df['tahun ajaran'].unique().tolist()
       
    Col1,Col2, Col3 = st.columns(3)
   
    with Col1:
        pilih_unit = st.multiselect('unit',nama_unit,placeholder='pilih unit pendidikan')
    with Col2:  
        pilih_ta = st.multiselect('Tahun ajaran',thn_ajaran, placeholder='pilih tahun ajaran')
    with Col3:
        # Check if any unit is selected
        if pilih_unit:
            # Filter the DataFrame for the selected units and get the unique class names
            nama_kelas = df[df['nama unit'].isin(pilih_unit)]['nama kelas'].drop_duplicates().tolist()
        else:
            # If no unit is selected, set nama_kelas to an empty list
            nama_kelas = []
        pilih_kelas = st.multiselect('nama kelas', nama_kelas, placeholder='pilih kelas')

    filter_unit = df['nama unit'].isin(pilih_unit)
    filter_ta = df['tahun ajaran'].isin(pilih_ta)
    filter_kelas = df['nama kelas'].isin(pilih_kelas)
    
    jumlah = df[filter_unit & filter_ta & filter_kelas]
    if pilih_unit == [] or pilih_ta == [] or pilih_kelas == []:
        pass
    else:
        st.dataframe(jumlah[['tahun ajaran','nama unit','nama kelas','jumlah siswa']],hide_index=True)

def siswaKelas():
    df2 = pd.DataFrame(siswaData)
    
    Col1,Col2,Col3 = st.columns(3)
    with Col1:
        unit = df2['nama unit'].unique().tolist()
        pil_unit = st.multiselect('unit',unit,placeholder='pilih unit')
    with Col2:  
        ta = df2['tahun ajaran'].unique().tolist()
        pil_ta = st.multiselect('thn ajaran',ta)
    with Col3:
        if pil_unit:
           nama_kelas = df2[df2['nama unit'].isin(pil_unit)]['nama kelas'].drop_duplicates().tolist()
        else:
            nama_kelas = []
        pil_kelas = st.multiselect('kelas',nama_kelas,placeholder='pilih kelas')

    filter_unit = df2['nama unit'].isin(pil_unit)
    filter_ta = df2['tahun ajaran'].isin(pil_ta)
    filter_kelas = df2['nama kelas'].isin(pil_kelas)

    hasil = df2[filter_unit & filter_ta & filter_kelas]
    if pil_unit == [] or pil_ta == [] or pil_kelas == []:
        pass
    else:
        st.dataframe(hasil[['tahun ajaran','nama unit','nis','nama kelas','nama']],hide_index=True,use_container_width=True)
    
def sebaran():
    df = pd.DataFrame(alamat)
    df2 = pd.DataFrame(alamat_siapa)
    df.reset_index()
    df.index +=1
    df.index.rename('No', inplace=True)
    
    st.dataframe(df,use_container_width=True)

    
    kelurahan = df2['kelurahan'].unique().tolist()
    pilih_kelurahan = st.selectbox('kelurahan',kelurahan,placeholder='pilih kelurahan...',)
    cari_kelurahan = df2.query(F"kelurahan == '{pilih_kelurahan}' ")
    
    
    cari_kelurahan.reset_index(inplace=True,drop=True)
    cari_kelurahan.index +=1
    # cari_kelurahan.rename('No', inplace=False)
    
    st.dataframe(cari_kelurahan,use_container_width=True)
    

def jumlah_anak():
    df = pd.DataFrame(bersaudara)
    pilih = st.slider('jumlah anak',2,5)
    st.session_state
    hasil = df[df['jumlah anak']==pilih ]
    hasil.reset_index(drop=True,inplace=True)
    hasil.index +=1
    hasil.index.rename('no',inplace=True)
    st.dataframe(hasil,use_container_width=True)