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
import librosa

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
                if file.startswith(vt_name) and file.endswith('.wav') and not file.endswith(").wav"):
                    wav_names.append(file)
        return wav_names

    def wavDict(self, wav_names):
        wav_dict = {}
        col_names = []
        wav_count = 0
        wav_dict['jumlah baris'] = []
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
                    wav_count +=1
        wav_dict['jumlah baris'].append(wav_count)
        return wav_dict
        
    # count .wav per vt_names (as directory), return wav count
    def wavCount(self, vt_path):
        count_wav = 0
        for root, dirs, files in os.walk(vt_path):
            for file in files:
                if file.endswith('.wav') and not file.endswith(").wav") and not file.endswith(").wav"):
                    count_wav += 1
        return count_wav

    def fileLength(self, file_wav):
        duration = librosa.get_duration(filename=file_wav)
        return duration

    def wavDuration(self, path, nama_vt):
        duration = 0
        duration_menit = 0
        duration_jam = 0
        jumlah_baris = 0
        total_duration_jam = 0
        total_duration_menit = 0
        total_jumlah_baris = 0
        for root, dirs, files in os.walk(path):
            for index, filename in enumerate(files, start=1):
                if filename.startswith(nama_vt) and filename.endswith(".wav") and not filename.endswith(").wav"):
                    file_wav = root + "/" + filename
                    try:
                        # duration = librosa.get_duration(filename=file_wav)
                        file_duration = librosa.get_duration(filename=file_wav)
                        duration = duration + file_duration
                        jumlah_baris += 1
                    except:
                        # print(filename+' error')
                        pass
        duration_jam = round(duration/3600, 2)
        duration_menit = round(duration/60, 2)   
        total_duration_menit += duration_menit   
        total_duration_jam += duration_jam
        return total_duration_jam

if __name__ == '__main__':
    
    path = '/media/server/MyPassport/STT/Arsip-Data-1800jam/dailycount-speaker/'
    main = Main()
    # >> Username - baris - jam
    vt_names = ['yog104','mut139','deb111','apr109','ind145','indahp','pan142']
    for vt_name in vt_names:
        path_vt = os.path.join(path, vt_name)
        username = vt_name
        baris = len(main.wavList(vt_name, path_vt))
        jam = main.wavDuration(path, vt_name)
        print("{} - {} - {}".format(username, baris, jam))
    # path = 'C:/Users/jalerse/Downloads/data_speaker'
    # main = Main()
    # vt_names = main.openDir(path)
    # # >> XLSX Writer
    # xlsx_file = "list_downloaded_speaker.xlsx"
    # writer = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
    # for vt_name in vt_names:
    #     wav_names = main.wavList(vt_name, path)
    #     wav_dict = main.wavDict(wav_names)
    #     count_dict = []


    #     wav_excel = pd.DataFrame.from_dict(wav_dict, orient='index')
    #     wav_excel = wav_excel.transpose()
    #     wav_excel.to_excel(writer, sheet_name=vt_name)
    # writer.save()

    
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