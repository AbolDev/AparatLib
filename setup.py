# from setuptools import setup, find_packages

# setup(
#     name='AparatAPI',
#     version='0.1.0',
#     packages=find_packages(),
#     install_requires=[
#         'requests',
#     ],
#     author='Your Name',
#     author_email='your.email@example.com',
#     description='Aparat API interaction library',
#     long_description=open('README.md').read(),
#     long_description_content_type='text/markdown',
#     url='https://github.com/AbolDev/aparat-api',
#     classifiers=[
#         'Programming Language :: Python :: 3',
#         'License :: OSI Approved :: MIT License',
#         'Operating System :: OS Independent',
#     ],
#     python_requires='>=3.6',
# )

from setuptools import setup, find_packages

setup(
    name='AparatLib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Abol',
    author_email='abaqry8686@gmail.com',
    description='A library for interacting with the Aparat API',
    url='https://github.com/AbolDev/aparat-api',
)
