"""
Created on Mon Nov 26 2020

@author: jalerse
generate directory untuk perekaman stt dengan smartphone
juga directory untuk upload validator
"""

import os
import pandas as pd
from datetime import datetime

kode_tanggal = datetime.today().strftime('%Y%m%d') # datenow

# define path variable
path_output = 'talentDir-' + kode_tanggal
path_datadiri = os.path.join(r'C:\Users\jalerse\Downloads', 'Data Peserta - username 24122020.csv')
path_transcript = 'transcript-20201130'
xlsx_transcript = path_transcript+'.xlsx'
log = 'log.txt'
log_datadiri = 'datadiri.txt'


class Main3():
    def __init__(self):
        super(Main3, self)
    
    def hello(self):
        print("hellow!")

    def bikinDirektori(self):
        # buka csv
        csv_data = pd.read_csv(path_datadiri)
        # baca csv perbaris, for every talent name
        for i in range(0, len(csv_data)):
            if 'HP' in csv_data['Alat'][i]:
                # get data diri
                data_nama = csv_data['Nama Lengkap'][i]
                data_kelamin = csv_data['Jenis Kelamin'][i]
                data_usia = csv_data['Umur'][i]
                data_dialek = csv_data['Dialek'][i]
                kode_nama = csv_data['Username'][i]
                # Print processing progress
                print("processing", kode_nama)
                path_talent = os.path.join(path_output, kode_nama)
                if not os.path.exists(path_talent):
                    os.makedirs(path_talent)
                path_log = os.path.join(path_talent, log_datadiri)
                # simpan ke log
                log_data = open(path_log, 'w')
                # tulis log sesuai data google form individu
                log_data.write("{nama},{kelamin},{usia},{dialek},{username}".format(nama=data_nama, kelamin=data_kelamin, usia=str(data_usia), dialek=data_dialek, username=kode_nama))


    def bikinExcel(self):
        # panda excel writer
        writer = pd.ExcelWriter(xlsx_transcript, engine = 'xlsxwriter')
        # akses .csv dalam satu folder
        for root, dirs, files in os.walk(path_transcript):
            for filename in files:
                # buka csv dengan pandas
                file_csv = os.path.join(root, filename)
                csv_data = pd.read_csv(file_csv)
                # ambil kolom 'transcript_perekaman'
                data_transcript = csv_data['transcript_perekaman']
                number_transcript = list(range(1,data_transcript.size+1))
                # formating ke DataFrame, sesuai kolom
                data = pd.DataFrame({'no': number_transcript, 'transcript_perekaman': data_transcript})
                # convert dataframe ke excel
                sheet_title = filename.split('.')[0]
                data.to_excel(writer, sheet_name=sheet_title, index=False)

        # close pandas excel writer and output excel file
        writer.save()

        # print(data_transcript.size)
    
    def bikinDiretoriUsername(self, txtFile):
        f = open(txtFile, 'r')
        list_username = []
        for i in f:
            list_username.append(i)
        return list_username

if __name__ == "__main__":
    main3 = Main3()
    main3.bikinDirektori()
    # main3.bikinExcel()
    # list_username = main3.bikinDiretoriUsername('usernameTalent.txt')
