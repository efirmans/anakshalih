import streamlit as st
import pandas as pd

conn = st.connection('mysql', type='sql' )
jml_siswa_per_kelas = conn.query("select * from jml_siswa_per_kelas")


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


    