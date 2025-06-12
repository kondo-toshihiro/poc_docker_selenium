import os
import sys
from dotenv import load_dotenv
import logging

from src import kv_secrets


current_directory = os.path.dirname(sys.argv[0])
dotenv_path = os.path.join(current_directory, '.env')
load_dotenv(dotenv_path)


# ---------------------------------------------------------------------------------------------
# mode config
# ---------------------------------------------------------------------------------------------
__is_debug = os.getenv('PSI_DEBUG_MODE') or "FALSE"
IS_DEBUG = True if __is_debug == "TRUE" else False

__is_intranet = os.getenv('PSI_INTRANET') or "TRUE"
IS_INTRANET = False if __is_intranet == "FALSE" else True

__skip_notify = os.getenv('PSI_SKIP_NOTIFY') or "FALSE"
SKIP_NOTIFY = True if __skip_notify == "TRUE" else False

__log_level = os.getenv('PSI_LOG_LEVEL') or "INFO"
__log_level = __log_level.upper()
LOG_LEVEL = logging.INFO
if __log_level == "DEBUG":
    LOG_LEVEL = logging.DEBUG
elif __log_level == "INFO":
    LOG_LEVEL = logging.INFO
elif __log_level == "WARNING":
    LOG_LEVEL = logging.WARNING
elif __log_level == "ERROR":
    LOG_LEVEL = logging.ERROR
elif __log_level == "CRITICAL":
    LOG_LEVEL = logging.CRITICAL

# ---------------------------------------------------------------------------------------------
# database connection info (*the passwords are for development purpose)
# ---------------------------------------------------------------------------------------------
MSSQL_DEV_HOST = os.getenv('PSI_MSSQL_DEV_HOST') or "127.0.0.1"
MSSQL_PORT = os.getenv('PSI_MSSQL_PORT') or "1433"
MSSQL_USER = os.getenv('PSI_MSSQL_USER') or "sa"
if IS_DEBUG:
    MSSQL_DEV_PASSWORD = os.getenv('PSI_MSSQL_PASSWORD') or ""
else:
    MSSQL_DEV_PASSWORD = kv_secrets.get_db_password()
    if (MSSQL_DEV_PASSWORD is None):
        raise KeyError("MSSQL_DEV_PASSWORD is needed.")

MSSQL_DRIVER = os.getenv('PSI_MSSQL_DRIVER') or "{ODBC Driver 18 for SQL Server}"
MSSQL_DATABASE = os.getenv('PSI_MSSQL_DATABASE') or 'master'

# ---------------------------------------------------------------------------------------------
# excel format
# ---------------------------------------------------------------------------------------------

EXCEL_PATH = os.getenv('PSI_EXCEL_PATH') or ""

EXCEL_FONT_SIZE = os.getenv('PSI_EXCEL_FONT_SIZE') or 10

EXCEL_SHEET_NAME = '生産管理台帳'

EXCEL_ROW_TITLE = 1
EXCEL_ROW_START = 2

EXCEL_COL_ORDER_ID = 1  # 通し番号
EXCEL_COL_RECEIVED_DATE = 3  # 受注日
EXCEL_COL_ORDER_NUM = 4  # 受注番号
EXCEL_COL_ORDER_DETAIL_NUM = 5  # 受注明細番号
EXCEL_COL_INPUT_TYPE = 6  # 入力区分
EXCEL_COL_DETAIL_TYPE = 7  # 明細区分
EXCEL_COL_ADD_MANF = 9  # 追加工有無
EXCEL_COL_PRODUCTION_NUM = 10  # 製番
EXCEL_COL_MODEL_NUM = 16  # 型番
EXCEL_COL_PRODUCT_NUM = 17  # 製品コード
EXCEL_COL_PRODUCT_NAME = 18  # 製品名
EXCEL_COL_CUSTOMER_CODE = 19  # 得意先コード
EXCEL_COL_CUSTOMER_NAME = 20  # 得意先名
EXCEL_COL_ORDER_TITLE = 21  # 件名
EXCEL_COL_DELIVERY_DATE = 23  # 客先納期
EXCEL_COL_DELIVERY_DATE_STATUS = 24  # 納期ステータス
EXCEL_COL_REC_ORDER_QTY = 25  # 受注数量
EXCEL_COL_REC_UPDATE_TYPE = 26  # 更新区分
EXCEL_COL_KAISAKU_DETAIL = 27  # 改作内容
EXCEL_COL_UPDATED = 28  # 最終更新日
EXCEL_COL_ADD_MANF_PAINTING = 29  # 塗装
EXCEL_COL_ADD_MANF_NAMEPLATE = 30  # 銘板張替
EXCEL_COL_ADD_MANF_PLATING = 31  # メッキ
EXCEL_COL_ADD_MANF_OTHERS = 32  # その他
EXCEL_COL_ADD_MANF_DETAIL = 33  # 追加工内容
EXCEL_COL_MANF_ORDER = 34  # 外注発注状況
EXCEL_COL_DEPT = 36  # 担当事業部
EXCEL_COL_CUSTOMER_TYPE = 37  # 客先区分
EXCEL_COL_ARTICLE = 39  # 記事
EXCEL_COL_SPECIFICATION = 48  # 仕様指定事項
EXCEL_COL_SERIAL_NUM = 53  # シリアル番号
EXCEL_COL_SUPPLYER = 54  # 実作業者名
EXCEL_COL_INSPECTION_DATE = 55  # 社検日
EXCEL_COL_INSPECTION_STATUS = 56  # 社検日ステータス
EXCEL_COL_INSPECTION_UPDATED = 57  # 社検日更新日
EXCEL_COL_UPDATE_STATUS = 119  # 当RPA用の更新ステータス置き場、全更新が終わったら消す。

DONE = 1

EXCEL_COPY_FORMAT_START_COL = 2
EXCEL_COPY_FORMAT_FINISH_COL = 118

EXCEL_COPY_PRODUCTION_NUM_START_COL = 2
EXCEL_COPY_PRODUCTION_NUM_FINISH_COL = 118
EXCEL_COPY_PRODUCTION_NUM_SKIP_COLS = [EXCEL_COL_PRODUCTION_NUM, EXCEL_COL_REC_ORDER_QTY]


# logger.info("///////////////////////////////////")
# logger.info("Ver 1.0.0")
# logger.info(f"Mode: {IS_DEBUG}")
# logger.info(f"Intranet: {IS_INTRANET}")
# logger.info(f"Intranet: {IS_INTRANET}")
# logger.info(f"Notify: {SKIP_NOTIFY}")
# logger.info("--<Database>-----------------------")
# logger.info(f"Host: {MSSQL_DEV_HOST}")
# logger.info(f"Port: {MSSQL_PORT}")
# logger.info(f"user: {MSSQL_USER}")
# logger.info("--<Excel file>---------------------")
# logger.info(f"Excel file path: {EXCEL_PATH}")
# logger.info(f"Font size: {EXCEL_FONT_SIZE}")
# logger.info("///////////////////////////////////")
# sys.exit()
