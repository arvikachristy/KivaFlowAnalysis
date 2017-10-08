from setuptools import setup, find_packages

setup(
    name='ingest',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    description='An application that utilises Kiva API and analyses its data',
    author='Vika Christy',
    author_email='anastasia.arvika@gmail.com',
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'flask',
        'gunicorn',
        'psycopg2',
        'requests',
    ],
)
