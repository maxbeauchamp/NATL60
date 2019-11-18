"""
NATL60 is a set of libraries to deal with NATL60 maps and both nadir/swot NATL60-based datasets
"""

__version__ = "0.0.1"

##################################
# Standard lib
##################################
import sys
import os
from os.path import join as join_paths
from datetime import date, datetime, timedelta
import itertools
import warnings
import traceback
import re
import functools
import configparser
import builtins
from time import sleep
from collections import OrderedDict

# assert sys.version_info >= (3,6), "Need Python>=3.6"

##################################
# Config
##################################
dirs = {}
dirs['natl60']    = os.path.dirname(os.path.abspath(__file__))
dirs['NATL60']    = os.path.dirname(dirs['natl60'])

_rc = configparser.ConfigParser()
# Load rc files from dapper, user-home, and cwd
_rc.read(join_paths(x,'dpr_config.ini') for x in
    [dirs['natl60'], os.path.expanduser("~"), os.curdir])
# Convert to dict
rc = {s:dict(_rc.items(s)) for s in _rc.sections() if s not in ['int','bool']}
# Parse
#for x in _rc['bool']: rc[x] = _rc['bool'].getboolean(x)

# Define paths
dirs['datapath']  = dirs['NATL60']
datapath="/home/user/Bureau/NATL60"

'''if rc['welcome_message']:
  print("Initializing NATL60 libraries...",flush=True)'''

##################################
# Scientific and mapping
##################################
import matplotlib.pyplot as plt
import pandas as pd
import shapely
from shapely import wkt
import geopandas as gpd
from cartopy import crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
import xarray as xr

##################################
# Tools
##################################
from .mods.tools import *
from .mods.class_NATL60 import *
from .mods.class_NATL60_maps import *
from .mods.class_NATL60_nadir import *
from .mods.class_NATL60_swot import *
from .mods.class_NATL60_fusion import *

'''if rc['welcome_message']:
  print("...Done") # ... initializing Libraries
  print("PS: Turn off this message in your configuration: dpr_config.ini")'''



