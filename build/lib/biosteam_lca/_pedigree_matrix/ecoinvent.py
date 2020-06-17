from .pm import PedigreeMatrix
import re


comment_matcher = re.compile("^\([0-9na, ]*\)")


def from_ei_text(comment):
    """Create PedigreeMatrix from ecoinvent comment text"""
    factors = comment_matcher.match(comment).group()
    assert factors, "No formatted comment found"
    return PedigreeMatrix(factors)
