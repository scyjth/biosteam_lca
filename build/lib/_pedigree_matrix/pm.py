# -*- coding: utf-8 -*
from .data import basic_uncertainty, version_1, version_2
import math


class PedigreeMatrix(object):
    labels = (
        "reliability",
        "completeness",
        "temporal correlation",
        "geographical correlation",
        "further technological correlation",
        "sample size"
        )

    def __init__(self, *args):
        self.pm_factors = version_1
        self.inputs = self.pad_args(self.parse_args(args))
        self.args = self.lookup_inputs()
        self.basic_uncertainty = 1.
        self.version = 1

    def denester(self, keys, data):
        keys = list(keys)
        while keys:
            data = data[keys.pop(0)]
        return data

    def use_new_factors(self):
        self.pm_factors = version_2
        self.args = self.lookup_inputs()

    def use_old_factors(self):
        self.pm_factors = version_1
        self.args = self.lookup_inputs()

    def lookup_inputs(self):
        return [self.pm_factors[key][index - 1] for key, index in \
            zip(self.labels, self.inputs)]

    def add_basic_uncertainty(self, *keys):
        try:
            self.basic_uncertainty = self.denester(basic_uncertainty, keys)
        except KeyError:
            raise ValueError("This basic uncertainty could not be found.")

    def parse_args(self, args):
        def maybe_int(x):
            try:
                return int(x)
            except:
                return 1.
        """
Parse input into usable form.

``args`` can be one of three data formats:

* "(1,2,3,4,5,6)": A string, e.g. the Ecospold 1 format.
* (1, 2, 3, 4, 5): A tuple of floats, which require no additional processing.
* ("1", "2", "3", "4", "5"): A tuple of strings, e.g. input from a web app.
        """
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            args = args[0]
        elif len(args) == 1 and isinstance(args[0], basestring):
            args = args[0].replace("(", "").replace(")", "").split(",")
        return [maybe_int(x) for x in args]

    def pad_args(self, args):
        """Pad ``args`` to a length of 6 with zeros (for consistency)."""
        if len(args) < 6:
            missing = 6 - len(args)
            args = args + [1, ] * missing
        elif len(args) > 6:
            raise ValueError
        return args

    def unpack_args(self):
        return zip(self.labels, self.inputs, self.args)

    def calculate_uncertainty(self, include_basic_uncertainty=True):
        if include_basic_uncertainty:
            args = self.args + [self.basic_uncertainty, ]
        else:
            args = self.args
        return math.sqrt(sum([math.log(x) ** 2 for x in args])) / 2

    def geometric_standard_deviation(self, include_basic_uncertainty=True):
        return math.sqrt(math.exp(
            self.calculate_uncertainty(include_basic_uncertainty)))
