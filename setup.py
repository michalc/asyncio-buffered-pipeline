import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='asyncio-buffered-pipeline',
    version='0.0.5',
    author='Michal Charemza',
    author_email='michal@charemza.name',
    description='Parallelize pipelines of Python async iterables/generators',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/michalc/asyncio-buffered-pipeline',
    py_modules=[
        'asyncio_buffered_pipeline',
    ],
    python_requires='>=3.7.1',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
    ],
)
