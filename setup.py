from setuptools import setup

setup(name='language_detection',
      version='0.1',
      description='Language Detection Tools',
      url='http://github.com/fievelk/language-detection',
      author='Pierpaolo Pantone',
      author_email='24alsecondo@gmail.com',
      license='MIT',
      packages=['language_detection'],
      entry_points = {
        'console_scripts': [
            'langd_train=language_detection.train:main',
            'langd_eval=language_detection.evaluate:main',
            'langd=language_detection.detect:main',
            ],
        },
      zip_safe=False)
