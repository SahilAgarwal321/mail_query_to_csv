from setuptools import setup


setup(name='mail_query_to_csv',
      version='1.0',
      description='Retrieves SQL query from email, sends it to the database, sends data back in reply to the email',
      author='Sahil Agarwal',
      author_email='sahil.agarwal94@gmail.com',
      keywords='email mail SQL query queryparser SQLparser database',
      # url='',
      license='MIT',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Logging Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],

      packages=find_packages(),
      )
