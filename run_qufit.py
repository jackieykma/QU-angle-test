'''
Run the actual QU-fitting
Split the sources into 50 chunks
Distribute each chunk into one PBS job
This will be controlled by the input parameter [0, 49]
'''

import time
import glob
import os
import sys
import numpy as np
from multiprocessing import Pool



qu_path = '~/scripts/RM-Tools/RMtools_1D/do_QUfit_1D_mnest.py'

if len(sys.argv) != 2:
   raise Exception('This script takes exactly one input argument!')

## Unpack the input arguments:
n = int(sys.argv[1])



def run_qufit_multicore(fname):
   os.system('python3 '+qu_path+' '+fname+' -m 1 --sampler nestle -i --ncores 1 --nlive 128')
   os.system('rm -rf '+fname.split('.')[0]+'*nestle')
   os.system('rm -rf '+fname.split('.')[0]+'*pdf')



## Load in the full source list, and determine which ones to run
full_flist = glob.glob('src_spec/*dat')
full_flist.sort()
i_list = np.arange(int((len(full_flist)/50)*n), int((len(full_flist)/50)*(n+1)), 1)
## Start running
start_time = time.time()
pool = Pool(56)
pool.map(run_qufit_multicore, np.array(full_flist)[i_list])
pool.close()
pool.join()
elapsed_time = time.time() - start_time
print('Elapsed time: '+str(int(elapsed_time)//3600)+' hours '+str(int(elapsed_time%3600)//60)+' minutes %.2f' % ((elapsed_time%3600)%60)+' seconds.')












