from tkinter import *
from pytube import YouTube
from tkinter import filedialog, messagebox
from pytube import Playlist
from moviepy.editor import *
import os
import re

saving_path = ""   # global variable for download path

# functions


def download(v_url, path, type_mp3_mp4):
    yt = YouTube(v_url)

    if type_mp3_mp4 == 1:   # if mp3 check box is selected
        video = yt.streams.filter(file_extension='mp4').first()   # gets the first mp4 stream

        # converting mp4 to mp3
        video_file = VideoFileClip(video.download(path))
        audio_file = video_file.audio
        audio_file.write_audiofile(f"{re.findall(r'(.+).mp4', str(video.download(path)))[0]}.mp3")
        video_file.close()
        audio_file.close()

        os.remove(str(video.download(path)))   # deletes mp4 file

    else:
        video = yt.streams.get_highest_resolution()
        video.download(path)
        # if mp3 check box is not selected downloads video


def download_path():
    global saving_path

    save_path = filedialog.askdirectory(title="Where to save")
    if save_path == "":
        saving.config(fg="red", text="Please enter a save path")   # if there is no saving path

    else:
        saving.config(fg="green", text=f"Videos will be downloaded in:\n{save_path}")   # if there is a saving path
        saving_path = save_path


def video_download():
    video_url = url.get()   # gets the url
    save_path = saving_path   # gets the saving path
    type_download = check_var.get()   # gets type of download (one video or playlist)
    mp3_or_video = mp3_var.get()   # gets info about mp3 check box

    if type_download == 0:   # if type download is a one video
        try:
            download(video_url, save_path, mp3_or_video)

            messagebox.showinfo("Done", "Download complete")
            # message box - done if download is complete

        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Video could not be downloaded")
            # error if video cannot be downloaded

    elif type_download == 1:   # if type download is playlist
        try:
            playlist = Playlist(video_url)   # gets all urls in the playlist

            video_count = 0   # variable for how many videos are in the playlist
            video_downloaded = 0   # variable for how many videos are downloaded

            # adding a txt file for unsuccessfully downloaded videos
            f = open(f"{save_path}/Videos.txt", "w+")
            f.truncate(0)
            f.write(f"Video URLs:\n")
            f.close()

            for video in playlist.video_urls:
                video_count += 1
                try:
                    download(video, save_path, mp3_or_video)

                    video_downloaded += 1

                except Exception as e:
                    f = open(f"{save_path}/Videos.txt", "a+")
                    f.write(f"{video}\n")
                    f.close()
                    # writes the video url if download is unsuccessful

                    print(e)

            if video_downloaded == video_count:
                messagebox.showinfo("Done", "All videos have been downloaded")
                # if all videos from the playlist are downloaded

            else:
                messagebox.showinfo("Not all videos have been downloaded",
                                    f"Downloaded {video_downloaded} videos out of {len(playlist.video_urls)}.\n"
                                    f"Please check the videos.txt file to get all the URLs"
                                    f" from the non-downloaded videos")
                # if not all videos is downloaded

        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Playlist could not be downloaded")
            # error if playlist cannot be found


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
check_var = IntVar()
mp3_var = IntVar()

# entry
Entry(master, width=50, textvariable=url).grid(sticky=N, row=4)

# buttons
Button(master, width=20, text="Where to save", font="Times 13", command=download_path).grid(sticky=N, row=1, pady=10)

Checkbutton(master, width=20, text="Download mp3", font="Times 12", variable=mp3_var).grid(sticky=N, row=5)
Checkbutton(master, width=20, text="Download playlist", font="Times 12", variable=check_var).grid(sticky=N, row=6)

Button(master, width=20, text="Download", font="Times 12", command=video_download).grid(sticky=N, row=7, pady=10)

master.mainloop()
