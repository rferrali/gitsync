from setuptools import setup, find_packages

setup(
    name='papersync',
    version='0.1.0',
    description='Sync folders from a git repo to local folders',
    author='Romain Ferrali',
    author_email='rferrali@gmail.com',
    url='https://github.com/rferrali/papersync',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'papersync=papersync.cli:cli',
        ]
    },
    include_package_data=True,
    package_data={
        'papersync': ['data/papersync.yaml']
    },
    install_requires=['click','GitPython','python-dotenv'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL 3.0 License',
        'Operating System :: OS Independent',
    ],
)