from distutils.core import setup

setup(
    name='lsd',
    version='0.0.0',
    author='Michal Grzedzicki',
    author_email='lazy@iq.pl',
    packages=['lds','lds.video','lds.net'],
    scripts=['bin/makeHtaccess.py',],
    description='Supermagiczny leniwy digitall signage',
)