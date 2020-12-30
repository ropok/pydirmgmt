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
        self.path = path
        for root, dirs, files in os.walk(self.path):
            for dire in dirs:
                if dire[-3:].isnumeric() and len(dire) < 7:
                    vt_names.append(dire)
        vt_names = sorted(list(set(vt_names)))
        return vt_names

    def wavList(self, vt_path):
        wav_names = []
        for root, dirs, files in os.walk(vt_path):
            for file in files:
                if not file.startswith('datadiri.txt') and file.endswith('.wav'):
                    wav_names.append(file)
        return wav_names

    def separatorTalent(self, vt_name):
        separator = {
            "ach159": "-",
            "agu101": "-",
            "ind033": "-",
        }
        return separator.get(vt_name, "nothing")

    def wavDict(self, wav_names):
        wav_dict = {}
        for wav in wav_names:
            wav_dict['file'].append(wav)
        # col_names = []
        # for wav in wav_names:
        #     col_name = wav.split('_')[4]
        #     col_names.append(col_name)
        # col_names = sorted(list(set(col_names)))
        # for col in col_names:
        #     wav_dict[col] = []
        #     for wav in wav_names:
        #         transcript = wav.split('_')[4]
        #         if col == transcript:
        #             wav_dict[col].append(wav)
        # return wav_dict


                
    # count .wav per vt_names (as directory), return wav count
    def wavCount(self, vt_path):
        # os.chdir(vt_name)
        # count_dict = {}
        # cnt = collections.Counter()
        # for filename in glob.glob(os.path.join(vt_path,"*.wav")):
        #     try:
        #         name, ext = os.path.splitext(filename)
        #         cnt[ext] += 1
        #     except:
        #         print("no file exist")
        # # count_dict['username'] = vt_name
        # # count_dict['jumlah file'] = cnt[ext]
        # # print(cnt[ext])
        # return cnt[ext]
        count_wav = 0
        for root, dirs, files in os.walk(vt_path):
            for file in files:
                if file.endswith('.wav'):
                    count_wav += 1
        return count_wav

    def fileLength(self, file_wav):
        duration = librosa.get_duration(filename=file_wav)
        return duration

    def wavDuration(self, path_vt, vt_name):
        duration = 0
        duration_menit = 0
        duration_jam = 0
        jumlah_baris = 0
        total_duration_jam = 0
        total_duration_menit = 0
        total_jumlah_baris = 0
        # progress print per nama_vt
        print("Processing:", vt_name)
        for root, dirs, files in os.walk(path_vt):
            for index, filename in enumerate(files, start=1):
            #     # masukkan ke list dulu agar tidak duplikasi.
            #     if filename.endswith(".wav") and nama_vt in root:
            #         file_wav = os.path.join(root, filename)
            #         list_audio_vt.append(filename)
            # list_audio_vt = sorted(list(set(list_audio_vt)))
            # for audio_file in list_audio_vt:
                # print (os.path.join(root,audio_file))
                # cek berdasarkan nama talent dan .wav
                if filename.endswith(".wav"):
                    file_wav = root + "/" + filename
                    try:
                        # duration = librosa.get_duration(filename=file_wav)
                        file_duration = librosa.get_duration(filename=file_wav)
                        duration = duration + file_duration
                        jumlah_baris += 1
                    except:
                        print(filename+' error')
        duration_jam = round(duration/3600, 2)
        duration_menit = round(duration/60, 2)   
        total_duration_menit += duration_menit   
        total_duration_jam += duration_jam
        return total_duration_jam


if __name__ == '__main__':
    path = 'C:/Users/jalerse/Downloads/data_hp'
    main = Main()
    # >> XLSX Writer
    xlsx_file = "handphone_count.xlsx"
    writer = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
    vt_names = main.openDir(path)
    # dict_counts = pd.DataFrame(columns=['username', 'jumlah file'])
    # dict_counts = {}
    for vt_name in vt_names:
        path_vt = os.path.join(path, vt_name)
        # > masuk ke sheet hitung
        talent_dict = {}
        count_dict = main.wavCount(path_vt)
        wav_names = main.wavList(path_vt)
        wav_durasi = main.wavDuration(path_vt, vt_name)
        talent_dict['jumlah file'] = []
        talent_dict['jumlah file'].append(count_dict)
        talent_dict['file'] = []
        for wav in wav_names:
            talent_dict['file'].append(wav)
        talent_dict['durasi (jam)'] = []
        talent_dict['durasi (jam)'].append(wav_durasi)

        talent_excel = pd.DataFrame.from_dict(talent_dict, orient='index')
        talent_excel = talent_excel.transpose()
        talent_excel.to_excel(writer, sheet_name=vt_name)
    writer.save()
        # count_dict = pd.DataFrame(count_dict)
        # talent_dict = pd.DataFrame.from_dict(count_dict, orient='index')
        # talent_dict = talent_dict.transpose()
        # talent_dict.to_excel(writer, sheet_name="")
        # dict_count = {'username':vt_name, 'jumlah file':wav_count}
        # dict_counts = dict_counts.update(dict_count)
 
    # path_vt = os.path.join(path, vt_names[0])
    # wav_names = main.wavList(path_vt)
    

    # vt_names = main.openDir(path)
    # >> XLSX Writer
    # xlsx_file = "output.xlsx"
    # writer = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
    # for vt_name in vt_names:
    #     wav_names = main.wavList(vt_name, path)
    #     wav_dict = main.wavDict(wav_names)

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