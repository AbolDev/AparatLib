from setuptools import setup, find_packages

setup(
    name='AparatLib',
    version='0.5.1',
    packages=find_packages(),
    author='Abol',
    author_email='abaqry8686@gmail.com',
    description='A library for interacting with the Aparat API',
    long_description=open('C:\\Users\\Bagheri\\Desktop\\projects\\python\\Github projects\\aparat\\README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AbolDev/AparatLib',
    license='MIT',
    install_requires=[
        'tqdm',
        'requests',
        'python-magic',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
    keywords = [
        'python', 'library', 'aparat', 'aparat-api', 'aparat-downloader',
        'aparat-playlist-downloader', 'aparat-uploader', 'aparat-upload', 'aparat-dl',
        'aparat-news', 'aparat-lib', 'aparat-python',
    ],
    entry_points={
        'console_scripts': [
            'aparat=aparat.cli:main',
        ],
    },
    project_urls={
        'Bug Tracker': 'https://github.com/AbolDev/AparatLib/issues',
        'Documentation': 'https://aparatlib.readthedocs.io/en/latest/',
        'Source Code': 'https://github.com/AbolDev/AparatLib',
    },
)
