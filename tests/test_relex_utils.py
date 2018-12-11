# -*- coding: utf-8 -*-
"""

Test relex snowball

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import io
import logging
import os
import unittest
import numpy as np

from chemdataextractor.relex.utils import mode_rows, match, KnuthMorrisPratt
from chemdataextractor.doc import Sentence
from chemdataextractor.relex import Relation, Entity, Phrase, Cluster
from chemdataextractor.parse.cem import chemical_name
from chemdataextractor.parse import R, merge

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

units = (R('^[CFK]\.?$'))('units').add_action(merge)
value = (R('^\d+(\.\,\d+)?$'))('value')

class TestRelexUtils(unittest.TestCase):
    maxDiff=None

    def test_mode_rows(self):
        a = np.array([[1,1,1,1],
                    [1,2,3,4],
                    [1,1,1,1],
                    [3,4,5,6]])
        expected = [1,1,1,1]
        result = list(mode_rows(a))
        self.assertListEqual(result, expected)
    
    def test_match(self):
        s1 = Sentence('BiFeO3 with 1103 K')
        entities = [Entity('BiFeO3', chemical_name, 0, 1), Entity('1103', value, 2,3), Entity('K', units, 2,3)]
        rel1 = [Relation(entities, 1.0)]
        phrase = Phrase(s1.raw_tokens, rel1, prefix_length=1, suffix_length=1)
        cluster = Cluster(label=0, order=phrase.order, learning_rate=0.5)
        cluster.add_phrase(phrase)
        similarity = match(phrase, phrase)
        expected = 1.0
        self.assertEqual(similarity, expected)
    
    def test_kmp(self):
        a = [1,2,3,4,5,6]
        test = [5,6]
        expected = [4]
        result = []
        for r in KnuthMorrisPratt(a, test):
            result.append(r)
        self.assertEqual(result, expected)

        
        
