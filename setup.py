import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

if os.environ.get('DATABASE_URL', False):
    requires.append('psycopg2')

setup(name='triproutes',
      version='0.0',
      description='triproutes',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Tyghe Vallard',
      author_email='vallardt@gmail.com',
      url='http://www.tygertown.us',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='triproutes',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = triproutes:main
      [console_scripts]
      initialize_triproutes_db = triproutes.scripts.initializedb:main
      """,
      )
