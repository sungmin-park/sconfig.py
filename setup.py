from setuptools import setup

setup(
    name='sconfig',
    version='0.0.2',
    license='MIT',
    url='https://github.com/sungmin-park/sconfig.py',
    author='Park Sung Min',
    description='Simple config',
    packages=['sconfig'],
    install_requires=[],
    extras_require={
        'dev': [
            'pytest==3.6.3',
            'pytest-mock==1.10.0',
            'wheel==0.31.1',
            'twine==1.11.0'
        ]
    }
)
