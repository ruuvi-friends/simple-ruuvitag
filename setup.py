from setuptools import setup

import simple_ruuvitag

try:
    import pypandoc
    readme = pypandoc.convert_file('README.md', 'rst')
    readme = readme.replace('\r', '')
except ImportError:
    import io
    with io.open('README.md', encoding='utf-8') as f:
        readme = f.read()

setup(name='simple_ruuvitag',
      version=simple_ruuvitag.__version__,
      description='Find RuuviTag sensor beacons and get data from selected sensors',
      long_description=readme,
      url='https://github.com/sergioisidoro/simple-ruuvitag',
      download_url='https://github.com/sergioisidoro/simple-ruuvitag' +
                   simple_ruuvitag.__version__,
      author='Sergio Isidoro',
      author_email='smaisidoro@gmail.com',
      platforms='any',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
      ],
      keywords='RuuviTag BLE',
      install_requires=[
          'bleson==0.0.10'
      ],
      license='MIT',
      packages=['simple_ruuvitag', 'simple_ruuvitag.adaptors'],
      include_package_data=True,
      tests_require=[
          'nose',
          'mock'
      ],
      test_suite='nose.collector',
      zip_safe=True)
