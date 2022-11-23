from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import threading

##needs thread constructor and exception handling (push them to the text box inside root)##

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    root.title((str(int(percentage_of_completion))) + '%')

def get_path():
    path = filedialog.askdirectory()
    path_entry.delete(0, 'end')
    path_entry.insert(0,str(path))
    
def download_file(path, link):
    root.title('Downloading...')
    chunk_size = 1024
    yt = YouTube(link)
    video = yt.streams.get_highest_resolution()
    yt.register_on_progress_callback(on_progress)
    info_box.configure(state='normal')
    info_box.insert(1.0, f"Fetching \"{video.title}\".. \n")
    info_box.insert(2.0, f"Fetching successful\n")
    info_box.insert(3.0, f"Information: \n"
          f"File size: {round(video.filesize * 0.000001, 2)} MegaBytes\n"
          f"Highest Resolution: {video.resolution}\n"
          f"Author: {yt.author}\n")
    info_box.insert(4.0, "Views: {:,}\n".format(yt.views))
    info_box.configure(state='disabled')
    video.download(path)  
    root.title("Done.")

root = Tk()
root.title('yt_dlp 720p')

path_entry = Entry(root, width=50)
path_entry.grid(row=0,column=0)
path_entry.insert(0, 'C:/')

get_path_button = Button(root, text='Get Path', command=lambda:get_path())
get_path_button.grid(row=1, column=0, ipadx=5)

url_entry = Entry(root, width=50)
url_entry.grid(row=2, column=0)
url_entry.bind("<Button-1>", lambda e: url_entry.delete(0, 'end'))
url_entry.insert(0, "URL")

download_button = Button(root, text='Download', command=threading.Thread(
    target=lambda:download_file(path_entry.get(), url_entry.get())).start)
download_button.grid(row=3,column=0, ipadx=5)


info_box = Text(root, wrap='word', state='disabled', width=38, height=10)
info_box.grid(row=4, column=0)

root.mainloop()
