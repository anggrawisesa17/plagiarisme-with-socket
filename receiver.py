# import library
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import socket
import numpy as np

# membuka folder database
path = r"C:\Users\Virgo\Documents\semester 5\sister\tubes plagiarism\database"
os.chdir(path)

# fungsi untuk menghitung nilai plagiarisme
def nilai_plagiarisme(text):
    # membaca tiap file yang ada di dalam folder di database
    data = [doc for doc in os.listdir() if doc.endswith('.txt')]

    # membaca seluruh konten yang ada dalam setiap file 
    data_fix = [open(_file, encoding='utf-8').read()
                 for _file in data]

    # memasukkan file yang dikirimkan user ke array yang paling awal
    data_fix.insert(0,text)

    # convert kumpulan text ke dalam matrix
    x = CountVectorizer(encoding='latin-1', binary=False)

    # memelajari kosakata dan mengembalikan matriks
    vector = x.fit_transform(data_fix)

    # menghitung kesamaan file dengan metode cosine_similarity
    cosim = cosine_similarity(vector[0], vector)

    # mengurutkan hasil kesamaan tiap file dari yang terkecil ke yang paling besar nilai plagiarismenya
    urutan = np.argsort(cosim)

    # deklarasi nilai dengan nilai plagiarisme yang paling besar nomor 2, karena nomor 1 adalah file yang dikirimkan user itu sendiri
    nilai = cosim[0][urutan[0][len(data)-1]]

    return nilai * 100

# deklarasi ip local
ip = socket.gethostbyname("192.168.10.10")

# deklarasi port
port = 5055

# deklarasikan socket
sc = socket.socket()

# binding ip dan port yang sudah di deklarasi
sc.bind((ip, port))
print("server diaktifkan")

# menunggu koneksi dari client
sc.listen(5)

# menerima koneksi dari client
conn, addr = sc.accept()
print("terhubung dengan ", addr)

while 1:
    # menerima pesan dari client berupa text
    inbox = conn.recv(1000000)
    inbox = inbox.decode()

    # pesan tersebut di hitung nilai plagiarismenya
    hasil = nilai_plagiarisme(inbox)

    # mengirimkan kembali hasil dari nilai plagiarisme
    pesan2 = "nilai plagiarisme adalah "+ str(hasil)+" %"
    pesan2 = pesan2.encode()
    conn.send(pesan2)

 