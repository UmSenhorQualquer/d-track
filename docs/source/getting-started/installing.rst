.. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _installing-label:

**********
Installing
**********

Install the Windows binary files
--------------------------------

* Download the zip file containing the `windows binaries files <https://bitbucket.org/fchampalimaud/d-track/downloads>`_.
* Uncompress the zip file to a folder.
* The application is ready to be used.

--------------------------- 

|

Install the source code
--------------------------------

.. warning::
   This project was developed and tested with Python 2.7 running on Ubuntu 14.04.5 LTS (Trusty Tahr).

Requirements
~~~~~~~~~~~~~~~~~~~~~~

====================	=============
**LIBRARY**				  **VERSION**
Python 					        2.7.6
Numpy 					        1.8.2
OpenCV 					        3.1.0
PyOpenGL 				      3.1.1a1
PyOpenGL_accelerate 	      3.1.1a1
PyForms 				    v1.0.beta
csv 					          1.0
py3dengine				          0.0
====================	=============


Installation
~~~~~~~~~~~~~~~~~~~~~~

* Ubuntu already comes with python 2.7 installed, therefore there is not need to install python.
* Download and install the source code of `Numpy 1.8.2 <https://sourceforge.net/projects/numpy/files/NumPy/1.8.2/>`_
* Download the OpenCV library from the `opencv.org <http://opencv.org/downloads.html>`_ website, and follow the instructions to compile and install it with cmake.
* Execute the command: ``sudo pip2.7 install pyopengl pyopengl_accelerate``
* Follow this `instructions <http://pyforms.readthedocs.io/en/v1.0.beta/#installation>`_ to install PyForms.
* Install the csv library using the command: ``sudo pip install csv==1.0``
* Install the py3dengine library using the command: ``sudo pip install git+https://UmSenhorQualquer@bitbucket.org/UmSenhorQualquer/py3dengine.git``
* Download an uncompress the d-tracker source code and install it using pip: ``sudo pip install git+https://github.com/UmSenhorQualquer/d-track.git``


