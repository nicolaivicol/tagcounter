from setuptools import setup, find_packages

setup(name='tagcounter',
      version='0.1.0',
      description='Counting tags in a web page',
      long_description='This package is a lab work for course: Introduction to python N13.',
      keywords='python basic html',
      # url='',
      author='Nicolai Vicol',
      author_email='nicolaivicol@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['markdown'],
      include_package_data=True,
      zip_safe=False)