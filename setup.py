from setuptools import setup, find_packages


setup(
    name="participationgraphs",
    version=__import__("participationgraphs").__version__,
    author="Matt Riggott",
    description="Django app with a template tag to allow you to include sparklines of the 52-week commit history for a project on Github",
    long_description=open("README.rst").read(),
    license="GPL",
    url="http://github.com/flother/participationgraphs",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
