import os
import sys
import requests
import zipfile
import shutil
from pathlib import Path
import logging
from datetime import datetime

class EdgeDriverUpdater:
    def __init__(self):
        self.driver_path = Path(r"C:\Python")
        self.download_path = Path(r"C:\temp")
        self.edge_version = "131.0.2903.70"
        
        # 必要なディレクトリを作成
        self.driver_path.mkdir(exist_ok=True)
        self.download_path.mkdir(exist_ok=True)

    def check_driver_exists(self) -> bool:
        """ドライバーが存在するかチェック"""
        driver_file = self.driver_path / "msedgedriver.exe"
        return driver_file.exists()

    def download_driver(self) -> bool:
        """Edgeドライバーをダウンロード"""
        try:
            driver_url = f"https://msedgedriver.azureedge.net/{self.edge_version}/edgedriver_win64.zip"
            zip_path = self.download_path / "edgedriver_win64.zip"
            
            logging.info(f"Downloading from: {driver_url}")
            print(f"Downloading EdgeDriver from: {driver_url}")
            
            response = requests.get(driver_url, timeout=30)
            response.raise_for_status()
            
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            logging.info("Driver downloaded successfully")
            return True
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error while downloading driver: {str(e)}")
            print(f"HTTPエラー: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Driver download failed: {str(e)}")
            print(f"ダウンロードエラー: {str(e)}")
            return False

    def extract_and_install_driver(self) -> bool:
        """ドライバーを展開してインストール"""
        try:
            zip_path = self.download_path / "edgedriver_win64.zip"
            
            # 既存のドライバーを削除
            target_driver = self.driver_path / "msedgedriver.exe"
            if target_driver.exists():
                os.remove(target_driver)
                logging.info("Removed existing driver")
            
            # 新しいドライバーを展開
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.download_path)
            logging.info("Extracted driver files")
            
            # ドライバーを移動
            temp_driver = self.download_path / "msedgedriver.exe"
            shutil.move(str(temp_driver), str(target_driver))
            logging.info("Moved driver to target location")
            
            # クリーンアップ
            if zip_path.exists():
                os.remove(zip_path)
                logging.info("Cleaned up temporary files")
            
            return True
        except Exception as e:
            logging.error(f"Driver installation failed: {str(e)}")
            print(f"インストールエラー: {str(e)}")
            return False

    def update_driver(self) -> bool:
        """ドライバーの更新プロセスを実行"""
        try:
            print(f"Installing EdgeDriver version {self.edge_version}")
            logging.info(f"Starting update for EdgeDriver version {self.edge_version}")
            
            # ドライバーが存在しない場合、または更新が要求された場合
            if not self.check_driver_exists():
                print("EdgeDriverが見つかりません。新規インストールを実行します。")
                logging.info("EdgeDriver not found. Performing new installation.")
                
                if not self.download_driver():
                    return False
                    
                if not self.extract_and_install_driver():
                    return False

                print("EdgeDriverの新規インストールが完了しました。")
                logging.info("New installation completed successfully")
                return True
            else:
                print("EdgeDriverは既に存在します。更新をスキップします。")
                logging.info("EdgeDriver already exists. Skipping update.")
                return True

        except Exception as e:
            logging.error(f"Update process failed: {str(e)}")
            print(f"更新プロセスエラー: {str(e)}")
            return False


def main():
    try:
        updater = EdgeDriverUpdater()
        if updater.update_driver():
            print("処理が正常に完了しました。")
        else:
            print("処理中にエラーが発生しました。ログを確認してください。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        logging.error(f"Fatal error: {e}")


if __name__ == "__main__":
    # ロギングの設定
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=log_dir / f"edge_driver_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    main()