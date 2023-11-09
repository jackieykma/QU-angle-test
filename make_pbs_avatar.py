'''
Write PBS scripts
'''

import os

os.system('rm -rf pbs_scripts_avatar')
os.system('mkdir pbs_scripts_avatar')

for i in range(50):
   f = open('pbs_scripts_avatar/pbs_'+str(i)+'.pbs', 'w')
   f.write('#!/bin/bash\n#### JOB NAME\n')
   f.write('#PBS -N QUfit-'+str(i)+'\n')
   f.write('#PBS -M yikki.ma@anu.edu.au\n')
   f.write('#PBS -m abe\n')
   f.write('#PBS -l select=1:ncpus=56\n')
   f.write('source ~/anaconda3/etc/profile.d/conda.sh\n')
   f.write('conda activate base\n')
   f.write('cd /priv/avatar/ykma/my_script/QU-angle-test\n')
   f.write('python3 run_qufit.py '+str(i))
   f.close()








