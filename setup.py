#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
	name='D-Tracker',
	version='0.0',
	author='Ricardo Ribeiro',
	author_email='ricardojvr@gmail.com',
	license='MIT',
	url='https://github.com/UmSenhorQualquer/d-track',
	packages=find_packages(),
	entry_points={
		'console_scripts':[
			'd-track-singlecam=dolphintracker.singlecam_tracker.singlecam_tracker:main',
			'd-track-smoothpath=dolphintracker.smooth_path.smooth_path:main',
			'd-track-render=dolphinrender.DolphinRender:main'
		]
	}
)
