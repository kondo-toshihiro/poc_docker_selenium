#  https://learn.microsoft.com/ja-jp/cli/azure/

# proxy setting
# $env:https_proxy = "http://j063514:passowrd@www-n.ddreams.jp:8080"
# $env:http_proxy = "http://j063514:passowrd@www-n.ddreams.jp:8080"

# import os
from azure.keyvault.secrets import SecretClient
from azure.identity import InteractiveBrowserCredential

from src.proxy_setting import input_proxy_setting

# from src.LogHandler import get_logger

# logger = get_logger(__name__)


def get_db_password() -> str:
    # keyVaultName = os.environ["KEY_VAULT_NAME"]
    input_proxy_setting()
    keyVaultName = 'fdb-keyvault'
    KVUri = f"https://{keyVaultName}.vault.azure.net"

    credential = InteractiveBrowserCredential(additionally_allowed_tenants=["83a93e6c-7d11-4610-a5a9-edd6052f14b7"])
    client = SecretClient(vault_url=KVUri, credential=credential)
    secretName = 'dbuss-dwh'
    retrieved_secret = client.get_secret(secretName)
    # logger.info("get kv")
    return retrieved_secret.value

# print(f"Your secret is '{retrieved_secret.value}'.")
# print(" done.")
