from setuptools import setup, find_packages

setup(
    name='AlgoTradingMonitor',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'', 'src'},
    extras_require=dict(tests=['pytest'])
)
