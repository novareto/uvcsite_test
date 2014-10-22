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
          'GenericCache',
          'Paste',
          'WebOb',
          'barrel',
          'cromlech.browser',
          'cromlech.configuration',
          'cromlech.container',
          'cromlech.dawnlight >= 0.5',
          'cromlech.i18n',
          'cromlech.security',
          'cromlech.webob',
          'cromlech.zodb >= 0.3',
          'dawnlight',
          'docutils',
          'dolmen.beaker',
          'dolmen.breadcrumbs',
          'dolmen.container',
          'dolmen.content',
          'dolmen.forms.base',
          'dolmen.forms.crud',
          'dolmen.forms.wizard',
          'dolmen.forms.ztk',
          'dolmen.layout >= 0.4',
          'dolmen.location',
          'dolmen.menu',
          'dolmen.message',
          'dolmen.security.policies',
          'dolmen.tales',  # need for the "slot" component.
          'dolmen.template',
          'dolmen.view',
          'dolmen.viewlet',
          'elementtree',
          'fanstatic',
          'formencode',
          'grokcore.component',
          'grokcore.layout',
          'grokcore.registries',
          'grokcore.security',
          'hurry.workflow',
          'js.bootstrap',
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
          'setuptools',
          'traject',
          'transaction',
          'unittest2',
          'uvc.design.canvas',
          'uvc.homefolder',
          'uvc.staticcontent',
          'uvc.testcontent',
          #'uvc.themes.siguv',  # this is to test
          'uvc.themes.dguv',  # this is to test
          'uvc.api', # API TEST
          'uvc.validation',
          'uvc.widgets',
          'uvckickstart',
          'uvclight',
          'uvclight[auth]',
          'uvclight[zodb]',
          'webob',
          'z3c.schema2xml',
          'zope.cachedescriptors',
          'zope.component',
          'zope.event',
          'zope.generations',
          'zope.i18n [compile]',
          'zope.i18n',
          'zope.interface',
          'zope.location',
          'zope.schema',
          'zope.security',
          'zope.sendmail',
          'zope.testbrowser [zope-functional-testing]',
          ],
      entry_points = """
      [paste.app_factory]
      app = uvcsite.app:uvcsite

      [paste.filter_app_factory]
      registries = uvcsite.registries:provide_registries

      [pytest11]
      uvcsite_fixtures = uvcsite.tests.fixtures
      """,
      )
