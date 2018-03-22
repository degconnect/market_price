from setuptools import setup


setup(name='market_price',
      version='0.02',
      description='API for market_price',
      keywords='crypto currencies exchanges',
      url='https://github.com/degconnect/market_price',
      author='DEGConnect',
      author_email='info@degconnect.com',
      license='MIT',
      packages=["market_price", ],
      install_requires=[
          'requests==2.18.1',
          'weightedstats==0.3',
          'python-bittrex==0.3.0',
          # 'git+git://github.com/edilio/cryptopia.git',
            
      ],
      zip_safe=False
      )

