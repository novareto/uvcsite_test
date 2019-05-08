import os
from setuptools import setup, find_packages

version = '2.8.1.dev0'


docs = os.path.join(os.path.dirname(__file__), 'docs')

desc = ""
with open(os.path.join(docs, 'CHANGES.txt'), 'r') as changes:
    desc += changes.read()


tests_require = [
    'zope.testbrowser',
    'zope.app.testing',
]


setup(name='uvcsite',
      version=version,
      description="Grok-Based CMS",
      long_description=desc,
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
          'dolmen.authentication',
          #'dolmen.app.layout',
          'dolmen.beaker',
          'dolmen.content',
          'dolmen.forms.base',
          'dolmen.forms.crud',
          'dolmen.forms.wizard',
          'dolmen.security.policies',
          'enum34',
          'formencode',
          'grok',
          'grokcore.chameleon',
          'grokcore.layout',
          'grokcore.registries',
          'grokcore.startup',
          'grokui.admin',
          'hurry.query',
          'hurry.workflow',
          'js.jquery_tablesorter',
          'lxml',
          'megrok.rendersource',
          'megrok.z3ctable',
          'plone.memoize',
          'profilehooks',
          'pyPdf',
          'reportlab',
          'repoze.filesafe',
          'repoze.profile',
          'setuptools',
          'unittest2',
          'uvc.api[grok]',
          'uvc.layout',
          'uvc.staticcontent',
          'uvc.tbskin',
          'uvc.validation',
          'uvc.widgets',
          'z3c.schema2json',
          'z3c.schema2xml',
          'zope.catalog',
          'zeam.form.layout',
          'zeam.form.table',
          'zeam.form.viewlet',
          'zope.app.locales',
          'zope.app.pagetemplate',
          'zope.app.renderer',
          'zope.app.wsgi [testlayer]',
          'zope.cachedescriptors',
          'zope.generations',
          'zope.i18n [compile]',
          'zope.pluggableauth',
          'zope.principalannotation',
          'zope.sendmail',
          ],
      extras_require={'test': tests_require},
      entry_points = """
      [paste.app_factory]
      main = grokcore.startup:application_factory
      [paste.filter_app_factory]
      registries = uvcsite.registries:provide_registries
      [zodbupdate]
      renames = uvcsite.homefolder:rename_dict
      """,
      )
