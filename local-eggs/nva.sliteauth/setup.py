from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='nva.sliteauth',
      version=version,
      description="Sample SQLite User Database for Demonstration and Testing",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Christian Klinger',
      author_email='cklinger@novareto.de',
      url='www.novareto.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['nva'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
	  'grok',
	  'pysqlite',
	  'z3c.testsetup',
          # -*- Extra requirements: -*-
      ],
      )
