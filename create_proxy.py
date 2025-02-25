import os
import requests # TODO this import is only necessary for app ownership transfers. Remove from final repo.
from heroku_tools import (
    heroku_url,
    headers,
    get_app_info,
    create_heroku_app,
    get_addon_info,
    attach_addon,
    set_config_vars,
    create_blob_source,
    create_build,
    )


HUB_APP_NAME = os.getenv("APP_NAME")
HEROKU_AUTH_TOKEN = os.getenv("HEROKU_AUTH_TOKEN")
HUB_PORT = os.getenv("PORT")
PROXY_APP_NAME = os.getenv("PROXY_NAME")
PROXY_AUTH_TOKEN = os.getenv("CONFIGPROXY_AUTH_TOKEN")
PROXY_BLOB = os.getenv("PROXY_BLOB")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_GLOBAL_NAME = os.getenv("DATABASE_GLOBAL_NAME")


if __name__ == "__main__":

    # query for current (hub) app url
    print("\n\nGetting hub app info...")
    hub_info = get_app_info(app_name=HUB_APP_NAME)
    print("HUB INFO: ")
    for item in hub_info:
        print(f"{item}: {hub_info[item]}")

    print("\n\nGetting proxy app info...")
    proxy_info = create_heroku_app(app_name=PROXY_APP_NAME)
    print("PROXY INFO: ")
    for item in proxy_info:
        print(f"{item}: {proxy_info[item]}")

    # Check if proxy has postgres add-on and attach if not
    print("\n\nChecking for Proxy App database add-on...")
    database_info = get_addon_info(PROXY_APP_NAME, DATABASE_GLOBAL_NAME)
    if database_info is None:
        print("Database add-on not found for Proxy App")
        print(f"Attaching {DATABASE_GLOBAL_NAME} to {PROXY_APP_NAME}")
        database_info = attach_addon(PROXY_APP_NAME, DATABASE_GLOBAL_NAME, confirm=HUB_APP_NAME)
    else:
        print(f"{PROXY_APP_NAME} already has {DATABASE_GLOBAL_NAME} add-on attached.")
        print("ADD-ON ATTACH RESPONSE:")
        print(database_info)
    print("DATABASE ADD-ON INFO:")
    for each in database_info:
        print(f"{each}: {database_info[each]}")

    # Set all necessary config vars for both apps
    print("\n\nSetting config variables...")

    # Set proxy URL in hub app
# Set proxy URL in hub app with correct API path
    hub_config_vars = {
        "PROXY_WEB_URL": proxy_info['web_url']
    }
    set_config_vars(app_name=HUB_APP_NAME, config_vars=hub_config_vars)

    # Set all necessary config vars for proxy app
    proxy_config_vars = {
        "APP_NAME": PROXY_APP_NAME,
        "HUB_APP_NAME": HUB_APP_NAME,
        "HUB_WEB_URL": hub_info["web_url"],
        "HUB_PORT": HUB_PORT,
        "PROXY_WEB_URL": proxy_info["web_url"],
        "CONFIGPROXY_AUTH_TOKEN": PROXY_AUTH_TOKEN,
        "HEROKU_AUTH_TOKEN": HEROKU_AUTH_TOKEN,
    }
    set_config_vars(app_name=PROXY_APP_NAME, config_vars=proxy_config_vars)

    # Push proxy app blob to heroku source url
    print("\n\nCreating source for proxy app blob...")
    blob_get_url = create_blob_source(app_name=PROXY_APP_NAME, blob_path=PROXY_BLOB)

    # Create build for proxy server app
    print("\n\nAttempting to create proxy server build...")
    proxy_build = create_build(app_name=PROXY_APP_NAME, source_blob={"source_blob": {"url": blob_get_url}})
    print("Proxy server is running...")



