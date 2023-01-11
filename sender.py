# import library
import socket
import PySimpleGUI as sg

# membuat GUI untuk input file user
def gui_input():
    sg.theme("DarkTeal2")

    # membuat layout input
    layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(), 
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),),key="-IN-")],[sg.Button("Submit")], [sg.Button("Exit")]]

    # Building Window
    window = sg.Window('Input File', layout, size=(600,150))
    
    while True:
        # menjalankan window
        event, values = window.read()

        # jika user menekan Exit atau close window maka akan break code
        if event == sg.WIN_CLOSED or event=="Exit":
            break

        # jika user menekan submit maka akan return value yang di inputkan user
        elif event == "Submit":
            window.close()
            return values["-IN-"]
        
        
# membuat GUI untuk menampilkan hasil dari penghitungan plagiarisme
def gui_show(text):
    # membuat layout hasil
    layout = [[sg.Button(text, size=(300,8))], [sg.Button("Ok", size=(300,5))]]

    # building window
    window = sg.Window('Plagiarism Checker', layout, size=(400,200))

    # menjalankan window
    event, values = window.read()

    # jika user menekan ok atau close window maka window akan tertutup
    if event == sg.WIN_CLOSED or event=="Ok":
        window.close()

# deklarasi ip local
ip = "192.168.10.10"

# deklarasi port
port = 5055

# deklarasikan socket
sc = socket.socket()

# mencoba untuk menyambukan dengan server
try:
    sc.connect((ip,port))
except:
    print("sambungan gagal: (")

while 1:
    # menjalankan GUI input dan menyimpan kembaliannya dalam variabel nama_file
    nama_file = gui_input()

    # ketika nama_file kosong maka GUI input akan diulang
    while nama_file == '':
        sg.popup("tidak ada file yang dipilih!")
        nama_file = gui_input()

    # membuka file yang telah di inputkan dan encoding file tersebut menjadi sebuah text
    with open(nama_file, "r", encoding='utf-8-sig') as f:
        file = f.read()
    pesan = file.encode()

    # mengirim file tersebut dalam bentuk text
    sc.send(pesan)

    # menampilkan popup untuk loading
    sg.popup_no_buttons("Menghitung...", auto_close=True, auto_close_duration=8.0)

    # menerima kembali nilai plagiarisme yang sudah di hitung oleh server
    inbox = sc.recv(1000000)
    inbox = inbox.decode()

    # menampilkan nilai plagiarisme kepada user
    gui_show(inbox)
    