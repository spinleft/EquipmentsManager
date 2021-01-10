from setuptools import find_packages, setup

setup(
    name='manager',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'pymysql',
        'xlrd==1.2.0',
        'xlwt==1.3.0',
    ],
)