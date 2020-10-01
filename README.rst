=========================================================================
BioSTEAM_LCA: The Biorefinery Simulation Module with Techno-Economic Analysis and Life Cycle Assessment
=========================================================================

.. image:: http://img.shields.io/pypi/v/biosteam-lca.svg?style=flat
   :target: https://pypi.org/project/biosteam-lca/
   :alt: Version_status
.. image:: http://img.shields.io/badge/license-UIUC-blue.svg?style=flat
   :target: https://github.com/scyjth/biosteam_lca/blob/master/LICENSE.txt
   :alt: license
.. image:: https://img.shields.io/pypi/pyversions/biosteam.svg
   :target: https://pypi.python.org/pypi/biosteam
   :alt: Supported_versions
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: Formatted with Black





Biosteam_LCA is an an agile life cycle assessment (LCA) platform that enables the fast and flexible evaluation of the life cycle environmental impacts of biorefineries under uncertainty. It interfaces with BioSTEAM to simultaneously characterize environmental and economic metrics while enabling complete flexibility for user-defined biofuels, bioproducts, biomass compositions, and processes. This open-source, installable package allows users to perform streamlined LCAs of biorefineries. The focus of BioSTEAM-LCA is to streamline and automate early-stage environmental impact analyses of processes and technologies, and to enable rigorous sensitivity and uncertainty analyses linking process design, performance, economics, and environmental impacts.

Installation
------------

Get the latest version from `PyPI <https://pypi.org/project/biosteam-lca/>`__. If you have an installation of Python with pip, simple install it with:

    $ pip install biosteam_lca

To get the git version, run:

    $ git clone git://https://github.com/scyjth/biosteam_lca/tree/master/biosteam_lca


Prerequisites
-------------

- Valid [ecoinvent](https://www.ecoinvent.org) login credentials
- Alternatively, several open source life cycle inventory databases are built in, such as [FORWAST](https://lca-net.com/projects/show/forwast/)

Where the inventory inputs can be chosen from any of the supported databases:

==========  ================
Database    ``inputs``
==========  ================
Ecoinvent   ``'ecoinvent'``
FORWAST     ``'forwast'``
U.S LCI     ``'us-lci'``
==========  ================


License information
-------------------

See ``LICENSE.txt`` for information on the terms & conditions for usage
of this software, and a DISCLAIMER OF ALL WARRANTIES.


About the authors
-----------------

BioSTEAM_LCA was created and developed by Dr. Rui Shi as part of the `Guest Group <http://engineeringforsustainability.com/>`__ and the `Center for Advanced Bioenergy and Bioproducts Innovation (CABBI) <https://cabbi.bio/>`__ at the `University of Illinois at Urbana-Champaign (UIUC) <https://illinois.edu/>`__. 

References
----------
[1] Shi, Rui and Jeremy S. Guest, "BioSTEAM-LCA: An Integrated Modeling Framework for Agile Life Cycle Assessment of Biorefineries Under Uncertainty. " ACS Sustainable Chemistry & Engineering. Under review. 

