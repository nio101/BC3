#!/usr/bin/env python3
# coding: utf-8

"""
generate_index.py
generate index/checksum files for OTA update
"""

# =======================================================
# Imports
import glob

# =======================================================
# helpers


# =======================================================
# main loop

for name in glob.glob('ESP32/*'):
	print(name)
