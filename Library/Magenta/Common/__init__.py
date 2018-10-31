# Abstracted from Magenta. Original work credit, Google Inc.

# Copyright stemAI Open Source Labs. All Rights Reserved.

from __future__ import absolute_import

from . import state_util
from .beam_search import beam_search
from .nade import Nade 
from .sequence_example_lib import count_records
from .sequence_example_lib import flatten_maybe_padded_sequences
from .sequence_example_lib import get_padded_batch
from .sequence_example_lib import make_sequence_example
from .tf_utils import merge_hparams