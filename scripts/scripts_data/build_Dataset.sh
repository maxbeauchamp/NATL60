#!/bin/sh

domain=$1

# 1) create mask
#python -u $HOME/NATL60/src/create_mask.py ${domain}
# 2) convert nadir & SWOT to daily datasets
python -u $HOME/NATL60/scripts/scripts_data/convertNadirSwot_to_daily.py ${domain}
# 3) regrid nadir & SWOT datasets to the 1/20 regular grid
#python -u $HOME/NATL60/scripts/scripts_data/regrid_Dataset.py ${domain}
