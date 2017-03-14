from setuptools import setup

setup(name='json_api_mapper',
      version='0.0.1',
      description='JSON API mapper',
      url='https://github.com/kundo/json_api_mapper',
      author='Kundo',
      author_email='dev@kundo.se',
      license='MIT',
      packages=['json_api_mapper'],
      install_requires=[
          'jsonpointer',
          'python-dateutil',
          'six',
      ],
      zip_safe=False)
