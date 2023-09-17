import threading
import tkinter as tk
from tkinter import filedialog, ttk
from moviepy.editor import VideoFileClip
import pygame
from pygame.locals import *
import time


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

        # 创建倍速选择框
        self.speed_label = tk.Label(root, text="选择倍速:")
        self.speed_label.pack()
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient="horizontal",
                                    variable=self.speed_var)
        self.speed_scale.pack()

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

            # 初始化Pygame音频
            pygame.mixer.quit()
            pygame.mixer.init()

            # 播放视频和音频
            self.is_playing = True
            self.playing_thread = threading.Thread(target=self.play_video_thread)
            self.playing_thread.start()

    def play_video_thread(self):
        pygame.display.init()
        screen = pygame.display.set_mode((1280, 720), RESIZABLE)
        pygame.display.set_caption("视频播放器")

        clock = pygame.time.Clock()

        current_time = 0
        self.video_clip.set_duration(self.video_clip.duration * (1 / self.speed_var.get()))

        while self.is_playing and current_time < self.video_clip.duration:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.is_playing = False

            frame = self.video_clip.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (0, 0))
            pygame.display.flip()

            self.update_progress_bar(current_time)
            current_time += 0.03  # 播放速度

            clock.tick(30)

        pygame.quit()
        pygame.mixer.quit()

    def update_progress_bar(self, current_time):
        progress = (current_time / self.video_clip.duration) * 100
        self.progress_bar["value"] = progress

    def pause_video(self):
        self.is_playing = False


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)

    # 创建进度条
    app.progress_label = tk.Label(root, text="进度:")
    app.progress_label.pack()
    app.progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
    app.progress_bar.pack()

    root.mainloop()
