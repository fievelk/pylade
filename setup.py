from setuptools import setup, find_packages

setup(name='pylade',
      version='0.1',
      description='PyLaDe - Language Detection tool written in Python.',
      url='https://github.com/fievelk/pylade',
      author='Pierpaolo Pantone',
      author_email='24alsecondo@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_data={'pylade': ['data/*.json']},
      entry_points = {
        'console_scripts': [
            'pylade=pylade.console_scripts.detect:main',
            'pylade_train=pylade.console_scripts.train:main',
            'pylade_eval=pylade.console_scripts.evaluate:main'
            ],
        },
      install_requires=[
          'nltk',
      ],
      zip_safe=False)
