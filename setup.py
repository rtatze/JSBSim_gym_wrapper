from setuptools import setup, find_packages


setup(name='jsbsim_gym_wrapper',
      version='0.1',
      description='A simple open ai wrapper for jsbsim (flight dynamics model)',
      url='https://github.com/rtatze/JSBSim_gym_wrapper',
      author='',
      license='MIT',
      install_requires=[
            'numpy',
            'gym',
            'matplotlib',
            'jsbsim',
            'bokeh',
            'pandas',
            'toml'
      ],
      packages=find_packages(),
      classifiers=[
            'License :: OSI Approved :: MIT License',
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3.6',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      python_requires='>=3.6',
      include_package_data=True,
      zip_safe=False)
