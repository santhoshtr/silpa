from setuptools import setup, find_packages
setup(
    name = "silpa",
    version = "0.1-20100221",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    author = "Santhosh Thottingal",
    author_email = "santhosh.thottingal@gmail.com",
    description = "Silpa Indian Language Computing Library",
    license = "AGPL",
    keywords = "nlp indic",
    url = "http://smc.org.in/silpa",  

    # could also include long_description, download_url, classifiers, etc.
)
