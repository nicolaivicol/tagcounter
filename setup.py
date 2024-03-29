from setuptools import setup, find_packages

setup(name='tagcounter',
      version='0.1.0',
      description='Counting tags in a web page',
      long_description='This package is a lab work for course: Introduction to python #13.',
      keywords='python basic html',
      url='https://github.com/nicolaivicol/tagcounter',
      author='Nicolai Vicol',
      author_email='nicolaivicol@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['sqlalchemy',
                        'bs4',
                        'pyyaml',
                        'requests',
                        ],
      package_data={'tagcounter/data': ['*.db', '*.yml', '*.log']},
      include_package_data=True,
      entry_points={'console_scripts': ['tagcounter = tagcounter.main:run']},
      zip_safe=False,
      )
