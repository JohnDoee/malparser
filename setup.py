#!/usr/bin/env python

from setuptools import setup


setup(name='malparser',
      version='1.1.4',
      description='Python package to access the MyAnimeList Anime',
      long_description=open('README.rst').read(),
      author='Anders Jensen',
      license='MIT',
      author_email='johndoee+malparser@tidalstream.org',
      url='https://github.com/JohnDoee/malparser',
      packages=['malparser'],
      install_requires=['requests', 'lxml'],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
