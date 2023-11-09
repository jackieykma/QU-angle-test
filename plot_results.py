'''
Plot the results to test effectiveness
- Plot against ground truth (to see how close the results get)
- Plot against PA0 = 90 deg (to compare against cases with no wrapping)
'''

import numpy as np
import astropy.table as at
import matplotlib.pyplot as plt
import glob
import json
import os



## Load in ground truth, and the QU-fitting output file list
truth_table = at.Table.read('ground_truth.csv')
fa_list = glob.glob('src_spec/*a_m1_nestle.json')

## Define lists to store the results
fa_pa = []
fa_pa_perr = []
fa_pa_merr = []
fb_pa = []
fb_pa_perr = []
fb_pa_merr = []
truth_pa = []
truth_pi = []
truth_rm = []


for fa in fa_list:
   fa_json = json.load(open(fa))
   if os.path.exists(fa.replace('a_m1', 'b_m1')):
      print('Working on '+fa+'...')
      ## Extract the values
      fb_json = json.load(open(fa.replace('a_m1', 'b_m1')))
      fa_pa.append(fa_json['values'][1])
      fa_pa_perr.append(fa_json['errPlus'][1])
      fa_pa_merr.append(fa_json['errMinus'][1])
      fb_pa.append(fb_json['values'][1])
      fb_pa_perr.append(fb_json['errPlus'][1])
      fb_pa_merr.append(fb_json['errMinus'][1])
      truth_pa.append(truth_table['PA0 (deg)'][truth_table['srcname'] == fa.split('/')[-1].split('_')[0]][0])
      truth_pi.append(truth_table['PI (arb. unit)'][truth_table['srcname'] == fa.split('/')[-1].split('_')[0]][0])
      truth_rm.append(truth_table['RM (radm-2)'][truth_table['srcname'] == fa.split('/')[-1].split('_')[0]][0])



## Ground-truth PA v.s. QU-fitting PA
plt.errorbar(truth_pa, fa_pa, yerr=[fa_pa_merr, fa_pa_perr], fmt='ko')
plt.xlabel('Ground-truth PA (deg)')
plt.ylabel('QU-fitting PA (deg)')
plt.tight_layout()
plt.show()



## Ground-truth PA v.s. QU-fitting PA; as 2D histogram
hist_plt = plt.hist2d(truth_pa, fa_pa, bins=[180, 180], density=True, cmap='gist_heat')
cbar = plt.colorbar()
cbar.set_label('Fractional Count')
plt.xlabel('Ground-truth PA (deg)')
plt.ylabel('QU-fitting PA (deg)')
plt.tight_layout()
plt.show()



## Difference in PA between ground-truth and QU-fitting, v.s. PI
ang_diff = np.array(fa_pa) - np.array(truth_pa)
ang_diff -= 180.*(ang_diff > 90.)
ang_diff += 180.*(ang_diff < -90.)
plt.errorbar(truth_pi, ang_diff, yerr=[fa_pa_merr, fa_pa_perr], fmt='ko')
plt.xlabel('Ground-truth PI (arb. unit)')
plt.ylabel('Ground-truth PA - QU-fitting PA (deg)')
plt.tight_layout()
plt.show()



## Difference in PA between ground-truth and QU-fitting, v.s. PI; as 2D histogram
ang_diff = np.array(fa_pa) - np.array(truth_pa)
ang_diff -= 180.*(ang_diff > 90.)
ang_diff += 180.*(ang_diff < -90.)
hist_plt = plt.hist2d(truth_pi, ang_diff, bins=[200, 180], density=True, cmap='gist_heat')
cbar = plt.colorbar()
cbar.set_label('Fractional Count')
plt.xlabel('Ground-truth PI (arb. unit)')
plt.ylabel('Ground-truth PA - QU-fitting PA (deg)')
plt.tight_layout()
plt.show()



## Difference in PA between ground-truth and QU-fitting, v.s. RM
ang_diff = np.array(fa_pa) - np.array(truth_pa)
ang_diff -= 180.*(ang_diff > 90.)
ang_diff += 180.*(ang_diff < -90.)
plt.errorbar(truth_rm, ang_diff, yerr=[fa_pa_merr, fa_pa_perr], fmt='ko')
plt.xlabel('Ground-truth RM (rad m-2)')
plt.ylabel('Ground-truth PA - QU-fitting PA (deg)')
plt.tight_layout()
plt.show()



## Difference in PA between ground-truth and QU-fitting, v.s. RM; as 2D histogram
ang_diff = np.array(fa_pa) - np.array(truth_pa)
ang_diff -= 180.*(ang_diff > 90.)
ang_diff += 180.*(ang_diff < -90.)
hist_plt = plt.hist2d(truth_rm, ang_diff, bins=[200, 180], density=True, cmap='gist_heat')
plt.xlabel('Ground-truth RM (rad m-2)')
plt.ylabel('Ground-truth PA - QU-fitting PA (deg)')
plt.tight_layout()
plt.show()



## Plot histogram of PA difference, in units of PA error reported
ang_diff_sn = ang_diff/np.sqrt(np.array(fa_pa_merr)*np.array(fa_pa_perr))
plt.hist(ang_diff_sn, bins=np.arange(-90., 90.1, 0.1), density=True, label='Results')
plt.plot(np.arange(-20., 20.01, 0.01), np.exp(-0.5*np.arange(-20., 20.01, 0.01)**2)/np.sqrt(2.*np.pi), label='Overplot of Gaussian distribution')
plt.xlim([-8., 8.])
plt.xlabel(r'$\Delta {\rm PA}/\sigma_{\rm PA}$')
plt.ylabel('Fractional Count')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()



## Plot minus error bar of source (a) v.s. source (b)
plt.plot(fa_pa_merr, fb_pa_merr, 'ko')
plt.xlabel('PA error minus a (deg)')
plt.ylabel('PA error minus b (deg)')
plt.tight_layout()
plt.show()



## Plot minus error bar of source (a) v.s. source (b); as 2D histogram
plt.hist2d(fa_pa_merr, fb_pa_merr, bins=[np.arange(0., 30.5, 0.5), np.arange(0., 30.5, 0.5)], density=True, cmap='gist_heat', vmin=0., vmax=0.05)
cbar = plt.colorbar()
cbar.set_label('Fractional Count')
plt.xlim(0., 20.)
plt.ylim(0., 20.)
plt.xlabel('PA error minus a (deg)')
plt.ylabel('PA error minus b (deg)')
plt.tight_layout()
plt.show()



## Plot plus error bar of source (a) v.s. source (b)
plt.plot(fa_pa_perr, fb_pa_perr, 'ko')
plt.xlabel('PA error plus a (deg)')
plt.ylabel('PA error plus b (deg)')
plt.tight_layout()
plt.show()



## Plot plus error bar of source (a) v.s. source (b); as 2D histogram
plt.hist2d(fa_pa_perr, fb_pa_perr, bins=[np.arange(0., 30.5, 0.5), np.arange(0., 30.5, 0.5)], density=True, cmap='gist_heat', vmin=0., vmax=0.05)
cbar = plt.colorbar()
cbar.set_label('Fractional Count')
plt.xlim(0., 20.)
plt.ylim(0., 20.)
plt.xlabel('PA error plus a (deg)')
plt.ylabel('PA error plus b (deg)')
plt.tight_layout()
plt.show()









