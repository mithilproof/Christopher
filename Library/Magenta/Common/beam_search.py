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

	"""Performs a single iteration of branch generation for beam search.

  This method generates `branch_factor` branches for each sequence in the beam,
  where each branch extends the event sequence by `num_steps` steps (via calls
  to `generate_step_fn`). The resulting beam is returned.

  Args:
    beam_entries: A list of BeamEntry tuples, the current beam.
    generate_step_fn: A function that takes three parameters: a list of
        sequences, a list of states, and a list of scores, all of the same size.
        The function should generate a single step for each of the sequences and
        return the extended sequences, updated states, and updated (total)
        scores, as three lists. The function may modify the sequences, states,
        and scores in place, but should also return the modified values.
    branch_factor: The integer branch factor to use.
    num_steps: The integer number of steps to take per branch.

  Returns:
    The updated beam, with `branch_factor` timmes as many BeamEntry tuples.
    """
    if branch_factor > 1:
    	branched_entries = beam_entries * branch_factor
    	all_sequences = [copy.deepcopy(entry.sequence)
    						for entry in branched _entries]
    	all_states = [copy.deepcopy(entry.state) for entry in branched_entries]
    	all_scores = [entry.score for entry in branched_entries]
    else:
    	# No need to make copies if there is no branching 
    	all_sequences = [entry.sequence for entry in beam_entries]
    	all_states = [entry.state for entry in beam_entries]
    	all_scores = [entry.score for entry in beam_entries]

    for _ in range(num_steps):
    	all_sequences, all_states, all_scores = generate_step_fn(all_sequences, all_scores, all_states)

    return [BeamEntry(sequence, state, score)
    			for sequence, score, state
    			in zip(all_sequences, all_states, all_scores)]		  	

def _prune_branches(beam_entries, k):
	""" Prune all but k sequence with the highest score from the Beam."""
		indices = heapq.nlargest(k, range(len(beam_entries)), 
								  key=lambda i: beam_entries[i].score)
		return [beam_entries[i] for i in indices]

def beam_search(initial_sequence, initial_state, generate, generate_step_fn, num_steps,
				beam_size, branch_factor, step_per_iteration):
	"""Generates a sequence using beam search.

	Initially, the beam is filled with  'beam_size' copies of the initial sequence.

	Each iteration, the beam is pruned to contain only the 'beam_size' event 
	sequence with the highest score. Then 'branch_factor' new event sequences are 
	generated for each sequence in the beam. These new sequences are formed by 
	extending each sequence in the beam by the 'steps_per_iteration' steps. So between
	branching and a pruning phase, there will be 'beam_size' * 'branch_factor' active event
	sequences.

	After the final iteration, the single sequence inthe beam with highest likelihood will be 
	returned.

	The 'generated_step_fn' function operates on the list of sequences + states + scores 
	rather than single sequences. This is to allow for the possibility of batching.

	Args:
		initial_sequence: The initial sequence, a python list-like object.
		initial_state: The state corresponding to the initial sequence, with any auxiliary 
				information needed for extending the sequence.
		generated_step_fn: A function that takes three parameters: a list of sequences, 
				a list of states, a list of scores, all of them of same size.
				The function should generate a single step for each of the sequences and
				return the extended sequences, updated states, and updated (total) scores, as three lists.
		num_steps: The integer length in steps of the final sequence, after generation.
		beam_size: The integer beam size to use.
		branch_factor: The integer branch factor to use.
		steps_per_iteration: The integer number of steps to take per iteration.

	Returns:
		A tuple containg a) the highest-scoring sequence as computed by the beam search,
		b) the state corresponding to this sequence, and c) the score of this sequence.
		"""

	sequences = [copy.deepcopy(initial_sequence) for _ in range(beam_size)]
	states = [copy.deepcopy(initial_state) for _ in range(beam_size)]
	scores = [0] * beam_size
	



















