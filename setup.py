#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import lamp


def main():

    install_requires = open("requirements.txt").read().splitlines()

    setuptools.setup(name="lamp",
        version=lamp.__version__,
        description="Liverpool Annotation of metabolites using Mass Spectrometry",
        long_description=open("README.rst").read(),
        long_description_content_type="text/x-rst",
        author="Wanchang Lin and Warwick Dunn",
        author_email="wanchang.lin@liverpool.ac.uk",
        url="https://github.com/wanchanglin/lamp",
        license="GPLv3",
        platforms=["Windows, UNIX"],
        keywords=["Metabolomics", "Mass spectrometry",
                  "Liquid-Chromatography Mass Spectrometry",
                  "Metabolite Annotation"],
        packages=setuptools.find_packages(),
        python_requires=">=3.10",
        # test_suite="tests.suite",
        install_requires=install_requires,
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Scientific/Engineering :: Bio-Informatics",
            "Topic :: Scientific/Engineering :: Chemistry",
            "Topic :: Utilities",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": [
                "lamp = lamp.__main__:main"
            ]
        }
    )


if __name__ == "__main__":
    main()
