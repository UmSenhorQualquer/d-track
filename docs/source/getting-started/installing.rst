.. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _installing-label:

*************
Install
*************

.. note:: 
  
   Currently only the environment configurations for Ubuntu 17 and MacOS X are available.



* Download and install `Anaconda <https://www.anaconda.com/download/#linux>`_ or `Miniconda <https://conda.io/miniconda.html>`_
* Download the environment configuration file for `Ubuntu 17 <https://raw.githubusercontent.com/UmSenhorQualquer/d-track/master/environment-ubuntu17.yml>`_ or for the `MacOSx <https://raw.githubusercontent.com/UmSenhorQualquer/d-track/master/environment-macosx.yml>`_.


  .. code-block:: bash

     #command to use on Ubuntu 17.10
     wget --no-check-certificate https://raw.githubusercontent.com/UmSenhorQualquer/d-track/master/environment-ubuntu17.yml

     #or 

     #command to use on MacOS X
     wget --no-check-certificate https://raw.githubusercontent.com/UmSenhorQualquer/d-track/master/environment-macosx.yml

* Open the terminal and execute the next command to install the python environment.

  .. code-block:: bash

     #environment to use on Ubuntu 17.10
     conda env create -f environment-ubuntu17.yml

     #or 

     #environment to use on MacOS X
     conda env create -f environment-macosx.yml

* Activate the environment.

  .. code-block:: bash

     source activate d-track-environment

* Clone the d-track repository.

  .. code-block:: bash

     git clone --recursive https://github.com/UmSenhorQualquer/d-track.git

* Change the current directory to the d-track folder.

  .. code-block:: bash

     cd d-track

* Run the installation script.

  .. code-block:: bash

     python install.py
