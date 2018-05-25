.. d-track documentation master file, created by
   sphinx-quickstart on Mon Jan 30 09:40:02 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



D-Track
=====================================

D-Track is a suite of software used to track an object in 3D based on the 3D schematics of a scene. These set of software was used to calculate and analyse the 3D position of a dolphin in a pool in `Zoomarine @ Portugal <https://www.zoomarine.pt/pt/>`_.

**D-Track applications**

=================================   ==========================================================================================
d-track-singlecam                   Extracts 2d information, used for the tracking, from a recording captured by a single camera.
d-track-smoothpath                  Combine the 2 cameras 2d information to find the 3d path.
d-track-render                      Render the resulting 3d path into a 3d scene.
=================================   ==========================================================================================

**Other software used in the project**

=====================================================================================   ==========================================================================
`Python Video Annotator <https://pythonvideoannotator.readthedocs.io>`_                 Software used to correct values from the 2d tracking.
`Python 3D Engine <https://python-3d-engine.readthedocs.io>`_                           Python library for 3d physics simulation.
`Python 3D Scene Editor <https://python-3d-scene-editor.readthedocs.io>`_               Software to create 3d scenes to be used with the py3dengine library.
`3D-tracking-analyser <https://github.com/UmSenhorQualquer/3D-tracking-analyser>`_      Software to visualize and analyse the results of the 3d tracking.
=====================================================================================   ==========================================================================


.. raw:: html
   
   <iframe width="700" height="270" src="https://www.youtube.com/embed/4KGe94g8F3g?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

|

Developers & collaborations
--------------------------------------

=================================   ============================================================================================================================================
Ricardo Ribeiro                     from the `Champalimaud Scientific Software Platform <http://neuro.fchampalimaud.org/en/research/platforms/staff/Scientific%20Software/>`_
                                       ricardo.ribeiro@research.fchampalimaud.org
Patrícia Rachinas Lopes             from the `MARE-ISPA <http://www.mare-centre.pt/en/user/164>`_
                                       plopes@ispa.pt
Dolphins                            `Zoomarine @ Portugal <https://www.zoomarine.pt/en/>`_
=================================   ============================================================================================================================================

|

.. image:: /_static/zoomarine-logo.png
   :target: https://www.zoomarine.pt
   :align: left

.. image:: /_static/ispa-logo.png
   :target: http://www.ispa.pt/
   :align: left

.. image:: /_static/MARE-logo.png
   :target: http://www.mare-centre.pt/en/
   :align: left

.. image:: /_static/cf-logo.png
   :target: https://neuro.fchampalimaud.org

|

Code on Github
---------------------------------

.. image:: /_static/github.png
   :target: https://github.com/UmSenhorQualquer/d-track







.. high level toc tree

.. toctree::
   :hidden:
   :maxdepth: 2
   :includehidden:
   :caption: Getting started

   Introduction <self>
   getting-started/installing
   getting-started/running

.. toctree::
   :hidden:
   :maxdepth: 4
   :includehidden:
   :caption: User manual

   user-manual/how-to-use
   user-manual/example