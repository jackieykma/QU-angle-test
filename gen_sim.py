'''
Generate simulated sources that will be run through QU-fitting
These sources are all Faraday simple

Simulate N (= 1e5?) sets of polarised sources
Each set will be comprised of two sources:
(a) Random PA0 (as below)
(b) Fixed PA0 = 90 deg (which will not have angle wrapping issue)
All other parameters will be fixed between the two soruces

Frequency range of 800-1088 MHz; 1 MHz channels (as per POSSUM Band 1)
PI: [0.005, 0.5] (arbitrary unit; uniform distribution)
PI noise: 0.005 (arbitrary unit; full band)
PA0: [0, 180) (deg; for source a)
RM: [-100, +100] (rad m-2)
'''

import numpy as np
import os



## Initial settings
np.random.seed(323476)
N = 100000
freq_array = np.arange(800.e6, 1089.e6, 1.e6)
c = 299792458.
l2_array = (c/freq_array)**2



## Create directory to store all source files
os.system('rm -rf src_spec')
os.system('mkdir src_spec')
## Create catalogue file to store "ground truth"
f = open('ground_truth.csv', 'w')
f.write('srcname,PI (arb. unit),PA0 (deg),RM (radm-2)\n')



for i in range(N):
   if i%1000 == 0:
      print('Working on source set '+str(i)+' out of '+str(N)+'...')
   ## Generate noise that will be used for both sources (a and b)
   q_noise = np.random.randn(len(freq_array))*0.005*np.sqrt(len(l2_array))
   u_noise = np.random.randn(len(freq_array))*0.005*np.sqrt(len(l2_array))
   ## Choose the PI, PA0, and RM
   chosen_pi = (np.random.rand()*0.495)+0.005
   chosen_pa0 = np.random.rand()*180.
   chosen_rm = (np.random.rand()-0.5)*200.
   ## Generate Q, U arrays for both sources
   q_a = chosen_pi*np.cos(2.*(np.radians(chosen_pa0)+chosen_rm*l2_array))
   u_a = chosen_pi*np.sin(2.*(np.radians(chosen_pa0)+chosen_rm*l2_array))
   q_b = chosen_pi*np.cos(2.*(np.radians(90.)+chosen_rm*l2_array))
   u_b = chosen_pi*np.sin(2.*(np.radians(90.)+chosen_rm*l2_array))
   ## Add in noise
   q_a += q_noise; q_b += q_noise
   u_a += u_noise; u_b += u_noise
   ## Write out the chosen "ground truth" to catalogue
   f.write(str(i)+'a,'+str(chosen_pi)+','+str(chosen_pa0)+','+str(chosen_rm)+'\n')
   f.write(str(i)+'b,'+str(chosen_pi)+','+str(90.0)+','+str(chosen_rm)+'\n')
   ## Write out the source spectrum files
   g1 = open('src_spec/'+str(i)+'a.dat', 'w')
   g2 = open('src_spec/'+str(i)+'b.dat', 'w')
   for j in range(len(freq_array)):
      g1.write(str(freq_array[j])+'\t'+str(q_a[j])+'\t'+str(u_a[j])+'\t'+str(0.005*np.sqrt(len(l2_array)))+'\t'+str(0.005*np.sqrt(len(l2_array)))+'\n')
      g2.write(str(freq_array[j])+'\t'+str(q_b[j])+'\t'+str(u_b[j])+'\t'+str(0.005*np.sqrt(len(l2_array)))+'\t'+str(0.005*np.sqrt(len(l2_array)))+'\n')




