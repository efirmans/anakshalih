import streamlit as st
import pandas as pd

conn = st.connection('mysql', type='sql' )
tagihan= conn.query("select * from v_tunggakan_by_nama_tagihan")
df= pd.DataFrame(tagihan)
catatan = conn.query ("SELECT * from dana_pendidikan")


def nunggak():
    df2 = pd.DataFrame(catatan)
    df2['tgl_bayar'] = pd.to_datetime(df2['tgl_bayar'],format="mixed" )
    max_date = df2['tgl_bayar'].max()
    st.write('data update',max_date)
    nama_tab = ["Agregat tunggakan","jenis tagihan", "nama siswa","unit","nama orang tua"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(nama_tab)

    with tab1:
        st.text('Agregat tunggakan')
        df2 = df.rename(columns={"kekurangan":"nominal"})
        total_tunggakan = df2.groupby('kategori')['nominal'].sum().reset_index()
        
        
        total_tunggakan.loc[len(total_tunggakan)] = ['TOTAL', total_tunggakan['nominal'].sum()]

        st.dataframe(total_tunggakan,hide_index=True)

    with tab2:
        kategori = st.selectbox('kategori tagihan',df['kategori'].drop_duplicates()) 
        pilih = df.query(f"kategori == '{kategori}' ")
        ngurut = pilih.sort_values(by='urutan')
        pilih_tag = st.selectbox('nama tagihan',ngurut['nama tagihan'].drop_duplicates())
                
        hasilnya = df.query(f" `nama tagihan`  == '{pilih_tag}' ")
        hasilnya.reset_index(inplace=True)
        hasilnya.index +=1
        hasilnya.index.rename("no", inplace=True )
        filter_hasil = hasilnya[['nis','nama siswa', 'total', 'terbayarkan','kekurangan']]
        
        total_row = pd.Series(filter_hasil.sum(numeric_only=True)).fillna(0)
        filter_hasil.loc['Total'] = total_row
        st.write(filter_hasil)

    with tab3:
        st.text('berdasar nama siswa')
        cari_nis = st.text_input('input nis')
    
        if cari_nis:
            df2 = df.query("nis == @cari_nis ")
            
            df2.reset_index(drop=True, inplace=True)
            df2.index +=1
            df2.loc['Total'] = pd.Series(df2.sum(numeric_only=True).fillna(0) )
            df2.index.rename('No',inplace=True)
            df4= df[df['nis'] == cari_nis]['nama siswa'].drop_duplicates().to_string(index=False)
            st.text('nama siswa: ' + df4 +  '\nNIS: ' + cari_nis)
            df3 = df2[['kategori','total','terbayarkan','kekurangan']]
            st.dataframe(df3)

    with tab4:
        st.header("berdasar unit")
   
    with tab5:
        
        tampil = df[['nama orang tua', 'total', 'terbayarkan', 'kekurangan']]
        gabung = tampil.groupby('nama orang tua')[['total', 'terbayarkan', 'kekurangan']].sum()
        filter = gabung.sort_values('kekurangan', ascending=False)

        # Get the range from the slider  
        slider_range = st.slider('range', max_value=30000000, min_value=1000000, step=1000000, value=(1000000, 5000000))
        formatted_min_value = f"{slider_range[0]:,}"
        formatted_max_value = f"{slider_range[1]:,}"

        # Display the formatted values
        st.write(f"range tunggakan: {formatted_min_value} - {formatted_max_value}")

        # Use the slider range to filter the DataFrame
        filtered_df = filter[(filter['kekurangan'] >= slider_range[0]) & (filter['kekurangan'] <= slider_range[1])]
        st.dataframe(filtered_df,use_container_width=True,)