import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='asyncio-buffer-iterable',
    version='0.0.0',
    author='Michal Charemza',
    author_email='michal@charemza.name',
    description='Utility function to parallelize pipelines of Python async iterables/generators',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/michalc/asyncio-buffer-iterable',
    py_modules=[
        'asyncio_buffer_iterable',
    ],
    python_requires='>=3.6.3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
    ],
)
