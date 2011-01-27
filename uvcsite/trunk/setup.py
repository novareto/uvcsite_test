from setuptools import setup, find_packages

version = '0.2.4dev'

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
      install_requires=[
          'docutils',
          'dolmen.app.site',
          'dolmen.app.layout',
          'dolmen.beaker',
          'dolmen.content',
          'dolmen.forms.base',
          'dolmen.forms.crud',
          'dolmen.forms.wizard',
          'dolmen.security.policies',
          'dolmen.app.authentication',
          'dolmen.app.layout',
          'elementtree',
          'grok',
          'grokcore.startup',
          'grokui.admin',
          'hurry.jquery',
          'hurry.jquerytools',
          'hurry.workflow',
          'hurry.zoperesource',
          'lxml',
          'megrok.layout',
          'megrok.rendersource',
          'megrok.z3ctable',
          'reportlab',
          'repoze.profile',
          'setuptools',
          'unittest2',
          'uvc.layout',
          'uvc.skin',
          'uvc.validation',
          'uvc.widgets',
          'uvckickstart',
          'z3c.schema2xml',
          'zeam.form.layout',
          'zope.app.exception',
          'zope.app.homefolder',
          'zope.app.renderer',
          'zope.generations',
          'zope.pluggableauth',
          'zope.principalannotation',
          'zope.sendmail',
          ],
      entry_points = """
      [console_scripts]
      uvcsite-debug = grokcore.startup:interactive_debug_prompt
      uvcsite-ctl = grokcore.startup:zdaemon_controller
      [paste.app_factory]
      main = grokcore.startup:application_factory
      """,
      )
