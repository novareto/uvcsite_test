from setuptools import setup, find_packages

version = '0.2.2dev'

setup(name='uvcsite',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[], 
      keywords="",
      author="UVC-WebCommnunity",
      author_email="cklinger@novareto.de",
      url="http://uvwebcommunity.bg-kooperation.de/",
      license="ZPL",
      package_dir={'': 'src'},
      packages=find_packages('src', exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'dolmen.app.site',
                        'dolmen.content',
                        'dolmen.menu',
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
                        'megrok.z3cform.wizard',
                        'megrok.z3cform.tabular',
                        'megrok.z3cform.ui',
                        'megrok.z3ctable',
                        'z3c.schema2xml',
                        'z3c.testsetup',
                        'zope.app.homefolder',
                        'zope.app.cache',
                        'uvc.skin',
                        'uvc.layout',
                        'uvc.widgets',
                        'uvc.validation',
                        'dolmen.app.layout',
                        'megrok.rendersource',
                        'dolmen.beaker',
                        'zope.sendmail',
                        'megrok.icon',
                        'uvckickstart',
                        'zeam.form.layout',
                        'dolmen.forms.base',
                        'dolmen.forms.crud',
                        'ipdb',
                       ],
          entry_points = """
          [console_scripts]
          uvcsite-debug = grokcore.startup:interactive_debug_prompt
      uvcsite-ctl = grokcore.startup:zdaemon_controller
      [paste.app_factory]
      main = grokcore.startup:application_factory
      """,
      )
