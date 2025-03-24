from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='cypherctf-bot',
    version='1.0.0',
    author='strangeprogram',
    author_email='blowfish@hivemind',
    description='An advanced IRC-based Capture The Flag (CTF) game bot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/strangeprogram/cypherctf-bot',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'irc3>=1.9.0',
        'python-dotenv>=0.19.0',
    ],
    entry_points={
        'console_scripts': [
            'cypherctf-bot=bot:main',
        ],
    },
) 