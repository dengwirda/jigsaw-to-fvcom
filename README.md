## `JIGSAW-to-FVCOM`

A simple interface between the `JIGSAW` mesh generator and `FVCOM` ocean model.

### `Quickstart`

`JIGSAW-to-FVCOM` requires the `JIGSAW` meshing package be installed. `JIGSAW`'s `Python` interface is available <a href="https://github.com/dengwirda/jigsaw-python">here</a>. Once installed, the example problems can be run via:

    clone/download + unpack this repository.
    python3 ex_1.py
    python3 ex_2.py

`JIGSAW` itself can either be built directly from src, or installed using the <a href="https://anaconda.org/conda-forge/jigsaw">`conda`</a> package manager (recommended):

    conda create -n jigsaw_plus python=3.7 netCDF4 scipy jigsaw jigsawpy

Each time you want to use `JIGSAW` simply activate the environment using: `conda activate jigsaw_plus`

Once activated, `JIGSAW's` various command-line utilities and `Python` front-end will be available to the `JIGSAW-to-FVCOM` utilities contained in this repository.

### `Example Problems`

The following set of example problems are available in `JIGSAW-to-FVCOM`:

    example: 1; # generate a simple "box" domain with non-uniform mesh spacing
    example: 2; # generate an example modelling domain for the Saco bay region
    
Run `python3 ex_1.py` or `python3 ex_2.py` to call the examples scripts. On completion, `*.dat` input files for `FVCOM` are saved locally. `*.vtk` output is also exported allowing meshes to be visualised with, for example, <a href=https://www.paraview.org/>Paraview</a>.

### `License`

This program may be freely redistributed under the condition that the copyright notices (including this entire header) are not removed, and no compensation is received through use of the software.  Private, research, and institutional use is free.  You may distribute modified versions of this code `UNDER THE CONDITION THAT THIS CODE AND ANY MODIFICATIONS MADE TO IT IN THE SAME FILE REMAIN UNDER COPYRIGHT OF THE ORIGINAL AUTHOR, BOTH SOURCE AND OBJECT CODE ARE MADE FREELY AVAILABLE WITHOUT CHARGE, AND CLEAR NOTICE IS GIVEN OF THE MODIFICATIONS`. Distribution of this code as part of a commercial system is permissible `ONLY BY DIRECT ARRANGEMENT WITH THE AUTHOR`. (If you are not directly supplying this code to a customer, and you are instead telling them how they can obtain it for free, then you are not required to make any arrangement with me.) 

`DISCLAIMER`:  Neither I nor: Columbia University, the Massachusetts Institute of Technology, the University of Sydney, nor the National Aeronautics and Space Administration warrant this code in any way whatsoever.  This code is provided "as-is" to be used at your own risk.

### `References`

Additional information and references regarding the formulation of the underlying `JIGSAW` mesh-generator can be found <a href="https://github.com/dengwirda/jigsaw">here</a>.
