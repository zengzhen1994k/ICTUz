import zap_auth
import zap_config
import zap_blindxss
import os
import traceback
import logging

config = zap_config.ZapConfig()

# Triggered when running a script directly (ex. python zap-baseline.py ...)
def start_docker_zap(docker_image, port, extra_zap_params, mount_dir):
    try:
        config.load_config(extra_zap_params)
    except:
        logging.error("error in start_docker_zap: %s", traceback.print_exc())
        os._exit(1)

# Triggered when running from the Docker image
def start_zap(port, extra_zap_params):
    try:
        config.load_config(extra_zap_params)
    except:
        logging.error("error in start_zap: %s", traceback.print_exc())
        os._exit(1)

def zap_started(zap, target):
    try:
        # ZAP Docker scripts reset the target to the root URL
        if target.count('/') > 2:
            # The url can include a valid path, but always reset to spider the host
            target = target[0:target.index('/', 8)+1]

        scan_policy = 'Default Policy'
        zap.ascan.update_scan_policy(scanpolicyname=scan_policy , attackstrength="LOW")
        zap_auth.ZapAuth().login(config, zap, target)
        zap_blindxss.load(config, zap)
    except:
        logging.error("error in zap_started: %s", traceback.print_exc())
        os._exit(1)

    return zap, target

# def zap_pre_shutdown(zap):
#     for url in zap.spider.all_urls:
#         logging.info("found: %s", url)