#! /usr/bin/python3

# quick deployment script for use with gitlab runner

import os
from hinoki.sensuapi import sensu_connect
from hinoki.sensuasset import sync_assets
from hinoki.config import config
from hinoki.logger import log
from hinoki.assets import build_assets

def import_defs():

	check_defs=True
	asset_defs=True
	filter_defs=True
	handler_defs=True
	errors=True
	assets=True

	if not sensu_connect.test_connection():
		exit(1)

	sensu_connect.api_auth()

	# sync asset definitions

	## if definitions already exist in the folder, these can just be caught with the main case
	## otherwise if we're building, we need to make sure that we build first and that this step
	## succeeds before moving on.

	if asset_list:
		for file in asset_list:
			asset_def_succeeded=sensu_connect.sync_definition('asset', file)
			if not asset_def_succeeded:
				asset_defs=False
				break
			if asset_defs:
				log.info("Asset definitions successfully imported.")
		assets=sync_assets()

	# sync definitions
	# config['api_items']['asset']['endpoint']['dir']
	for item_name, item_obj in config['api_items'].items():
		try:
			for file in os.listdir(item_obj['dir']):
				import_succeeded=sensu_connect.sync_definition(item_name, file)
				if not import_succeeded:
					log.error("Failed importing "+item_name+" "+file)
					errors = True
					break
			if import_succeeded:
				log.info("All "+item_name+" definitions succesfully imported.")
		except KeyError:
			log.debug("No directory key for api item "+item_name)
			pass

	if (assets and asset_defs and check_defs):
		log.info("All file and API operations completed successfully!")
		exit(0)
	else:
		log.info("Some sync operations did not complete, failing the job.")
		if not assets:
			log.error("Asset rsync failed.")
		if not asset_defs:
			log.error("API sync for asset definitions failed.")
		if not check_defs:
			log.error("API sync for check definitions failed.")
		exit(1)

def import_assets():
	build_assets()

def import_all():
	import_assets()
	import_defs()