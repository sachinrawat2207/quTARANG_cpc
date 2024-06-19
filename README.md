[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<!-- **quTARANG** is a Python package developed to study turbulence in quantum systems, specifically in atomic Bose-Einstein condensates by using the mean-field Gross-Pitaevskii equation (GPE). quTARANG is the GPU-CPU agnostic i.e., one can switch the code to run on a CPU or a GPU by setting a parameter `device` in `para.py` file which is discussed below in detail. It uses the Time-splitting pseudo-spectral (TSSP) to evolve the system. The stationary states can also be computed by evolving the GPE in imaginary time. This can be done in quTARANG by merely setting a parameters in `para.py`.
It is also equipped with the functions for computing different statistical quanties such as spectra and fluxes of different energies and fluxes. -->
**quTARANG** is a Python package designed for studying turbulence in quantum systems, specifically in atomic Bose-Einstein condensates (BECs), using the mean-field Gross-Pitaevskii equation (GPE) given by

$i\hbar\partial_t\psi(\vec{r},t) = -\frac{\hbar^2}{2m}\nabla^2\psi(\vec{r},t) + V(\vec{r},t)\psi(\vec{r},t) + U_0|\psi(\vec{r},t)|^2\psi(\vec{r},t)$,

where $\psi(\vec{r},t)$ is the macroscopic complex wave function, $m$ is the atomic mass, $V(\vec{r},t)$ is the trapping potential, $N$ is the number of particles, $\displaystyle U_0=(4\pi\hslash^2a_s)/m$ is the nonlinear interaction parameter and $a_s$ denotes the scattering length for the interaction of the atomic particles.

The package is hardware-agnostic, allowing users to run simulations on either a CPU or a GPU by setting the `device` parameter in the para.py file, as detailed below. **quTARANG** employs the Time-Splitting Pseudo-Spectral (TSSP) method for evolving the system, ensuring both efficiency and accuracy. Additionally, the package can compute stationary states by evolving the GPE in imaginary time, enabled by setting `imgtime` parameter as `True` in the para.py file. **quTARANG** also includes functions to compute various statistical quantities, such as energy spectra and fluxes. It can compute the energy spectra by using a conventional binning method as well as more resolve spectra using the the angle-averaged Wiener-Khinchin approach [see](https://journals.aps.org/pra/pdf/10.1103/PhysRevA.106.043322). 

The directory structure of ***quTARANG*** package is as follows:
```
├── postprocessing
└── quTARANG
    ├── config
    ├── initial_cond
    ├── util
    ├── src
    └── para.py
├── main.py
```
- `postprocessing` directory contains the function to plot the energy evolution, animation of wavefunction density and phase evolution and function to compute the spectra and fluxes of compressible kinetic energy, incompressible kinetic energy and particle number.
- `quTARANG` directory contains the source files and `para.py` file where user needs to set the parameters required to run the code.
- `main.py` is used to run the code when all the necessary input parameters are set inside the `para.py` file.

## 1) Packages required to run quTARANG
The following Python packages need to be installed to run quTARANG
* `numpy` : To run on CPU,
* `cupy` : To run code on single GPU,
* `h5py`,
* `matplotlib`,
* `pyfftw`.


## 2) Steps to run the code
1. Set the parameters inside the following `para.py` file:
```python
#para.py
#================================================================================
#                       Change the following parameters
#================================================================================
real_dtype = "float64"
complex_dtype = "complex128"

pi = 3.141592653589793

# Device Setting 
device = "gpu"             # Choose the device <"cpu"> to run on cpu and gpu to run on <"gpu">
device_rank = 0            # Set GPU no in case if you are running on a single GPU else leave it as it is

# Set grid size 
Nx = 512
Ny = 512
Nz = 1
    
# Set box length
Lx = 22
Ly = 22
Lz = 1

# Set maximum time and dt
tmax = 8    
dt = 0.001

# Choose the value of the non linerarity
g = 0.1

# Soping criteria in imaginary time evolution 
delta = 1e-12

init_usrdef = False
init_cond = 'rp'

# If init_usrdef is True then either pass input through main or set the input path along with input file
in_path = "/path/to/input/folder/"


# Set output folder path
op_path = "/path/to/output/folder/"

# Choose the scheme need to implement in the code
scheme = "TSSP"          # Choose the shemes <"TSSP">, <"RK4"> etc
imgtime = False          # set <False> for real time evolution and <True> for imaginary time evolution

# To resume the Run
resume = False

# To overwrite the existing output
overwrite = True

# Wavefunction save setting
wfc_start_step = 0

# make wfc_iter too big to stop saving the wfc 
wfc_iter_step = 500

# Rms save setting
save_rms = True
rms_start_step = 0
rms_iter_step = 10

# Energy save setting
save_en = True
en_start_step = 0
en_iter_step = 100

# Printing iteration step
t_print_step = 1000

#================================================================================

if Nx != 1 and Ny == 1 and Nz == 1:
    dimension = 1

elif Nx != 1 and Ny != 1 and Nz == 1:
    dimension = 2

elif Nx != 1 and Ny != 1 and Nz != 1:
    dimension = 3  
```

3. Modify the following `main.py` file:

```python
from quTARANG import para
from quTARANG.src.lib import gpe
from quTARANG.src import evolution
from quTARANG.src.univ import grid, fns
from quTARANG.config.config import ncp

# 2D user defined initial conditon 
def gstate_wfc2d():
    return 1/ncp.sqrt(ncp.pi)*ncp.exp(-(grid.x_mesh**2 + grid.y_mesh**2)/2)

def gstate_pot2d(t):
    return 0.5*(grid.x_mesh**2 + grid.y_mesh**2)

# 3D user defined intial conditon
def gstate_wfc3d():
    return 1/(ncp.pi)**(3/4)*ncp.exp(-(grid.x_mesh**2 + grid.y_mesh**2+ grid.z_mesh**2)/2)

def gstate_pot3d(t):
    return 0.5*(grid.x_mesh**2 + grid.y_mesh**2 + 4**2 * grid.z_mesh**2)


G = gpe.GPE(wfcfn = None, potfn = None)

# If init_usrdef = True in para.py file and user want to pass the user defined funcitns.
# G = gpe.GPE(wfcfn = gstate_wfc2d, potfn = gstate_pot2d)

##########################################################################

evolution.time_advance(G)
```
4. Once the `para.py` and `main.py` file sets, the one can run the simulations using:

```python
python main.py
```


## 3) Postprocessing