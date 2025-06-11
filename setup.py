from setuptools import setup, find_packages

NAME = "SqlQtTools"
VERSION = "0.0.5"
REQUIRES = ["PyQt6>=6.9.1", "SQLAlchemy>=2.0.41", "aiosqlite>=0.21.0"]

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
        'Programming Language :: Python :: 3.12',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Utilities'
    ]
)