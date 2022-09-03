#! /usr/bin/env python3

import os
import sys
import subprocess

try:
  result = subprocess.run(['sqlite3', '/app/template.db', '.read g2core-schema-sqlite-create.sql'],  capture_output=True, text=True)
  print(result.stdout)
  print(result.stderr, file=sys.stderr)
  result.check_returncode()

except subprocess.CalledProcessError as err:
  print('Running sqlite to create the DB failed', file=sys.stderr)
  exit(-1)
except Exception as err:
  print(err, file=sys.stderr)
  exit(-1)

