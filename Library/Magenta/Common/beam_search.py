"""Beam search library."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import copy
import heapq

# A beam entry containing 
# 	a. Current Sequence
# 	b. a "state" containing any information needed to extend the sequence, and
# 	c. a score for current sequence e.g. log-likelyhood.

BeamEntry = collections.nametuple('BeamEntry', ['sequence', 'state', 'score'])

def _generate_branches(beam_entries, generate_step_fn, branch_factor, num_steps):
	