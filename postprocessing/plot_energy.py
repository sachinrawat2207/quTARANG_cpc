from postprocessing.config import *
import numpy as np 
import matplotlib.pyplot as plt
import h5py as hp 

plt.rcParams.update({'font.size':'15',
                     'font.family':'serif',
                     'font.weight':'bold',
                     'lines.linewidth':1.5,
                     'text.usetex':True})

f = hp.File(Path(path)/'energies.h5', 'r')
te = f['tenergy'][:]
ke = f['ke'][:]
kec = f['kec'][:]
kei = f['kei'][:]
kec = f['kec'][:]
qe = f['qe'][:]
t = f['t'][:]
f.close()

plt.plot(t, te, linewidth = 2, label = r'$E$')
plt.plot(t, ke, linewidth = 2, label = r'$E_{k}$')
plt.plot(t, kec, linewidth = 2, label = r'$E^{c}_{k}$')
plt.plot(t, kei, linewidth = 2, label = r'$E^{i}_{k}$')
plt.plot(t, qe, linewidth = 2, label = r'$E_{qnt}$')


plt.xlim(t[0], t[-1])
plt.ylim(top = te[-1]+te[-1]/2)
plt.xlabel('$t$')
plt.ylabel('$E$')
plt.legend(fancybox=False,  loc='upper right', frameon=False, ncol = 2)
plt.tight_layout()
plt.savefig(dir/"energy.jpeg", dpi=300, bbox_inches='tight')
plt.show()