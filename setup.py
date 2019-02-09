from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='django-datatables-ajax',
      version='0.6',
      description=('Lightweight Django class for a full Datatables server processing implementation'),
      long_description=readme(),
      classifiers=[
                  'Development Status :: 5 - Production/Stable',
                  'License :: OSI Approved :: BSD License',
                  'Programming Language :: Python :: 3 :: Only',
                  'Operating System :: POSIX :: Linux'
                  ],
      url='https://github.com/peppelinux/django-datatables-ajax',
      author='Giuseppe De Marco',
      author_email='giuseppe.demarco@unical.it',
      license='BSD',
      packages=['datatables_ajax'],
      install_requires=['django'],
     )
