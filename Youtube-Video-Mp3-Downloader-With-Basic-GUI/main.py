from tkinter import *
from pytube import YouTube
from tkinter import filedialog, messagebox
from pytube import Playlist
from moviepy.video.io import ffmpeg_tools
import os

# functions


def download_path():
    global saving_path

    save_path = filedialog.askdirectory(title="Where to save")
    if save_path == "":
        saving.config(fg="red", text="Please enter a save path")

    else:
        saving.config(fg="green", text=f"Videos will be downloaded in:\n{save_path}")
        saving_path = save_path


def video_download():
    video_url = url.get()
    download = saving_path
    type_download = check_var.get()
    mp3_or_video = mp3_var.get()

    if type_download == 0:
        try:
            yt = YouTube(video_url)

            if mp3_or_video == 1:
                video = yt.streams.get_audio_only()
                video.download(download)

                ffmpeg_tools.ffmpeg_extract_audio(video.download(download), f"{download}/{yt.title}.mp3")
                os.remove(f"{video.download(download)}")

            else:
                video = yt.streams.get_highest_resolution()
                video.download(download)

            messagebox.showinfo("Done", "Download complete")

        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Video could not be downloaded")

    elif type_download == 1:
        try:
            playlist = Playlist(video_url)
            download = saving_path
            video_count = 0
            video_downloaded = 0

            f = open(f"{download}/Videos.txt", "w+")
            f.truncate(0)
            f.write(f"Video URLs:\n")
            f.close()

            for video in playlist.video_urls:
                video_count += 1
                try:
                    yt = YouTube(video)

                    if mp3_or_video == 1:
                        video = yt.streams.get_audio_only()
                        video.download(download)

                        ffmpeg_tools.ffmpeg_extract_audio(video.download(download), f"{download}/{yt.title}.mp3")
                        os.remove(f"{video.download(download)}")

                    else:
                        video = yt.streams.get_highest_resolution()
                        video.download(download)

                    video_downloaded += 1

                except Exception as e:
                    f = open(f"{download}/Videos.txt", "a+")
                    f.write(f"{video}\n")
                    f.close()

                    print(e)

            if video_downloaded == video_count:
                messagebox.showinfo("Done", "All videos have been downloaded")

            else:
                messagebox.showinfo("Not all videos have been downloaded",
                                    f"Downloaded {video_downloaded} videos out of {len(playlist.video_urls)}.\n"
                                    f"Please check the videos.txt file to get all the URLs"
                                    f" from the non-downloaded videos")

        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Playlist could not be downloaded")


# main screen
master = Tk()
master.title("Youtube downloader")
master.resizable(width=False, height=False)

# labels
Label(master, text="Youtube Downloader", fg="red", font="Times 30").grid(sticky=N, row=0, padx=70)

saving = Label(master, font="Times 15", fg="red", text="Please enter a save path")
saving.grid(sticky=N, pady=1, row=2)

Label(master, text="Enter your youtube link: ", font="Times 20").grid(sticky=N, row=3, pady=10)

# vars
url = StringVar()
saving_path = ""
check_var = IntVar()
mp3_var = IntVar()

# entry
Entry(master, width=50, textvariable=url).grid(sticky=N, row=4)

# button
Button(master, width=20, text="Where to save", font="Times 13", command=download_path).grid(sticky=N, row=1, pady=10)
Checkbutton(master, width=20, text="Download mp3", font="Times 12", variable=mp3_var).grid(sticky=N, row=5)
Checkbutton(master, width=20, text="Download playlist", font="Times 12", variable=check_var).grid(sticky=N, row=6)
Button(master, width=20, text="Download", font="Times 12", command=video_download).grid(sticky=N, row=7, pady=10)
master.mainloop()