.. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _installing-label:

*************
Install
*************

Install on Ubuntu 17.10
--------------------------------

* Download and install `Anaconda <https://www.anaconda.com/download/#linux>`_ or `Miniconda <https://conda.io/miniconda.html>`_
* Download yml file containing `environment configuration <https://raw.githubusercontent.com/UmSenhorQualquer/d-track/master/environment-ubuntu17.yml>`_.
* Open the terminal and excute the next commands to install the python environment.

  .. code-block:: bash

     conda env create -f environment-ubuntu17.yml

* Activate the environment.

  .. code-block:: bash

     source activate py3dengine-environment

* Clone the d-track repository.

  .. code-block:: bash

     git clone https://github.com/UmSenhorQualquer/d-track.git

* Change the current directory to the d-track folder.

  .. code-block:: bash

     cd d-track

* Run the installation script.

  .. code-block:: bash

     python install.py
