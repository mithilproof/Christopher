""" Test for beam search."""

# Internal imports
import tensorflow as tf 

from magenta.common import beam_search

class BeamSearchTest(tf.test.TestCase):
	"""docstring for BeamSearchTest"""
	def _generate_step_fn(self, sequences, states, scores):
    # This acts as a binary counter for testing purposes. For scoring, zeros
    # accumulate value exponentially in the state, ones "cash in". The highest-
    # scoring sequence would be all zeros followed by a single one.
    	value = 0
    	for i in range(len(sequences)):
      		sequences[i].append(value)
      		if value == 0:
        		states[i] *= 2
      		else:
        		scores[i] += states[i]
        		states[i] = 1
      		if (i - 1) % (2 ** len(sequences[i])) == 0:
        		value = 1 - value
    	return sequences, states, scores

    def 		