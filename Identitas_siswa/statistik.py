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
    
    tab1, tab2, tab3,tab4,tab5 = st.tabs(["jumlah siswa per unit", "jumlah siswa per kelas", "daftar siswa per kelas", "sebaran domisili", "siswa bersaudara"])

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
    
def per_unit():
    df = pd.DataFrame(jml_siswa_unit)
    nama_unit = df['nama unit'].unique().tolist()
    pilih_unit = st.multiselect('unit pendidikan',nama_unit)

    thn_ajaran = df['tahun ajaran'].unique().tolist()
    pilih_ta = st.multiselect('tahun ajaran',thn_ajaran)
    
    filter_unit = df['nama unit'].isin(pilih_unit)
    filter_ta = df['tahun ajaran'].isin(pilih_ta)
    
    jumlah = df[filter_unit & filter_ta]

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
    pilih_unit = st.multiselect('unit',nama_unit)

    thn_ajaran = df['tahun ajaran'].unique().tolist()
    pilih_ta = st.multiselect('Tahun ajaran',thn_ajaran)
    
    nama_kelas = df['nama kelas'].unique().tolist()
    pilih_kelas = st.multiselect('nama kelas',nama_kelas)

    filter_unit = df['nama unit'].isin(pilih_unit)
    filter_ta = df['tahun ajaran'].isin(pilih_ta)
    filter_kelas = df['nama kelas'].isin(pilih_kelas)


    jumlah = df[filter_unit & filter_ta & filter_kelas]
    st.dataframe(jumlah[['tahun ajaran','nama unit','nama kelas','jumlah siswa']],hide_index=True)

def siswaKelas():
    df2 = pd.DataFrame(siswaData)
    unit = df2['nama unit'].unique().tolist()
    pil_unit = st.multiselect('unit',unit)

    ta = df2['tahun ajaran'].unique().tolist()
    pil_ta = st.multiselect('thn ajaran',ta)
    
    kelas = df2['nama kelas'].unique().tolist()
    pil_kelas = st.multiselect('kelas',kelas)

    filter_unit = df2['nama unit'].isin(pil_unit)
    filter_ta = df2['tahun ajaran'].isin(pil_ta)
    filter_kelas = df2['nama kelas'].isin(pil_kelas)

    hasil = df2[filter_unit & filter_ta & filter_kelas]
    st.dataframe(hasil[['tahun ajaran','nama unit','nis','nama kelas','nama']],hide_index=True)
    
def sebaran():
    df = pd.DataFrame(alamat)
    df2 = pd.DataFrame(alamat_siapa)
    st.dataframe(df)

    
    kelurahan = df2['kelurahan'].unique().tolist()
    pilih_kelurahan = st.selectbox('kelurahan',kelurahan,placeholder='pilih kelurahan...',)
    cari_kelurahan = df2.query(F"kelurahan == '{pilih_kelurahan}' ")
    cari_kelurahan.reset_index(inplace=True,drop=True)
    cari_kelurahan.index +=1
    # cari_kelurahan.rename('No', inplace=True)
    st.dataframe(cari_kelurahan)
    

def jumlah_anak():
    df = pd.DataFrame(bersaudara)
    st.dataframe(df)