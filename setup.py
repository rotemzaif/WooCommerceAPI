from setuptools import setup, find_packages

setup(name='woocommercetest',
      version='1.0',
      description='Practice API testing',
      author='Rotem Zaif',
      author_email='rotem8zaif@gmail.com',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          "pytest==7.1.3",
          "pytest-html==3.2.0",
          "requests==2.28.2",
          "requests-oauthlib==1.3.1",
          "PyMySQL==1.0.2",
          "allure-pytest=2.13.2",
          "WooCommerce==3.0.0",
      ]
      )
