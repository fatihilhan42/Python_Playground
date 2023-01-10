import tkinter as tk
from tkinter import filedialog, PhotoImage
import youtube_dl
import tkinter.ttk as ttk 
import threading
import time

class App:
    def __init__(self, root):
        self.root = root
        self.init_gui()

    def init_gui(self):

        # Set window size
        self.root.title("Youtube Downloader")
        self.root.geometry("1280x720")
        self.root.configure(bg="#C780FA")
        self.thread = None

        # Add YouTube logo
        self.logo_frame = tk.Frame(self.root)
        self.logo_frame.pack_propagate(False)
        self.logo2 = PhotoImage(file="Youtube_logo.png")
        self.logo2 = self.logo2.zoom(2)
        self.logo2 = self.logo2.subsample(4)
        self.logo_label = tk.Label(self.root, image=self.logo2,bg="#FF0000")
        self.logo_label.pack()

        # Add logo and text to bottom corner
        self.logo = PhotoImage(file="my_logo.png")
        self.logo = self.logo.zoom(2)
        self.logo = self.logo.subsample(10)
        self.logo_label = tk.Label(self.root, image=self.logo)
        self.logo_label.place(relx=1, rely=1, anchor="se")
        self.text = tk.Label(self.root, text="Created By", font=("Arial", 12), bg="#DC0000")
        self.text.place(relx=0, rely=1, anchor="sw")
        

        # Create URL field
        self.url_label = tk.Label(self.root, text="Enter YouTube URL:", bg="#C780FA")
        self.custom_font = ("Arial", 16)
        self.url_label.config(font=self.custom_font)
        self.url_label.pack()
        self.url_entry = tk.Entry(self.root)
        self.url_entry.config(font=self.custom_font, width=50)
        self.url_entry.pack(padx=10 , pady=10)

        # Create save location field
        self.save_label = tk.Label(self.root, text="Choose save location:", font=("Arial", 14), bg="#C780FA")
        self.save_label.config(font=self.custom_font)
        self.save_label.pack(padx=10 , pady=10)
        self.save_button = tk.Button(self.root, text="Browse", command=self.choose_save_location, bg="#FF0032",relief=tk.RAISED)
        self.save_button.config(font=self.custom_font)
        self.save_button.pack()
        self.save_location = tk.Label(self.root, text="", bg="#C780FA",font=("Arial", 12))
        self.save_location.pack(padx=10 , pady=10)

        # Create format options
        self.format_label = tk.Label(self.root, text="Choose format:", font=("Arial", 14), bg="#C780FA")
        self.format_label.pack()
        self.format_var = tk.StringVar(self.root)
        self.format_var.set("mp4")
        self.format_option = tk.OptionMenu(self.root, self.format_var, "mp3", "mp4",)
        self.format_option.config(font=("Arial", 12),bg="#C780FA")
        self.format_option.pack(padx=10 , pady=10)

        # Create quality options
        self.quality_label = tk.Label(self.root, text="Choose quality (for mp4 only):", bg="#FF0032", font=("Arial", 14))
        self.quality_label.config(font=self.custom_font)
        self.quality_label.pack()
        self.quality_var = tk.StringVar(self.root)
        self.quality_var.set("720p")
        self.quality_option = tk.OptionMenu(self.root, self.quality_var, "240p", "360p", "480p", "720p", "1080p")
        self.quality_option.config(font=("Arial", 12),bg="#C780FA")
        self.quality_option.pack(padx=10 , pady=10)

        # Create download button
        self.download_button = tk.Button(self.root, text="Download", command=self.download, bg="#FF0032", relief=tk.RAISED)
        self.download_button.config(font=self.custom_font, width=20)
        self.download_button.pack(padx=10 , pady=10)

    def get_progress(self):
        # Get progress of download
        ydl = youtube_dl.YoutubeDL({"quiet": True})
        with ydl:
            info_dict = ydl.extract_info(self.url_entry.get(), download=True)
            return info_dict["progress_percent"]

    def choose_save_location(self):
        self.save_location_text = filedialog.askdirectory()
        self.save_location.config(text=self.save_location_text)

    def download(self):
            # Get download options
        url = self.url_entry.get()
        save_location = self.save_location_text
        format = self.format_var.get()
        quality = self.quality_var.get()

        # Set download options
        ydl_opts = {}
        if format == "mp4":
            ydl_opts = {
                "format": f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
                "outtmpl": f"{save_location}/%(title)s.%(ext)s",
                "quiet": True
            }
        elif format == "mp3":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"{save_location}/%(title)s.%(ext)s",
                "quiet": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
            }

        # Start download
        def start_download():
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    info_dict = ydl.extract_info(url, download=False)
                    video_title = info_dict.get("title", None)
                tk.messagebox.showinfo("Success", f"{video_title} was downloaded successfully!")
                self.root.destroy()
            except Exception as e:
                tk.messagebox.showerror("Error", e)

        # Start download in a new thread to allow for progress bar updates
        self.thread = threading.Thread(target=start_download)
        self.thread.start()

        self.root.after(100,self.update_progress)

        
       # Create progress bar
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress, maximum=100)
        self.progress_bar.pack(padx=10, pady=10)
        

    def update_progress(self):
        if self.thread.is_alive():
            self.progress.set(self.get_progress())
            self.root.after(100, self.update_progress)
        else:
            self.root.update_idletasks()

        # Reset fields
        self.url_entry.delete(0, "end")
        self.save_location_text = ""
        self.save_location.config(text="")
        self.format_var.set("mp4")
        self.quality_var.set("720p")

        # Update progress bar
        self.root.after(100, self.update_progress)

# Run program
root = tk.Tk()
app = App(root)
root.mainloop()
