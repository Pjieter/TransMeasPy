## Badges

(Customize these badges with your own links, and check https://shields.io/ or https://badgen.net/ to see which other badges are available.)

| fair-software.eu recommendations | |
| :-- | :--  |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/Pjieter/TransMeasPy) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/Pjieter/TransMeasPy)](https://github.com/Pjieter/TransMeasPy) |
| (3/5) community registry           | [![RSD](https://img.shields.io/badge/rsd-TransMeasPy-00a3e3.svg)](https://www.research-software.nl/software/TransMeasPy) [![workflow pypi badge](https://img.shields.io/pypi/v/TransMeasPy.svg?colorB=blue)](https://pypi.python.org/project/TransMeasPy/) |
| (4/5) citation                     | [![DOI](https://zenodo.org/badge/DOI/<replace-with-created-DOI>.svg)](https://doi.org/<replace-with-created-DOI>)|
| (5/5) checklist                    | [![workflow cii badge](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>/badge)](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>) |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| **Other best practices**           | &nbsp; |
| Static analysis                    | [![workflow scq badge](https://sonarcloud.io/api/project_badges/measure?project=Pjieter_TransMeasPy&metric=alert_status)](https://sonarcloud.io/dashboard?id=Pjieter_TransMeasPy) |
| Coverage                           | [![workflow scc badge](https://sonarcloud.io/api/project_badges/measure?project=Pjieter_TransMeasPy&metric=coverage)](https://sonarcloud.io/dashboard?id=Pjieter_TransMeasPy) || Documentation                      | [![Documentation Status](https://readthedocs.org/projects/TransMeasPy/badge/?version=latest)](https://TransMeasPy.readthedocs.io/en/latest/?badge=latest) || **GitHub Actions**                 | &nbsp; |
| Build                              | [![build](https://github.com/Pjieter/TransMeasPy/actions/workflows/build.yml/badge.svg)](https://github.com/Pjieter/TransMeasPy/actions/workflows/build.yml) |
| Citation data consistency          | [![cffconvert](https://github.com/Pjieter/TransMeasPy/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/Pjieter/TransMeasPy/actions/workflows/cffconvert.yml) || SonarCloud                         | [![sonarcloud](https://github.com/Pjieter/TransMeasPy/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/Pjieter/TransMeasPy/actions/workflows/sonarcloud.yml) || Link checker              | [![link-check](https://github.com/Pjieter/TransMeasPy/actions/workflows/link-check.yml/badge.svg)](https://github.com/Pjieter/TransMeasPy/actions/workflows/link-check.yml) |## How to use TransMeasPy

Instrument-agnostic electronic transport measurement framework built on top of qcodes. TransMeasPy structures experiments around independent (set) and dependent (measured) variables, captures comprehensive instrument and sample metadata for reproducibility, enforces safety limits, and supports adaptable, stoppable measurements.

The project setup is documented in [project_setup.md](project_setup.md). Feel free to remove this document (and/or the link to this document) if you don't need it.

## Installation

To install TransMeasPy from GitHub repository, do:

```console
git clone git@github.com:Pjieter/TransMeasPy.git
cd TransMeasPy
python -m pip install .
```

## Documentation

Include a link to your project's full documentation here.

## Contributing

If you want to contribute to the development of TransMeasPy,
have a look at the [contribution guidelines](CONTRIBUTING.md).

## Credits

This package was created with [Copier](https://github.com/copier-org/copier) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
