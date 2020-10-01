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

This package is continuing to develop, with new features and extensions being added.

Getting started
~~~~~~~~~~~~~~~~

Installation
------------

Get the latest version from `PyPI <https://pypi.org/project/biosteam-lca/>`__. This package can be installed through pip::

    $ pip install biosteam_lca

To get the git version, run:

    $ git clone git://https://github.com/scyjth/biosteam_lca/tree/master/biosteam_lca


Prerequisites
-------------

- Valid [ecoinvent](https://www.ecoinvent.org) login credentials
- Alternatively, several open source life cycle inventory databases are built in, such as [FORWAST](https://lca-net.com/projects/show/forwast/)


Setup
-------------

Linking to other LCA repositories
***************************************************


There has been more and more LCA researchers participating in open source communities. This `Dashboard <https://github.com/IndEcol/Dashboard/>`__  contains a list of all repositories for LCA researchers. BioSTEAM_LCA interfaces with these excellent packages to enable rapid translation of biorefinery designs/processes and laboratory scale results to systems-scale sustainability assessments. 

If you have not done so, add the required conda channels to your conda config file. You also need to install brightway and eidl. 
The recommended way (Sep 2020) to install with conda is:

    $ conda install -c conda-forge -c cmutel -c haasad brightway2

    $ conda install -c haasad eidl



Choose LCI Databases and impact assessment methods
***************************************************


User can create models using life cycle inventory data/datasets from any of the supported databases (including any version of the ecoinvent database, ecoinvent license required). LCI Database serves as a central source of critically reviewed, consistent, and transparent data. It allows users to objectively review and compare analysis results based on similar data collection and analysis methods.

Where the inventory inputs can be chosen from 

==========  ================
Database    ``inputs``
==========  ================
Ecoinvent   ``'ecoinvent'``
FORWAST     ``'forwast'``
U.S LCI     ``'us-lci'``
==========  ================

User can choose from over 840+ different impact assessment methods, and automatically calculate the impact scores for any unit processes. Other than specified by user, the default assessment methods will be `U.S. EPA TRACI2.0 <https://www.epa.gov/chemical-research/tool-reduction-and-assessment-chemicals-and-other-environmental-impacts-traci/>`__.


License information
~~~~~~~~~~~~~~~~

This project is licensed under the University of Illinois at Urbana-Champaign License. See the ``LICENSE.txt`` file for information on the terms & conditions, and a DISCLAIMER OF ALL WARRANTIES.


About the authors
~~~~~~~~~~~~~~~~

BioSTEAM_LCA was created and developed by Dr. Rui Shi as part of the `Guest Group <http://engineeringforsustainability.com/>`__ and the `Center for Advanced Bioenergy and Bioproducts Innovation (CABBI) <https://cabbi.bio/>`__ at the `University of Illinois at Urbana-Champaign (UIUC) <https://illinois.edu/>`__. 

References
~~~~~~~~~~~~~~~~
[1] Shi, Rui and Jeremy S. Guest, "BioSTEAM-LCA: An Integrated Modeling Framework for Agile Life Cycle Assessment of Biorefineries Under Uncertainty. " ACS Sustainable Chemistry & Engineering. Under review. 

