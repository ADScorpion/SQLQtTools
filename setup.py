import sys
from setuptools import setup, find_packages

python_version = sys.version_info

NAME = "SqlQtTools"
VERSION = "0.1.18"
REQUIRES = ["SQLAlchemy>=2.0.41", "aiosqlite>=0.21.0"]

if python_version >= (3, 10):
    REQUIRES.append('PySide6>=6.9.1')
else:
    REQUIRES.append('PySide2>=5.15.0')

setup(
    name=NAME,
    version=VERSION,
    url='https://github.com/ADScorpion/SQLQtTools',
    author='Sergey Skalozub',
    description='SQLQtTool README',
    keywords=[],
    long_description='SQLQtTool long README',
    license='MIT',
    packages=find_packages(),
    install_requires=REQUIRES,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Utilities'
    ]
)