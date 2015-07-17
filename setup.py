import os
import factsbeach

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = []

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(name='Factsbeach',
      version=factsbeach.__version__,
      description='Factsbeach',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='factsbeach pyaella',
      packages=find_packages(),
      include_package_data=True,
      package_data={'':[
          '*.mako', '*.yaml', '*.csv',
          '*.sql', '*.css', '*.sass',
          '*.js', '*.rb', '*.txt'
      ]},
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="factsbeach",
      entry_points="""      [paste.app_factory]
      main = pyaella.server.instance:main
      """,
      )