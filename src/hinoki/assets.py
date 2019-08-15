#! /usr/bin/python3

import subprocess
import os
import tarfile
import hashlib
import json
from urllib import parse
from hinoki.config import config
from hinoki.logger import log

def build_assets():

    asset_list = []

    output = os.listdir(config['check_scripts_dir'])
    asset_list = os.listdir(config['asset_defs_dir'])
    log.info("Beginning asset build...")
    
    try:
        output.remove('.DS_Store')
    except ValueError:
        pass

    if not os.path.exists(config['asset_files_dir']):
        os.mkdir(config['asset_files_dir'])
        log.debug("Check scripts ls: "+output)
        log.debug("Asset definitions ls: "+asset_list)
    for item in output:
        asset_hash = ''
        basename = os.path.basename(item)
        basepath = os.path.join(config['check_scripts_dir'], basename)
        archive_name = basename+".tar"
        archive_path = os.path.join(config['asset_files_dir'], archive_name)
        archive_file = open(archive_path, 'w')
        tarproc = subprocess.Popen(["tar", "--mtime", "'1970-01-01 00:00:00'", "--owner", "root", "-c", "-C", basepath, 'bin'], stdout=archive_file)
        tarproc.wait()
        archive_file.close()
        log.debug("basename: "+basename)
        asset_hash = hashlib.sha512(open(archive_path,'rb').read()).hexdigest()
        log.debug("asset hash: "+asset_hash)
        log.debug("archive_path = {}".format(archive_path))
        asset_definition_file = os.path.join(config['asset_defs_dir'], basename+".json")
        log.info(asset_definition_file)
        if not os.path.exists(asset_definition_file):
            handler = open(asset_definition_file, "w+")
            asset_obj = {
                "url": parse.urljoin(config['api_base_url'], archive_name),
                "sha512": asset_hash,
                "metadata": {
                    "name": basename,
                    "Content-Type": "application/zip",
                    "namespace": "default"
                }
            }
            json.dump(asset_obj, handler, indent=4)
            handler.close()
        else:
            asset_file_handler = open(asset_definition_file, "r+")
            asset_obj = json.load(asset_file_handler)
            asset_file_handler.close()
            asset_obj["sha512"] = asset_hash
            log.debug(asset_obj)
            new_handler = open(asset_definition_file, "w")
            json.dump(asset_obj, new_handler, indent=4)
            new_handler.close()

    return asset_list