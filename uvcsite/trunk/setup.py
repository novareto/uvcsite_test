from setuptools import setup, find_packages

version = '2.1.8.dev0'

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
          'dolmen.app.authentication',
          'dolmen.app.layout',
          'dolmen.beaker',
          'dolmen.content',
          'dolmen.forms.base',
          'dolmen.forms.crud',
          'dolmen.forms.wizard',
          'dolmen.security.policies',
          'elementtree',
          'grok',
          'grokcore.chameleon',
          'grokcore.layout',
          'grokcore.registries',
          'grokcore.startup',
          'grokui.admin',
          'hurry.workflow',
          'js.jquery_tablesorter',
          'lxml',
          'megrok.rendersource',
          'megrok.z3ctable',
          'mock',
          'plone.memoize',
          'profilehooks',
          'pyPdf',
          'reportlab',
          'repoze.filesafe',
          'repoze.profile',
          'setuptools',
          'unittest2',
          'uvc.layout',
          'uvc.staticcontent',
          'uvc.tbskin',
          'uvc.validation',
          'uvc.widgets',
          'uvckickstart',
          'z3c.schema2xml',
          'zeam.form.layout',
          'zeam.form.table',
          'zeam.form.viewlet',
          'zope.app.homefolder',
          'zope.app.locales',
          'zope.app.renderer',
          'zope.generations',
          'zope.i18n [compile]',
          'zope.pluggableauth',
          'zope.principalannotation',
          'zope.sendmail',
          'zope.testbrowser [zope-functional-testing]',
          ],
      entry_points = """
      [paste.app_factory]
      main = grokcore.startup:application_factory
      [paste.filter_app_factory]
      registries = uvcsite.registries:provide_registries
      """,
      )
