import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("视频播放器")

        # 创建视频播放器窗口
        self.video_frame = tk.Frame(root)
        self.video_frame.pack(padx=100, pady=50)

        # 创建视频标题
        self.video_title_label = tk.Label(self.video_frame, text="视频播放器")
        self.video_title_label.pack()

        # 创建选择文件按钮
        self.open_button = tk.Button(root, text="选择视频文件", command=self.open_file)
        self.open_button.pack(pady=10)

        # 创建文件路径标签
        self.file_path_label = tk.Label(root, text="", wraplength=300)
        self.file_path_label.pack()

        # 创建播放按钮
        self.play_button = tk.Button(root, text="播放", command=self.play_video)
        self.play_button.pack()

        # 创建退出按钮
        self.exit_button = tk.Button(root, text="退出", command=root.quit)
        self.exit_button.pack()

        # 初始化视频文件路径和播放状态
        self.video_file_path = ""
        self.is_playing = True

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("视频文件", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.video_file_path = file_path
            # 更新文件路径标签
            self.file_path_label.config(text="文件路径: " + file_path)

    def play_video(self):
        if self.video_file_path:
            video_clip = VideoFileClip(self.video_file_path)
            video_clip = video_clip.resize((1280, 720))
            video_clip.preview(fps=20, audio=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()