import subprocess
import os
from hinoki.logger import log
from hinoki.config import config

def sync_assets(assets_destination=config['assets_destination'], asset_files_dir=config['asset_files_dir']):
    # TODO: right now this is just a little nginx server where these files can be collected by clients.
    if not os.path.isdir(assets_destination):
        log.info("Directory %s does not exist, attempting to create it..." % assets_destination)
        try:
            os.mkdir(assets_destination)
        except os.PermissionError:
            log.error("Permission error while attempting to create destination directory %s" % assets_destination)
            return False
    cmd=["rsync",  "-r", "--include", "*.tar.gz", asset_files_dir+"/", assets_destination]
    log.debug(cmd)
    try:
        subprocess.check_call(cmd)
    except (FileNotFoundError, PermissionError, subprocess.CalledProcessError) as e:
        log.error("rsync failed!")
        log.error(e)
        return False
    log.info("rsync of assets to destination folder succeeded.")
    return True