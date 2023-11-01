import streamlit as st
import pandas as pd
import csv

conn = st.experimental_connection('mysql', type='sql' )
ta = conn.query(F"select thn_ajaran as ta FROM thn_ajaran order by ta desc ")
unit= conn.query(F"select nama_unit  FROM unit_pendidikan ")

def biaya_pendidikan():
    st.write("# Biaya Pendidikan")
    
    last_update=conn.query(F"select date_format(max(tgl_bayar),'%d-%m-%Y') as '' from dana_pendidikan")
    df=last_update
    ubah = df.values.tolist()
    satu = str(ubah).replace("[['","") 
    st.text('data terakhir: '+ str(satu).replace("']]",""))

    sub_kategori ={
        "histori pembayaran":histori,
        "dompet pendidikan":dompet_pendidikan,
        "tunggakan":tunggakan,
        'Posisi dana':dana
         }
    sub_kat = st.sidebar.selectbox('sub kategori', sub_kategori.keys())
    sub_kategori[sub_kat]()
    
def histori():
    st.text('histori pembayaran')
    col1,col2 = st.columns(2)
    with col1:
        pilih_ta = st.selectbox('pilih tahun ajaran',  (ta))
    with col2:
        queri = conn.query(F"select kategori from kategori_tagihan ")
        tambahan = "semua kategori"
        queri.loc[len(queri)] = tambahan
        kategori = st.selectbox('kategori tagihan',  (queri))

    cari = st.text_input('input nis',max_chars=10)
    nama_siswa = conn.query(F"select `nama_lengkap` as '' from siswa where `NIS SDIT` = '{cari}' or `NIS TKIT` = '{cari}' limit 1")
    df=nama_siswa
    ubah = df.values.tolist()
    satu = str(ubah).replace("[['","") 
    st.text('nama siswa: '+ str(satu).replace("']]",""))

    if cari=='':
        st.info('silahan input NIS')
    elif kategori == tambahan:
        df =conn.query (F"call nama_by_tagih_non_kategori ('{cari}','{pilih_ta}')")
        df.index +=1
        df.index.rename('No', inplace=True)
        st.dataframe(df)
    else:
        df =conn.query (F"call nama_by_tagih ('{cari}','{pilih_ta}','{kategori}')")
        df.index +=1
        df.index.rename('No', inplace=True)
        st.dataframe(df)
    
def dompet_pendidikan():
    st.text('dompet pendidikan')
    pilih_ta = st.selectbox('pilih tahun ajaran',  (conn.query(F"select thn_ajaran as ta FROM thn_ajaran order by ta desc ")))
    dopendik = conn.query(F"call donatur('{pilih_ta}') ")
    st.write(dopendik)

def belum_bayar():
    st.text('belum melakukan pembayaran berdasarkan jenis tagihan')
    pilih_ta = st.selectbox('pilih tahun ajaran',  (ta))
    kat_unit = st.selectbox('kategori tagihan',  (unit))
    
    queri = conn.query(F"select kategori from kategori_tagihan ")
    kat_tag = st.selectbox('kategori tagihan',  (queri))

    tag = conn.query(F"select distinct tag_singkat from  tag_kat where kategori = '{kat_tag}'  and nama_unit = '{kat_unit}' and thn_ajaran ='{pilih_ta}' ")
    nama_tag = st.selectbox('nama tagihan',(tag))

    df= conn.query(F"call belum_bayar ('{pilih_ta}', '{kat_unit}','{kat_tag}', '{nama_tag}') ")
    df.index +=1
    df.index.rename('No', inplace=True)
    st.write(df)

def convert_df(df):
    return df.to_csv(index=False,quoting=csv.QUOTE_NONNUMERIC,decimal=',').encode('utf-8')

def tunggakan():
    st.header('Tunggakan')
    total = conn.query("select * from v_total_tunggakan")
    df =total
    ubah = df.values.tolist()
    satu = str(ubah).replace("[['","") 
    st.text('jumlah tunggakan '+ str(satu).replace("']]",""))
    tab1, tab2, tab3, tab4 = st.tabs(["berdasar jenis tagihan", 
                                "berdasar nama siswa", 
                                "berdasar unit",
                                "berdasar nama orang tua"])

    # berdasar jenis tagihan
    with tab1:
        # jenis tagihan
               
        tagihan= conn.query("select * from v_tunggakan_by_nama_tagihan")
        kategori = st.selectbox('kategori tagihan',tagihan['kategori'].drop_duplicates()) 
        
        df= pd.DataFrame(tagihan)
        pilih = df.query(F"kategori == '{kategori}' ")
        pilih_tag = st.selectbox('nama tagihan',pilih['nama tagihan'].drop_duplicates())
                
        hasilnya = df.query(F" `nama tagihan`  == '{pilih_tag}' ")
        hasilnya.reset_index(inplace=True)
        hasilnya.index +=1
        hasilnya.index.rename("no", inplace=True )
        filter_hasil = hasilnya[['nama siswa', 'total', 'terbayarkan','kekurangan']]
        
        filter_hasil.loc['Total'] = pd.Series(filter_hasil.sum(numeric_only=True) )
        st.dataframe(filter_hasil)

        # df.index +=1
        # df.index.rename('No', inplace=True)
        # tag_apa =    df.query(F" `nama tagihan` == '{tagih}' ")
        # siapa_aja = tag_apa[['nama siswa','total','terbayarkan','kekurangan']] 
        
        # st.write(siapa_aja)
        
            #download
        csv = convert_df(df)
        st.download_button(
        label="download per nama tagihan",
        data= csv,
        file_name="per nama tagihan.csv",
        mime="text/csv"
        )   
        
        # kumulatif jenis tagihan

        df= conn.query("select * from v_tunggakan_kumulatif_nama_tagihan")
        
            #download
        csv = convert_df(df)
        st.download_button(
        label="download kumulatif per tagihan",
        data= csv,
        file_name="kumulatif per nama tagihan.csv",
        mime="text/csv"
        )

    # berdasar nama siswa
   
    with tab2:
        nama_siswa= conn.query("select distinct `nama siswa` from v_tunggakan_by_nama_siswa")
        df5 = pd.DataFrame(nama_siswa)
        cari_nama = st.selectbox('nama siswa',df5)
        
        # tunggakan nama siswa
        df= conn.query("select * from v_tunggakan_by_nama_siswa")
        
        df3 = df.query(F"`nama siswa` == '{cari_nama}' ")
        
        df3.reset_index(inplace=True)
        df3.index +=1
        df3.loc['Total'] = pd.Series(df3.sum(numeric_only=True) )
        
        df3.index.rename('No',inplace=True)
        
        st.write(df3[['tagihan','total','terbayarkan','kekurangan']])
           
            #download

        col1,col2 = st.columns(2)
        with col1:
            st.caption('tunggakan siswa per tagihan')
            csv = convert_df(df)
            st.download_button(
            label="download",
            data= csv,
            file_name="siswa tagihan.csv",
            mime="text/csv"
            )   
        with col2:
            df = conn.query("select * from v_tunggakan_kumulatif_nama_siswa")
            st.caption('tunggakan kumulatif per siswa')
            csv = convert_df(df)
            st.download_button(
            label="download",
            data= csv,  
            file_name="kumulatif per siswa.csv",
            mime="text/csv"
            ) 

    with tab3:
        st.header("berdasar unit")
        
        col1,col2= st.columns(2)
        with col1:
            pilih_ta = st.selectbox('pilih tahun ajaran',  (ta))
        with col2:
            kat_unit = st.selectbox('kategori tagihan',  (unit))
        col1,col2= st.columns(2)
        with col1:
            queri = conn.query(F"select kategori from kategori_tagihan ")
            kat_tag = st.selectbox('kategori tagihan',  (queri))
        with col2:
            tag = conn.query(F"select distinct tag_singkat from  tag_kat where kategori = '{kat_tag}'  and nama_unit = '{kat_unit}' and thn_ajaran ='{pilih_ta}' ")
            tambahan = "Semua SPP"
            tag.loc[len(tag)] = tambahan

            nama_tag = st.selectbox('nama tagihan',(tag))
            
        if nama_tag == 'Semua SPP':
            result = conn.query(F"call belum_bayar_Semua_tag ('{pilih_ta}', '{kat_unit}','{kat_tag}')")
            df = pd.DataFrame(result)
            df.index +=1
            df.index.rename('No', inplace=True)

        else:
            hasil= conn.query(F"call belum_bayar ('{pilih_ta}', '{kat_unit}','{kat_tag}', '{nama_tag}') ")
            df = pd.DataFrame(hasil)
            df.index +=1
            df.index.rename('No', inplace=True)
               
        df.loc['Total'] = pd.Series(df.sum(numeric_only=True) )
        st.write(df)
     
    with tab4:          
        nama_ortu = conn.query(f"select distinct `nama orang tua` from v_tunggakan_ortu")
        semua = "semua orang tua"
        
        nama_ortu.loc[len(nama_ortu.index)] = semua 
        cari = st.selectbox("ketik nama ortu", nama_ortu )
        
        
        # tunggakan ortu
        ortu = 'select * from v_tunggakan_ortu '
        if cari == "semua orang tua":
            df= conn.query(ortu)
            
            # kumulatif tunggakan ortu
            df.loc['Total'] = pd.Series(df.sum(numeric_only=True) )
            st.write(df)
        else:
            df= conn.query(ortu)
            df2 = df.query(F" `nama orang tua` == '{cari}' ",)
            
            df2.reset_index(inplace=True)
            df2.index +=1
            df2.loc['Total'] = pd.Series(df2.sum(numeric_only=True) )
            df6 = df2[['nama siswa','total','terbayarkan','kekurangan']]
            st.write(df6)
            
        #download
        df = conn.query("select * from v_kumulatif_ortu")
        
        csv = convert_df(df)
        st.download_button(
        label="kumulatif per siswa ortu",
        data= csv,
        file_name="kumulatif per ortu.csv",
        mime="text/csv"
        ) 

def dana():
    tab1,tab2,tab3 = st.tabs(['per tagihan','per kategori', 'kumulatif'])
    with tab1:
        st.text('posisi dana')
        
        col1,Col2,Col3 =st.columns(3)
        with col1:
            tahun =   st.selectbox('pilih tahun ajaran',  (ta))
        with Col2:
            up =  st.selectbox('unit',  (unit))
        with Col3:
            kat_tagihan= conn.query("select kategori FROM kategori_tagihan")
            kategori =  st.selectbox('kategori tagihan',  (kat_tagihan))
        posisi = conn.query(F"call pendatan_per_tagihan('{tahun}', '{up}', '{kategori}')")
        df = pd.DataFrame(posisi)
        df.index.rename('no', inplace=True)
        df.index +=1
        ubah = df.rename(columns={'tag_singkat':'tagihan'})
        st.write(ubah)
    
    with tab2:
        st.text('per kategori')
        Go11,Gol2 = st.columns(2)
        with Go11:
            t_ajar = conn.query(F"select thn_ajaran as ta FROM thn_ajaran order by ta desc ")
            t_ajaran =   st.selectbox(' tahun ajaran',  (t_ajar))
        with Gol2:
            up2= conn.query(F"select nama_unit  FROM unit_pendidikan ")
            unpen =  st.selectbox('unit pendidikan',  (up2))
        
        
        dana_kat = conn.query(F"call dana_per_kategori('{t_ajaran}','{unpen}')")
        df = pd.DataFrame(dana_kat)
        df.index.rename('no', inplace=True)
        df.index +=1
       
        # ubah heading label
        df2 =df.rename(columns={"sum(dp.terbayarkan)":"terbayar","sum(dp.kekurangan)":"kekurangan"})

        st.write(df2)
    
    with tab3:
        st.text('kumulatif')
