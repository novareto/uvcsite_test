from setuptools import setup, find_packages

version = '0.0'

setup(name='uvcsite',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[], 
      keywords="",
      author="",
      author_email="",
      url="",
      license="",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'dolmen.content',
                        'elementtree',
                        'grok',
                        'grokcore.startup',
                        'grokui.admin',
                        'hurry.jquery',
                        'hurry.workflow',
                        'hurry.zoperesource',
                        'lxml',
                        'megrok.layout',
                        'megrok.z3cform.base',
                        'megrok.z3cform.tabular',
                        'megrok.z3cform.ui',
                        'megrok.z3ctable',
                        'z3c.breadcrumb',
                        'z3c.formui',
                        'z3c.macro',
                        'z3c.menu.simple',
                        'z3c.schema2xml',
                        'z3c.template', # Needed for my custom Template
                        'z3c.testsetup',
                        'zc.blist',
                        'zope.app.homefolder',
                        'zope.app.cache',
                        'megrok.icon',
                            # Add extra requirements here
                            ],
          entry_points = """
          [console_scripts]
          uvcsite-debug = grokcore.startup:interactive_debug_prompt
      uvcsite-ctl = grokcore.startup:zdaemon_controller
      [paste.app_factory]
      main = grokcore.startup:application_factory
      """,
      )
