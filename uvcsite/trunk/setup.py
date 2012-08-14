from setuptools import setup, find_packages

version = '2.1.a1'

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
          'unittest2',
          'dolmen.forms.base',
          'dolmen.forms.crud',
          'dolmen.forms.wizard',
          'dolmen.security.policies',
          'dolmen.app.authentication',
          'dolmen.app.layout',
          'elementtree',
          'grok',
          'grokcore.chameleon',
          'grokcore.startup',
          'grokcore.registries',
          'grokui.admin',
          'hurry.workflow',
          'js.jquery_tablesorter',
          'lxml',
          'megrok.layout',
          'megrok.rendersource',
          'megrok.z3ctable',
          'mock',
          'plone.memoize',
          'profilehooks',
          'reportlab',
          'repoze.profile',
          'setuptools',
          'uvc.layout',
          'uvc.staticcontent',
          'uvc.validation',
          'uvc.widgets',
          'uvc.tbskin',
          'uvckickstart',
          'z3c.schema2xml',
          'zeam.form.layout',
          'zeam.form.viewlet',
          'zeam.form.table',
          'zope.app.homefolder',
          'zope.app.renderer',
          'zope.app.locales',
          'zope.generations',
          'zope.i18n [compile]',
          'zope.pluggableauth',
          'zope.principalannotation',
          'zope.sendmail',
          'zope.testbrowser [zope-functional-testing]',
          ],
      entry_points = """
      [console_scripts]
      uvcsite-debug = grokcore.startup:interactive_debug_prompt
      uvcsite-ctl = grokcore.startup:zdaemon_controller
      [paste.app_factory]
      main = grokcore.startup:application_factory
      [paste.filter_app_factory]
      registries = uvcsite.registries:provide_registries
      """,
      )
