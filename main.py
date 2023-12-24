# -*- coding: utf8 -*-
# import sound_text
# import split_sound
import tkinter as tk
from tkinter import filedialog
import os
import json

class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        
        self.load_data()
        
        self.master: tk.Tk
        self.master.geometry("550x200") 
        
        #---------------------------------------
        #  オプションフレーム
        #---------------------------------------
        self.show_option_frame()
        self.show_main_frame()

    def show_main_frame(self):
        """メインフレームの表示
        """
        self.frame_main: tk.Frame = tk.Frame(self.master)
        self.button_split_sound: tk.Button = tk.Button(self.frame_main, text="1.音声ファイル分割", width=15, command=self.split_sound)
        self.button_split_sound.grid(row=0, column=0)
        
        
        self.frame_main.pack(fill = tk.X)
    
    def split_sound(self):
        pass
        
    
    def show_option_frame(self):
        """設定フレームの表示
        """
        # オプションFrame
        self.frame_option: tk.Frame = tk.Frame(self.master)
        self.label_option_group: tk.Label = tk.Label(self.frame_option, text="■設定")
        self.label_option_group.grid(row=0, column=0)
        # OpenAI APIキー入力欄        
        self.label_open_ai_key: tk.Label = tk.Label(self.frame_option, text="OpenAI APIキー", anchor=tk.E)
        self.strvar_open_ai_key: tk.StringVar = tk.StringVar()
        if self.open_ai_key != "": self.strvar_open_ai_key.set(self.open_ai_key)
        self.entry_open_ai_key: tk.Entry = tk.Entry(self.frame_option, width = 50, show="*", textvariable=self.strvar_open_ai_key)
        
        self.label_open_ai_key.grid(row=1, column=0)
        self.entry_open_ai_key.grid(row=1, column=1)
        
        # 音声ファイル選択
        self.label_sound_file: tk.Label = tk.Label(self.frame_option, text="音声ファイル", anchor=tk.E)
        self.strvar_sound_file: tk.StringVar = tk.StringVar()
        if self.sound_file_path != "": self.strvar_sound_file.set(self.sound_file_path)
        self.entry_sound_file: tk.Entry = tk.Entry(self.frame_option, width = 50, textvariable=self.strvar_sound_file)
        self.button_sound_file: tk.Button = tk.Button(self.frame_option, text="参照", width=10, command=self.select_sound_file)
        
        self.label_sound_file.grid(row=2, column=0)
        self.entry_sound_file.grid(row=2, column=1)
        self.button_sound_file.grid(row=2, column=2)
        
        # エンコードファイル保存先
        self.label_encode_dir: tk.Label = tk.Label(self.frame_option, text="エンコードファイル保存先", anchor=tk.E)
        self.strvar_encode_dir: tk.StringVar = tk.StringVar()
        if self.encode_dir != "": self.strvar_encode_dir.set(self.encode_dir)
        self.entry_encode_dir: tk.Entry = tk.Entry(self.frame_option, width = 50, textvariable=self.strvar_encode_dir)
        self.button_encode_dir: tk.Button = tk.Button(self.frame_option, text="参照", width=10, command=self.select_encode_dir)
        
        self.label_encode_dir.grid(row=3, column=0)
        self.entry_encode_dir.grid(row=3, column=1)
        self.button_encode_dir.grid(row=3, column=2)
        
        # 保存ボタン
        self.button_open_ai_key: tk.Button = tk.Button(self.frame_option, text="保存", width=10, command=self.save_btn_click)
        self.button_open_ai_key.grid(row=4, column=0, columnspan=3, sticky=tk.SE)
        
        self.frame_option.pack(fill = tk.X)

    def load_data(self):
        self.user_dir: str = ".\\user\\"
        self.user_file: str = "user.dat"

        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

        self.open_ai_key: str = ""
        self.sound_file_path: str = ""
        self.encode_dir: str = ""

        # user_dirにuser_fileが存在するか
        if os.path.exists(self.user_dir + self.user_file):
            # 存在する場合はファイルを開いてキーを取得
            with open(self.user_dir + self.user_file) as f:
                json_text: str = f.read()
                json_data = json.loads(json_text)
                if "open_ai_key" in json_data:
                    self.open_ai_key = json_data["open_ai_key"]
                if "sound_file_path" in json_data:
                    self.sound_file_path = json_data["sound_file_path"]
                if "encode_dir" in json_data:
                    self.encode_dir = json_data["encode_dir"]
    
    def save_btn_click(self):
        self.open_ai_key = self.strvar_open_ai_key.get()
        self.sound_file_path = self.strvar_sound_file.get()
        self.encode_dir = self.strvar_encode_dir.get()
        # user_dirにuser_fileに保存する
        with open(self.user_dir + self.user_file, mode='w') as f:
            json_data = {"open_ai_key": self.open_ai_key, "sound_file_path": self.sound_file_path, "encode_dir": self.encode_dir}
            f.write(json.dumps(json_data))
    
    def select_sound_file(self):
        file = filedialog.askopenfile(initialdir='~/', filetypes=[("音声ファイル", "*.wav")])
        if file != None:
            self.sound_file_path = file.name
            
            self.strvar_sound_file.set(self.sound_file_path)
    
    def select_encode_dir(self):
        dir = filedialog.askdirectory(initialdir='~/', mustexist=True)
        if dir != None:
            self.encode_dir = dir
            
            self.strvar_encode_dir.set(self.encode_dir)

if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    photo: tk.PhotoImage = tk.PhotoImage(file="./img/icon.png")  
    root.iconphoto(False, photo)
    app: Application = Application(master = root)
    app.mainloop()