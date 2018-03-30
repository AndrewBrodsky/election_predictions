from distutils.core import setup

setup(
	name='CensusData',
	version='1.0.post2',
	description='Download data from U.S. Census API',
	long_description=open('README.rst').read(),
	url='https://github.com/jtleider/censusdata',
	author='Julien Leider',
	author_email='jtleider@gmail.com',
	license='MIT',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 2.7',
	],
	keywords='census',
	packages=['censusdata',],
	install_requires=['pandas', 'requests',],
	python_requires='>=2.7, >=3',
	package_data={
		'censusdata': ['variables/*.json',],
	}
)

