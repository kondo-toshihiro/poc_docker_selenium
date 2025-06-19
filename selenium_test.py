#!/usr/bin/env python3
"""
Selenium Edge Driver Test Script
Google Japan のページを表示するテスト
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_google_japan():
    # Edge オプションの設定
    edge_options = Options()
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    
    # リモートWebDriverの設定（Docker Compose環境対応）
    import os
    selenium_hub_url = os.getenv('SELENIUM_HUB_URL', 'http://localhost:4444/wd/hub')
    driver = webdriver.Remote(
        command_executor=selenium_hub_url,
        options=edge_options
    )
    
    try:
        print("Google Japan にアクセス中...")
        # Google Japan のページを開く
        driver.get("https://www.google.co.jp")
        
        # ページタイトルを取得
        title = driver.title
        print(f"ページタイトル: {title}")
        
        # 検索ボックスが表示されるまで待機
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        print("検索ボックスが見つかりました")
        
        # 検索テストを実行
        search_box.send_keys("Docker Selenium テスト")
        search_box.submit()
        
        # 検索結果ページのタイトルを取得
        WebDriverWait(driver, 10).until(
            EC.title_contains("Docker Selenium テスト")
        )
        
        print(f"検索結果ページタイトル: {driver.title}")
        print("テスト成功！Google Japan のページが正常に表示され、検索も実行されました。")
        
        # 10秒間ページを表示したままにする（VNCで確認可能）
        print("10秒間ページを表示します（VNC http://localhost:7900 で確認可能）...")
        time.sleep(10)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    finally:
        # ブラウザを閉じる
        driver.quit()
        print("ブラウザを閉じました")

if __name__ == "__main__":
    test_google_japan()
