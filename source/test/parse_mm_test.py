#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from lxml import etree
from os import path
from parse_mm import MechonMamreParser
from torah_model import Perek, TextFragment, Sefer


class MechonMamreParserTest(unittest.TestCase):

	def test_parse_sefer_filename(self):
		parser = MechonMamreParser()
		sefer = parser.parse_sefer_filename('../data/mamre.cantillation/c01.htm')

		for perek in sefer.iter_stream:
			self.assertEquals(Perek, type(perek))

		n_perakim = len(sefer.stream)
		expected_perakim = 50  # Bereshit has 50
		self.assertEquals(expected_perakim, n_perakim)

		# For a particular perek, check it has the right
		# number of psukim - same as number of TextFragments
		# except in very strange cases where psukim are broken
		# with a petuha/setumah which does not happen in Bereshit.
		random_perek = 13     # index 13 is perek 14
		expected_psukim = 24  # has 24 psukim
		actual_psukim = 0
		perek = sefer.stream[random_perek]
		for elt in perek.iter_stream:
			if type(elt) == TextFragment:
				actual_psukim += 1
		self.assertEquals(expected_psukim, actual_psukim)

	def test_parse_torah_filename(self):
		parser = MechonMamreParser()
		base_fname = '../data/mamre.cantillation/'
		fnames = ['c0%d.htm' % i for i in range(1, 6)]
		fnames = [path.join(base_fname, fname) for fname in fnames]
		torah = parser.parse_torah_filenames(fnames)

		for sefer in torah.iter_stream:
			self.assertEquals(Sefer, type(sefer))
			for perek in sefer.iter_stream:
				self.assertEquals(Perek, type(perek))

		n_sefarim = len(torah.stream)
		expected_sefarim = 5
		self.assertEquals(expected_sefarim, n_sefarim)

		vayikra = torah.stream[2]
		perek17 = vayikra.stream[16]
		expected_psukim = 16  # has 16 psukim
		actual_psukim = 0
		for elt in perek17.iter_stream:
			if type(elt) == TextFragment:
				actual_psukim += 1
		self.assertEquals(expected_psukim, actual_psukim)

	def test_make_xml(self):
		parser = MechonMamreParser()
		sefer = parser.parse_sefer_filename('../data/mamre.cantillation/c01.htm')

		root = etree.Element('root')
		sefer.add_to_xml_tree(root)

		with open('tmp.xml', 'w') as f:
			f.write(etree.tostring(root, pretty_print=True, encoding='utf-8'))
			print 'wrote to tmp.xml'


if __name__ == '__main__':
	unittest.main()