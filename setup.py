from setuptools import setup, find_packages


with open("README.md") as f:
    long_description = f.read()


setup(
    name="cherab-jet",
    version="1.1.0dev1",
    license="EUPL 1.1",
    namespace_packages=["cherab"],
    description="Cherab spectroscopy framework: JET machine submodule",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    url="https://github.com/cherab",
    project_urls=dict(
        Tracker="https://github.com/cherab/jet/issues",
        Documentation="https://cherab.github.io/documentation/",
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["cherab"],
)
