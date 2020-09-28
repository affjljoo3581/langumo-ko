from setuptools import setup, find_packages

setup(
    name='langumo-ko',
    version='0.1.0',

    author='Jungwoo Park',
    author_email='affjljoo3581@gmail.com',

    description='한국어 말뭉치용 langumo parser 모음',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',

    keywords=['langumo', 'corpus', 'dataset', 'nlp', 'language-model',
              'deep-learning', 'machine-learning', 'korean'],
    url='https://github.com/affjljoo3581/langumo-ko',
    license='Apache-2.0',

    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='>=3.6.0',
    install_requires=[
        'langumo',
        'ijson>=3.1.1'
    ],

    classifiers=[
        'Environment :: Console',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ]
)
