'''
Write PBS scripts
'''

import os

os.system('rm -rf pbs_scripts_gadi')
os.system('mkdir pbs_scripts_gadi')

for i in range(50):
   f = open('pbs_scripts_gadi/pbs_'+str(i)+'.pbs', 'w')
   f.write('#!/bin/bash\n#### JOB NAME\n')
   f.write('#PBS -N QUfit-'+str(i)+'\n')
   f.write('#PBS -M yikki.ma@anu.edu.au\n')
   f.write('#PBS -m abe\n')
   f.write('#PBS -l ncpus=56,mem=256GB,walltime=48:00:00\n')
   f.write('#PBS -q rsaa\n\n')
   f.write('source ~/miniconda3/etc/profile.d/conda.sh\n')
   f.write('conda activate base\n')
   f.write('cd /scratch/mk27/ym0976/QU-angle-test\n')
   f.write('python3 run_qufit.py '+str(i))
   f.close()








