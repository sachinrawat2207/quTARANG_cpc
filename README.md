[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


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

init_usrdef = False
init_cond = 'rp'

# If init_usrdef is True then either pass input through main or set the input path along with input file
in_path = "/path/to/input/folder/"


# Set output folder path
op_path = "/path/to/output/folder/"

# Choose the scheme need to implement in the code
scheme = "TSSP"          # Choose the shemes <"TSSP">, <"RK4"> etc
imgtime = False          # set <False> for real time evolution and <True> for imaginary time evolution

delta = 1e-12 # Soping criteria in imaginary time evolution 

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

The description of the parmeters inside the para.py file is as follows: 

* `real_dtype` and `complex_dtype` : These prameter set the precison of the arrays used in the code. `real_dtype` specifies the precision for real array and it can takes two values *`"float32"`* or *`"float64"`* for single and double precision arrays, while `complex_dtype` can takes the values *`"complex64"`* or *`"complex128"`* for setting the complex array as single and double precision, respectively.
* `device` : Specify the device on which the code will run. Set it to *`"cpu"`* or *`"gpu"`* to run the code on the central processing unit (CPU) or graphics processing unit (GPU), respectively.
* `device_rank` : For systems with multiple GPUs, this parameter specifies the GPU device on which the code will run. It accepts values from 0 (corresponding to the first GPU) to (number of GPUs - 1). The default value is 0.
* `(Lx, Ly, Lz)` and `(Nx, Ny, Nz)` : These parameters define the box lengths and grid sizes along the $x-, \ y-$, and $z-$ directions. In two-dimensional simulations (2D runs), set `Lz` (length in z-direction) and `Nz` (number of grid points in z-direction) to 1.

* `tamx, dt` :The `tmax` parameter specifies the total simulation time. It defines the maximum duration for which the simulation will run. The `dt` parameter, on the other hand, determines the time step size. 

* `g` : Sets the value of nonlinearity in the system.
* `init_usrdef` : This parameter controls whether the initial condition is defined by the user or by the code itself. It accepts Boolean values: *`True`* for user-defined initial conditions and *`False`* for code-defined initial conditions. The user can define user-defined initial conditions in two ways.
    - The first way is to provide the path of the input directory to the parameter `in_path` containing initial wavefunction and potential data in the form of HDF5 files named `wfc.h5` and `pot.h5`. The datasets inside the `wfc.h5` and `pot.h5` files should be named `wfc` and `pot`, respectively. 
    - The second way of defining the user-defined initial condition is through the `main.py` file which is described [here](#mainpy).  

    For the *`False`* values of `init_usrdef` i.e., for code defined initial condition, the user needs to set the `init_cond` parameter.

* `init_cond` :  If `init_usrdef` parameter is *`False`*, it will set the type of the code defined initial condition. In 2D simulations, it can take the values *`"rp"`* (random phase), *`"vl"`* (vortex lattice), and *`"rv"`* (random vortex). The number of vortices for *`"vl"`* and *`"rv"`* is specified in the quTARANG/initial_cond/dimension2.py file can be change accordingly inside the same file. For 3D simulations, only the *`"rp"`* (random phase) option is available. If init_usrdef is set to *`True`*, leave it unchanged.

* `in_path` : Sets the path to the input directory containing the initial wavefunction and potential data if `init_usrdef` is *`True`* and the wants to provide initial condition through input files. 

* `op_path` : Sets the path for the output folder where the data of the output will be stored.
* `scheme` : Sets the scheme for the simulation. Currently, only the Time-splitting pseudo-spectral (TSSP) scheme is implemented in the code. Therefore, the parameter can only take the value *`"TSSP"`*.
* `imgtime` : To compute the ground state, set this parameter to *`True`*. The code will then utilize the imaginary time approach to find the ground state.
* `delta` : This parameter will sets the stopping criteria in case of computing the ground state. The deafault value of this parameter is *`1e-12`*.
* `resume` : If the user wants to extend a simulation run, the user can do so by increasing the value of the `tmax` parameter and setting `resume` parameter to *`True`*.  The code will automatically load the most recently saved wavefunction and resume the simulation from that point.
* `overwrite` : If the output folder already contains data and the user wants to overwrite it, he can do so by simply setting this parameter to *`True`*.
* `wfc_start_step, wfc_iter_step` :  The `wfc_start_step` parameter determines the number of iterations after which the wavefunction starts saving. The `wfc_iter_step` parameter then controls the interval between subsequent wavefunction saves.
* `save_rms, rms_start_step, rms_iter_step` : The `save_rms` parameter controls whether the code saves the root mean square (RMS) value of the condensate. Set it to *`True`* to enable saving RMS values otherwise set it to *`False`*. If user choose to enable RMS data saving, the `rms_start_step` and `rms_iter_step` parameter comes into play. `rms_start_step` parameter determines the number of iterations after which the RMS values are first saved and then `rms_iter_step` controls the interval between subsequent saves.

* `save_en, en_start_step, en_iter_step` : Similarly, the `save_en` parameter controls whether the code saves energy data, while `en_start_step` and `en_iter_step` determine the starting iteration and interval for subsequent energy saves, respectively.
* `t_print_step` : Sets the interval of no of after which the code will print on the terminal.



2. Modify the following `main.py` file:
The user can 
#### main.py 


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
3. Once the `para.py` and `main.py` file sets, the one can run the simulations using:

```python
python main.py
```
## 3) Output format



## 4) Postprocessing 
1. Once the output from the ***quTARANG*** has been generated inside the output folder, the user can postprocess the data using the functions inside the `postprocessing` folder. The structre directories and files inside the `postprocessing` folder is as follows:
```
├── plot_energy.py
├── plot_rms.py
├── plot_spectra.ipynb
└── postprocessing
    ├── config.py
    └── libs
```
The main file inside the `postprocessing` folder is `config.py` file, where user will set the location of the output data folder. Once it is done the user can plot energy and rms evolution by running `plot_energy.py` file and `plot_rms.py` respectively. The output plots will be stored inside a postprocessing folder which will be created while postprocessing inside output folder. The jupyter-notebook `plot_spectra.ipynb` contains the commands to generate the spectra and fluxes with the description of them in form of comments. 
