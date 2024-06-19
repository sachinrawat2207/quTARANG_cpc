import sys
import h5py as hp
from pathlib import Path 
import matplotlib.pyplot as plt 
import os 

path = '/mnt/Disk_14TB/Sachin/cpc_code/op'
device = 'cpu'


op_file = Path(path)/'postprocessing/'

if not Path(op_file).exists():
    os.makedirs(op_file)

sys.path.insert(0, path)
import para 
