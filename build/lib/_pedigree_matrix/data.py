# -*- coding: utf-8 -*
from collections import defaultdict


basic_uncertainty = {
    "demand": {
        "thermal energy, electricity, semi-finished products, working material, waste treatment services":
            defaultdict(lambda: 1.05),
        "transport services (tkm)":
            defaultdict(lambda: 2),
        "Infrastructure":
            defaultdict(lambda: 3)
        },
    "resources": {
        "primary energy carriers, metals, salts":
            defaultdict(lambda: 1.05),
        "land use, occupation": {
            "combustion": 1.5,
            "process": 1.5,
            "agricultural": 1.1
            },
        "land use, transformation": {
            "combustion": 2,
            "process": 2,
            "agricultural": 1.2
            }
        },
    "water": {
        "BOD, COD, DOC, TOC, inorganic compounds": {
            "process": 1.5
            },
        "individual hydrocarbons, PAH": {
            "process": 3
            },
        "heavy metals": {
            "process": 1.5,
            "agricultural": 1.5
            },
        "NO3, PO4": {
            "agricultural": 1.2
            }
        },
    "soil": {
        "oil, hydrocarbon total": {
            "process": 1.5
            },
        "heavy metals": {
            "process": 1.5,
            "agricultural": 1.5
            },
        "pesticides": {
            "agricultural": 1.2
            }
        },
    "air": {
        "CO2": {
            "combustion": 1.05,
            "process": 1.05
            },
        "SO2": {
            "combustion": 1.05
            },
        "NMVOC total": {
            "combustion": 1.5
            },
        "NOx, N2O": {
            "combustion": 1.5,
            "agricultural": 1.4
            },
        "CH4, NH3": {
            "combustion": 1.5,
            "agricultural": 1.2
            },
        "individual hydrocarbons": {
            "combustion": 1.5,
            "process": 2
            },
        "PM>10": {
            "combustion": 1.5,
            "process": 1.5
            },
        "PM10": {
            "combustion": 2,
            "process": 2
            },
        "PM2.5": {
            "combustion": 3,
            "process": 3
            },
        "polycyclic aromatic hydrocarbons (PAH)": {
            "combustion": 3
            },
        "CO, heavy metals": {
            "combustion": 5
            },
        "inorganic emissions, others": {
            "process": 1.5
            },
        "radionuclides (e.g., Radon-222)": {
            "process": 3
            }
        }
    }

version_1 = {
    "reliability": (1., 1.05, 1.1, 1.2, 1.5),
    "completeness": (1., 1.02, 1.05, 1.1, 1.2),
    "temporal correlation": (1., 1.03, 1.1, 1.2, 1.5),
    "geographical correlation": (1., 1.01, 1.02, 1.02, 1.1),
    "further technological correlation": (1., 1., 1.2, 1.5, 2),
    "sample size": (1., 1.02, 1.05, 1.1, 1.2)
    }

version_2 = {
    "reliability": (1., 1.54, 1.61, 1.69, 1.69),
    "completeness": (1., 1.03, 1.04, 1.08, 1.08),
    "temporal correlation": (1., 1.03, 1.1, 1.19, 1.29),
    "geographical correlation": (1., 1.04, 1.08, 1.11, 1.11),
    "further technological correlation": (1., 1.18, 1.65, 2.08, 2.8),
    "sample size": (1., 1., 1., 1., 1.)
    }
