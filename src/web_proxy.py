# web_proxy.py の修正
import tkinter as tk
import requests
import os
from requests.exceptions import RequestException


def setup_proxy():
    """プロキシの設定"""
    def check_connection():
        """プロキシ設定の確認"""
        try:
            response = requests.get('https://www.google.com', timeout=5)
            return response.status_code == 200
        except RequestException:
            return False

    # プロキシが既に設定されており、接続も成功する場合
    if os.getenv('https_proxy') and check_connection():
        return True
        
    # プロキシ設定ダイアログの表示
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

    def close_window():
        proxy = f"http://{input_id.get()}:{input_pass.get()}@www-n.ddreams.jp:8080"
        os.environ['https_proxy'] = proxy
        os.environ['http_proxy'] = proxy
        root.destroy()

    button = tk.Button(text='ログイン', command=close_window)
    button.place(x=140, y=50)
    
    root.mainloop()

    # プロキシ設定後に接続確認
    return check_connection()
