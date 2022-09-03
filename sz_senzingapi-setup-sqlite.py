#! /usr/bin/env python3

import os
import sys
import shutil

from os.path import exists
import json
from urllib.parse import urlparse

from senzing import G2Config, G2ConfigMgr, G2Exception

try:
  engine_config = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON')
  if not engine_config:
    print('The environment variable SENZING_ENGINE_CONFIGURATION_JSON must be set with a proper JSON configuration.', file=sys.stderr)
    print('Please see https://senzing.zendesk.com/hc/en-us/articles/360038774134-G2Module-Configuration-and-the-Senzing-API', file=sys.stderr)
    exit(-1)

  parsed_config = json.loads(engine_config)
  backend = parsed_config['SQL'].get('BACKEND')
  if backend and backend != 'SQL':
    print('Clustered backends are not supported', file=sys.stderr)
    exit(-1)

  conn = parsed_config['SQL']['CONNECTION']
  uri = urlparse(conn)
  if uri.scheme != 'sqlite3':
    print(f'Only sqlite3 DBs are supported. Found [{uri.scheme}]', file=sys.stderr)
    exit(-1)

  if exists(uri.path):
    print(f'Database [{uri.path}] exists. Skipping creation.')
  else:
    print(f'Creating database [{uri.path}]')
    shutil.copy('/app/template.db',uri.path)

  default_config_id = bytearray()
  g2_config_mgr = G2ConfigMgr()
  g2_config_mgr.init("g2ConfigMgr", engine_config, False)
  g2_config_mgr.getDefaultConfigID(default_config_id)
  if default_config_id:
    print('Database already contains a default configuration.  Skipping creation.')
  else:
    g2_config = G2Config()
    g2_config.init("g2Config", engine_config, False)
    config_handle = g2_config.create()
    new_configuration_bytearray = bytearray()
    g2_config.save(config_handle, new_configuration_bytearray)
    g2_config.close(config_handle)

    config_json = new_configuration_bytearray.decode()
    new_config_id = bytearray()
    g2_config_mgr.addConfig(config_json, 'Configuration added from sz_senzingapi-setup-sqlite.', new_config_id)
    g2_config_mgr.setDefaultConfigID(new_config_id)
    g2_config.destroy()
    print('Created default configuration')

  g2_config_mgr.destroy()

except G2Exception as err:
  print(err, file=sys.stderr)
  exit(-1)
except Exception as err:
  print('The environment variable SENZING_ENGINE_CONFIGURATION_JSON must be set with a proper JSON configuration.', file=sys.stderr)
  print('Please see https://senzing.zendesk.com/hc/en-us/articles/360038774134-G2Module-Configuration-and-the-Senzing-API', file=sys.stderr)
  print(err, file=sys.stderr)
  exit(-1)

