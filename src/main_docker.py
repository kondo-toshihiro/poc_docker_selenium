import os
import sys
from pathlib import Path
import time
import json
from datetime import datetime

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    UnexpectedAlertPresentException
)

# ログ出力用の簡易ロガー
class SimpleLogger:
    def info(self, msg):
        print(f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
    
    def error(self, msg):
        print(f"[ERROR] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
    
    def warning(self, msg):
        print(f"[WARNING] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

logger = SimpleLogger()


def setup_edge_driver(headless=True, download_dir=None):
    """Docker Selenium用のEdgeドライバー設定"""
    edge_options = Options()
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--disable-extensions')
    
    if headless:
        edge_options.add_argument('--headless')
    
    if download_dir:
        edge_options.add_experimental_option('prefs', {
            'download.default_directory': download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })

    # Docker Selenium Gridに接続
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=edge_options
    )
    return driver


def create_ini_file():
    """pass_indy.iniファイルが存在しない場合に作成する（WSL用パス）"""
    try:
        # WSL環境用のパスに変更
        ini_path = "/home/user/pass_indy.ini"
        ini_dir = os.path.dirname(ini_path)

        # ディレクトリが存在しない場合は作成
        if not os.path.exists(ini_dir):
            os.makedirs(ini_dir)
            logger.info(f'ディレクトリを作成しました: {ini_dir}')

        if not os.path.exists(ini_path):
            logger.info('pass_indy.iniが見つかりません。ダミーファイルを作成します...')

            # UTF-8でファイルを直接作成
            with open(ini_path, 'w', encoding='utf-8') as f:
                f.write('id,pass,url,dir\n')
                f.write('KD50101311,dengyodengyo-01,https://scm2-indy2010.sumitomocorp.co.jp/lgnj/,/home/user/downloads\n')
                f.write('KD50101312,dengyodengyo-01,https://scm2-indy2010.sumitomocorp.co.jp/lgnj/,/home/user/downloads\n')

            logger.info(f'pass_indy.iniを作成しました: {ini_path}')

            if os.path.exists(ini_path):
                logger.info('ファイルの作成に成功しました')
                return True
            else:
                logger.error('ファイルの作成に失敗しました')
                return False
        else:
            logger.info('pass_indy.iniは既に存在しています')
            return True

    except Exception as e:
        logger.error(f'ファイル作成中にエラーが発生しました: {str(e)}')
        return False


def read_login_info():
    """パスワードファイルからログイン情報を取得する"""
    try:
        ini_path = "/home/user/pass_indy.ini"

        if not create_ini_file():
            logger.error('iniファイルの準備に失敗しました')
            return None

        login_info_list = []
        # UTF-8でファイルを開くように変更
        with open(ini_path, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:  # ヘッダー行をスキップ
                if line.strip():  # 空行をスキップ
                    info = line.strip().split(',')
                    if len(info) >= 4:  # id, pass, url, dirの4項目があることを確認
                        login_info_list.append({
                            'id': info[0],
                            'password': info[1],
                            'url': info[2],
                            'download_dir': info[3]
                        })
        logger.info(f"読み込んだログイン情報数: {len(login_info_list)}")
        return login_info_list
    except Exception as e:
        logger.error(f'ログイン情報の読み込みに失敗しました: {str(e)}')
        return None


def perform_login(driver, wait, login_info):
    """指定されたサイトにログインする"""
    try:
        driver.get(login_info['url'])
        logger.info('webページを開きました')
        logger.info(f'ページタイトル: {driver.title}')

        id_input = wait.until(EC.presence_of_element_located((By.NAME, "IDToken1")))
        id_input.clear()
        id_input.send_keys(login_info['id'])
        logger.info('ログインIDを入力しました')

        password_input = wait.until(EC.presence_of_element_located((By.NAME, "IDToken2")))
        password_input.clear()
        password_input.send_keys(login_info['password'])
        logger.info('パスワードを入力しました')
        time.sleep(2)

        login_button = wait.until(EC.element_to_be_clickable((By.NAME, "login")))
        login_button.click()
        logger.info('ログインボタンをクリックしました')

        wait.until(EC.url_changes(login_info['url']))
        logger.info('ログインに成功しました')

        return True

    except TimeoutException:
        logger.error('要素の待機がタイムアウトしました')
        return False
    except NoSuchElementException:
        logger.error('要素が見つかりませんでした')
        return False
    except Exception as e:
        logger.error(f'ログイン中にエラーが発生しました: {str(e)}')
        return False


def perform_logout(driver, wait):
    """ログアウトを実行する"""
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            logout_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "logout")))
            logout_button.click()
            time.sleep(2)
            logger.info('ログアウトしました')
            return True
        except TimeoutException:
            retry_count += 1
            logger.warning(f'ログアウトボタンの検出に失敗しました（試行 {retry_count}/{max_retries}）')

            if retry_count >= max_retries:
                logger.error('リトライ回数を超過しました。ブラウザを強制終了します。')
                try:
                    current_url = driver.current_url
                    logger.info(f'最終URL: {current_url}')

                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    driver.save_screenshot(f'/home/user/logout_error_{timestamp}.png')
                    logger.info('エラー時のスクリーンショットを保存しました')

                except Exception as e:
                    logger.error(f'デバッグ情報の取得に失敗: {str(e)}')

                return False

            time.sleep(5)
            continue

        except Exception as e:
            logger.error(f'ログアウト中に予期せぬエラーが発生しました: {str(e)}')
            return False
    return False


def open_shipping_info(wait):
    """出荷セクションを開く"""
    try:
        shukka_section = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, r"shukka")))
        shukka_section.click()
        logger.info("出荷セクションをクリックしました")
        return True
    except TimeoutException:
        logger.error("出荷セクションが見つからないか、クリックできない状態です")
        return False
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return False


def open_shipping_info_detale(wait):
    """出荷指示照会メニューを開く"""
    try:
        shipping_menu = wait.until(EC.element_to_be_clickable((By.XPATH, r"/html/body/div[2]/nav/section[5]/ul/li[1]/a")))
        shipping_menu.click()
        logger.info("出荷指示照会メニューをクリックしました")
        return True
    except TimeoutException:
        logger.error("メニュー要素が見つからないか、クリックできない状態です")
        return False
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return False


def open_top_page(driver, login_info):
    """トップページに戻る"""
    driver.get(login_info['url'])
    logger.info('topページに戻りました')


def open_page_csv(driver, wait):
    """出荷指示一覧ページを開いてCSVをダウンロード"""
    try:
        shiplist_button = wait.until(EC.element_to_be_clickable((By.ID, "decision")))
        shiplist_button.click()
        logger.info('出荷指示一覧ボタンをクリックしました')

        wait.until(EC.alert_is_present())
        alert = Alert(driver)
        logger.info(f"アラートメッセージ: {alert.text}")
        alert.accept()
        logger.info('アラートを承認しました')
        time.sleep(3)

        wait.until(lambda d: len(d.window_handles) > 1)
        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)
        logger.info(f"新しいタブに切り替えました: {driver.title}")
        time.sleep(2)

        max_retries = 240
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                update_button = wait.until(EC.element_to_be_clickable((By.ID, "search")))
                update_button.click()
                logger.info("更新・検索ボタンをクリックしました")
                time.sleep(30)

                try:
                    status_cell = driver.find_element(By.XPATH, "/html/body/form/div[4]/table/tbody/tr[3]/td[2]")
                    status_text = status_cell.text.strip()
                    logger.info(f"検出された処理状態: '{status_text}'")

                    if status_text == "ＮＧ":
                        logger.error("処理状態がNGです")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        return False
                    
                    elif status_text == "完了":
                        logger.info("完了状態を検出しました")
                        
                        clip_icon = status_cell.find_element(By.XPATH, "..//a[.//img[contains(@src, 'tenpu.gif')]]")
                        logger.info("クリップアイコンを検出しました")
                        
                        driver.execute_script("arguments[0].click();", clip_icon)
                        logger.info("ダウンロードを開始しました")
                        time.sleep(3)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        return True

                except NoSuchElementException:
                    logger.warning("状態要素が見つかりません")

                retry_count += 1
                logger.info(f"完了待機中... ({retry_count}/{max_retries})")
                time.sleep(5)

            except Exception as e:
                logger.error(f"ループ内でエラー: {str(e)}")
                retry_count += 1
                time.sleep(5)
                continue

        logger.error("処理完了の待機がタイムアウトしました")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return False

    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        logger.error(f"エラーの種類: {type(e).__name__}")
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        return False


def test_google_access():
    """Google Japanへのアクセステスト"""
    driver = None
    try:
        logger.info("=== Google Japan アクセステスト開始 ===")
        driver = setup_edge_driver(headless=True)
        
        driver.get("https://www.google.co.jp")
        logger.info(f"ページタイトル: {driver.title}")
        
        # 結果をJSONで保存
        result = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'url': 'https://www.google.co.jp',
            'title': driver.title,
            'status': 'success'
        }
        
        with open('/home/user/test_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        logger.info("テスト完了 - 結果をJSONファイルに保存しました")
        return True
        
    except Exception as e:
        logger.error(f"テスト中にエラーが発生しました: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()
            logger.info("ブラウザセッション終了")


def login_logout_loop():
    """メインループ処理"""
    driver = None
    try:
        # ログイン情報の読み込み
        login_info_list = read_login_info()
        if not login_info_list:
            logger.error('ログイン情報の読み込みに失敗')
            return False

        logger.info(f"処理対象のサイト数: {len(login_info_list)}")

        # 各サイトに対してログイン/ログアウトを実行
        for i, login_info in enumerate(login_info_list, 1):
            logger.info(f"\n=== {i}つ目のサイトの処理を開始 ===")
            logger.info(f"URL: {login_info['url']}")

            try:
                # ダウンロードディレクトリを指定してドライバーを設定
                driver = setup_edge_driver(headless=True, download_dir=login_info['download_dir'])
                wait = WebDriverWait(driver, 30)

                if perform_login(driver, wait, login_info):
                    time.sleep(3)
                    if not open_shipping_info(wait):
                        logger.error("出荷情報の開封に失敗しました")
                        continue
                    time.sleep(3)
                    if not open_shipping_info_detale(wait):
                        logger.error("出荷情報詳細の開封に失敗しました")
                        continue
                    time.sleep(3)
                    if not open_page_csv(driver, wait):
                        logger.error("CSVページの開封に失敗しました")
                        continue
                    time.sleep(3)

                    open_top_page(driver, login_info)
                    if not perform_logout(driver, wait):
                        logger.warning("ログアウトに失敗しました")

                if driver:
                    driver.quit()
                    driver = None

            except Exception as e:
                logger.error(f'サイト {i} の処理中にエラーが発生: {str(e)}')
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = None
                continue  # 次のサイトの処理へ
        
        logger.info("\n=== 全サイトの処理が完了 ===")
        return True
        
    except Exception as e:
        logger.error(f'予期せぬエラーが発生: {str(e)}')
        if driver:
            try:
                driver.quit()
            except:
                pass
        return False


if __name__ == "__main__":
    logger.info("Docker Selenium RPA プログラムを開始します")
    
    # まずGoogle Japanアクセステストを実行
    if test_google_access():
        logger.info("接続テスト成功 - メイン処理を開始します")
        
        if create_ini_file():
            if login_logout_loop():
                logger.info("プログラムが正常に完了しました")
            else:
                logger.error("メイン処理でエラーが発生しました")
        else:
            logger.error('必要なファイルの準備ができません。プログラムを終了します。')
    else:
        logger.error("接続テストに失敗しました。プログラムを終了します。")
