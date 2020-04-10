from setuptools import setup

__version__ = '0.0.3'

try:
    import pypandoc
    readme = pypandoc.convert_file('README.md', 'rst')
    readme = readme.replace('\r', '')
except ImportError:
    import io
    with io.open('README.md', encoding='utf-8') as f:
        readme = f.read()

setup(
    name='simple_ruuvitag',
    version=__version__,
    description='Find RuuviTag sensor beacons and get data from selected sensors',
    long_description=readme,
    url='https://github.com/ruuvi-friends/simple-ruuvitag',
    download_url='https://github.com/ruuvi-friends/simple-ruuvitag/archive/v' +
        __version__ + ".tar.gz",
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
        # 'bleson @ https://github.com/TheCellule/python-bleson/archive/RELEASE_0.0.16.zip#egg=bleson-0.0.13'
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
