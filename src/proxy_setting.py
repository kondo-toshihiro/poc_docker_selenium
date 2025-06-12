import tkinter as tk
import requests
from requests.exceptions import ConnectTimeout
import os

from src import env_variables as env

# ---------------------------------------------------------------------------------------------
# proxy setting
# ---------------------------------------------------------------------------------------------
# $env:https_proxy = "http://j063514:passowrd@www-n.ddreams.jp:8080"
# $env:http_proxy = "http://j063514:passowrd@www-n.ddreams.jp:8080"


def input_proxy_setting() -> None:
    """プロキシ設定が必要な場合はGUIで入力を求める"""
    if env.IS_INTRANET and os.getenv('https_proxy') is None:
        ddreams_login()
    while True:
        try:
            if requests.get('https://www.google.com', timeout=5).status_code == 200:
                return
        except (ConnectTimeout, requests.exceptions.ConnectionError):
            ddreams_login()


def ddreams_login() -> None:
    root = tk.Tk()
    root.title('プロキシ認証設定')
    root.geometry('300x80')

    input_id_label = tk.Label(text='ログインID')
    input_id_label.grid(row=1, column=1, padx=10)

    input_id = tk.Entry(width=30)
    input_id.grid(row=1, column=2)

    input_pass_label = tk.Label(text='パスワード')
    input_pass_label.grid(row=2, column=1, padx=10)

    input_pass = tk.Entry(show='*', width=30)
    input_pass.grid(row=2, column=2)

    button = tk.Button(text='ログイン', command=lambda: close_window(root, input_id, input_pass))
    button.place(x=140, y=50)

    def close_window(root, input_id, input_pass) -> None:
        set_proxy(user_id=input_id.get(), password=input_pass.get())
        root.destroy()
    root.mainloop()


def set_proxy(user_id: str, password: str) -> None:
    proxy = f"http://{user_id}:{password}@www-n.ddreams.jp:8080"
    os.environ['https_proxy'] = proxy
    os.environ['http_proxy'] = proxy
