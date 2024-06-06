from setuptools import setup, find_packages

setup(
    name='AparatLib',
    version='0.4.1',
    packages=find_packages(),
    author='Abol',
    author_email='abaqry8686@gmail.com',
    description='A library for interacting with the Aparat API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AbolDev/AparatLib',
    install_requires=[
        'requests',
        'python-magic',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords = [
        'python', 'library', 'aparat', 'aparat-api', 'aparat-downloader',
        'aparat-playlist-downloader', 'aparat-uploader', 'aparat-upload', 'aparat-dl',
        'aparat-news', 'aparat-lib', 'aparat-python',
    ],
)
