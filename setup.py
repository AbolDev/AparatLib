from setuptools import setup, find_packages

setup(
    name='AparatLib',
    version='0.1.3',
    packages=find_packages(),
    author='Abol',
    author_email='abaqry8686@gmail.com',
    description='A library for interacting with the Aparat API',
    long_description=open('C:\\Users\\Bagheri\\Desktop\\projects\\python\\Github projects\\aparat\\README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AbolDev/AparatLib',
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="Aparat API video streaming python",
    python_requires='>=3.6',
)
