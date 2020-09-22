# OverlApp
A simple tool to compute extent of spatial overlap associated with electronic transitions based on natural transition orbitals (NTOs)


<img src="https://github.com/danielsylvinson/OverlApp/blob/master/console.PNG"> 


Most quantum chemistry packages like (Gaussian, Q-Chem, Orca, etc.) have the the capability of generating NTOs for excited states. The spatial overlap integrals are computed numerically with the help of the ORBKIT [[1](https://orbkit.github.io/)] and Cubature [[2](https://pypi.org/project/cubature/)] libraries.  This tool accepts NTOs in the molden format and computes the spatial overlap integrals along with the mean absolute error of the integration scheme. It is asssumed that each molden file contains the NTOs of no more than one state. Multiple files  can be processed simultaneously and the results are summarized in a new file named "Overlap.txt" that will appear in the parent directory upon completion.

Note: So far, the tool has only been tested on NTOs generated by Q-Chem in Molden format.


## Install (pre-built binaries)

Windows users can directly download and install pre-built binaries from [here](https://github.com/danielsylvinson/OverlApp/blob/master/Win_build/OverlApp.zip).


## Install (from source)

Download the latest release

```
$ git clone https://github.com/danielsylvinson/OverlApp.git
```

## Dependencies
- Python (> 3.6)
- Numpy
- PyQt5 (For GUI)
- ORBKIT
- Cubature


Install dependencies:

To install ORBKIT, follow the instructions in the [ORBKIT page](https://orbkit.github.io/install.html)

To install other dependencies:
```
$ pip install pyqt5
$ pip install numpy
$ pip install cubature
```


## Usage
Run the following command to invoke GUI window
```
$ python OverlApp.py
```

OR

To run without GUI, run the OverlApp_cmdline.py script with the following arguments:
```
$ python OverlApp_cmdline.py [max_evaluations] [file1] [file2] ...... 
```
The first argument must always be a positive integer and refers to the maximum number of evaluations that will be attempted. Larger values result in denser grids and increased accuracy of the numerical integration. The arguments that follow are paths to the molden files for which the overlap integrals are evaluated.  

Example:
```
$ python OverlApp_cmdline.py 1000000 test1.molden test2.molden
```



## References

1.  Hermann,G.; Pohl,V.; Tremblay,J.C.; Paulus,B.; Hege,H.C.; Schild,A.,ORBKIT: A Modular Python Toolbox for -Platform Postprocessing of Quantum Chemical Wavefunction Data.Journal of Computational Chemistry 2016,37 (16),1511-1520.

2.  Castro,S.G.P.; Loukianov,A.; et.al.Python wrapper for Cubature: adaptive multidimensional integration,Version 0.14.3; 2020.
