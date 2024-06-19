from postprocessing.config import *
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size':'15',
                     'font.family':'serif',
                     'font.weight':'bold',
                     'lines.linewidth':1.5,
                     'text.usetex':True})


f = hp.File(Path(path)/'rms.h5', 'r')

if para.dimension == 1:
    xrms = f['xrms'][:]
    t_rms = f['t'][:]

if para.dimension == 2:
    rrms = f['rrms'][:]
    xrms = f['xrms'][:]
    yrms = f['yrms'][:]
    t_rms = f['t'][:]

if para.dimension == 3:
    xrms = f['xrms'][:]
    yrms = f['yrms'][:]
    zrms = f['zrms'][:]
    t_rms = f['t'][:]
f.close()

# print(rms)
# plt.plot(t_rms, rms, label='rms')
plt.plot(t_rms, xrms,'k', label = r'$x_{rms}$', linewidth = 2)

if para.dimension == 2:
    # plt.plot(t_rms, rrms, 'r--', label = r'$r_{rms}$', linewidth = 2)
    plt.plot(t_rms, yrms, 'b--', label = r'$y_{rms}$', linewidth = 2)
    

elif para.dimension == 3:
    plt.plot(t_rms, yrms, label = r'$y_{rms}$')
    plt.plot(t_rms, zrms, label = r'$z_{rms}$')

plt.xlabel('$t$', fontsize=28)    
plt.xlim(t_rms[0], t_rms[-1])
plt.legend(fancybox=False,  loc='best', frameon=False)
plt.tight_layout()
plt.savefig(dir/"rms.jpeg", dpi=300, bbox_inches='tight')
plt.show()