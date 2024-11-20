from setuptools import setup, find_packages

setup(
    name='gitsync',
    version='0.1.0',
    description='Sync folders from a git repo to local folders',
    author='Romain Ferrali',
    author_email='romain.ferrali@univ-amu.fr',
    url='https://github.com/yourusername/gitsync',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gitsync=gitsync.cli:cli',
        ]
    },
    include_package_data=True,
    package_data={
        'gitsync': ['data/gitsync.json']
    },
    install_requires=['click','GitPython','python-dotenv'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL 3.0 License',
        'Operating System :: OS Independent',
    ],
)