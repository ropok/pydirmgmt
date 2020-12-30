'''
list nama file audio, pertalent
output: 
.xlsx nama sheets = username
tampilkan apa saja nama file yang sudah ada
'''

import os
import pandas as pd
import glob
import collections

class Main():

    def __init__(self):
        super(Main, self)

    # open directory, list vt_names [get VT names]
    def openDir(self, path):
        vt_names = []
        # tr_names = []
        self.path = path
        for root, dirs, files in os.walk(self.path):
            for dire in dirs:
                dire_name = dire.split('_')
                vt_names.append(dire_name[0]) # username
        vt_names = sorted(list(set(vt_names))) # remove duplicate
        return vt_names

    def wavList(self, vt_name, path):
        wav_names = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.startswith(vt_name) and file.endswith('.wav'):
                    wav_names.append(file)
        return wav_names

    def wavDict(self, wav_names):
        wav_dict = {}
        col_names = []
        for wav in wav_names:
            col_name = wav.split('_')[4]
            col_names.append(col_name)
        col_names = sorted(list(set(col_names)))
        for col in col_names:
            wav_dict[col] = []
            for wav in wav_names:
                transcript = wav.split('_')[4]
                if col == transcript:
                    wav_dict[col].append(wav)
        return wav_dict
        
    # def writeDictXlsx(self, wav_dict):


                
    # count .wav per vt_names (as directory), return wav count
    def wavCount(self, vt_path):
        # os.chdir(vt_name)
        cnt = collections.Counter()
        for filename in glob.glob(os.path.join(vt_path,"*.wav")):
            name, ext = os.path.splitext(filename)
            cnt[ext] += 1
        # print(cnt[ext])
        return cnt[ext]

if __name__ == '__main__':
    path = 'C:/Users/jalerse/Downloads/data_speaker'
    main = Main()
    vt_names = main.openDir(path)
    # >> XLSX Writer
    xlsx_file = "output.xlsx"
    writer = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
    for vt_name in vt_names:
        wav_names = main.wavList(vt_name, path)
        wav_dict = main.wavDict(wav_names)

        wav_excel = pd.DataFrame.from_dict(wav_dict, orient='index')
        wav_excel = wav_excel.transpose()
        wav_excel.to_excel(writer, sheet_name=vt_name)
    writer.save()

    
    # print(vt_names, tr_names)
    # vt_name = "drp145_m_20201223_kumpulanistilah10_surabaya"
    # main.wavList(os.path.join(path, vt_name))

    # excel writer init
    # writer = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
    # output_data = pd.DataFrame(columns = ['no', 'nama folder', 'nama transcript', 'jumlah audio'])
    # main = Main()
    # vt_names = main.openDir(path)

    # for vt_name in vt_names:
    #     # for every vt_name
    #     print(vt_name)
    #     index = 0
    #     for root, dirs, files in os.walk(path):
    #         for dire in dirs:
    #             if dire.startswith(vt_name): # masuk folder berdasarkan nama username
    #                 # print(dire)
    # #                 # here we write the index, directory name, transcript name, and count
    #                 index += 1
    #                 directory_name = dire
    #                 transcript_name = dire.split('_')[3]
    #                 wav_count = main.wavList(os.path.join(path, dire)) # hitung .wav yang ada
    #                 dict_data = {'no':index, 'nama folder':directory_name, 'nama transcript':transcript_name, 'jumlah audio':wav_count}
    #                 # print(dict_data)
    #                 output_data = output_data.append(dict_data, ignore_index=True)
    #                 # print(output_data)
    #     output_data.to_excel(writer, sheet_name=vt_name, index=False)
    # writer.save()