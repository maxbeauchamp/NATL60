"""
NATL60 is a set of libraries to deal with NATL60 maps and both nadir/swot NATL60-based datasets
"""

__version__ = "0.0.1"

##################################
# Standard lib
##################################
import sys
import os
import time as timer
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

assert sys.version_info >= (3,6), "Need Python>=3.6"

##################################
# Config
##################################
# Define paths
datapath="/gpfswork/rech/yrf/uba22to/NATL60"
rawdatapath="/gpfsstore/rech/yrf/uba22to/NATL60_raw"
basepath="/linkhome/rech/genimt01/uba22to/NATL60"

print("Initializing NATL60 libraries...",flush=True)

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
from scipy.interpolate import RegularGridInterpolator
import xarray as xr
import xesmf as xe

##################################
# Tools
##################################
from .mods.tools import *
from .mods.class_NATL60 import *
from .mods.class_NATL60_maps import *
from .mods.class_NATL60_nadir import *
from .mods.class_NATL60_swot import *
from .mods.class_NATL60_fusion import *

print("...Done") # ... initializing Libraries
