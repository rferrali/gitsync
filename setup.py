from setuptools import setup, find_packages

setup(
    name='folder_sync',
    version='0.1.0',
    description='Sync folders from a git repo to local folders',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/folder_sync',
    packages=find_packages(),
    install_requires=['GitPython'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL 3.0 License',
        'Operating System :: OS Independent',
    ],
)