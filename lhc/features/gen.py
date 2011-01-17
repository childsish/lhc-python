#!/usr/bin/python

import numpy

from sequence.rna_tools import RNAFolder
from sequence.seq_tools import kContent
from sequence.MFEGenerator import MFEGenerator

FOLDER = RNAFolder(p=True)
MFE = MFEGenerator('mfe')
EFE = MFEGenerator('efe')

def calcFtrs(seq):
	ftrs = []
	
	stc, mfe, efe, cstc, cmfe, cdst, frq, div, bpp = FOLDER.fold(seq)
	
	kmer = kContent(seq, 1)
	atcg = (kmer['a'] + kmer['t']) / (kmer['a'] + kmer['t'] + kmer['c'] + kmer['g'])
	if kmer['a'] + kmer['t'] == 0:
		at = 0
	else:
		at = kmer['a'] / (kmer['a'] + kmer['t'])
	if kmer['c'] + kmer['g'] == 0:
		cg = 0
	else:
		cg = kmer['c'] / (kmer['c'] + kmer['g'])
	
	mfe_avg, mfe_std = MFE.generate(len(seq), atcg, at, cg)
	efe_avg, efe_std = EFE.generate(len(seq), atcg, at, cg)
	
	ftrs.append(mfe - mfe_avg)
	ftrs.append((mfe - mfe_avg) / mfe_std)
	ftrs.append(efe - efe_avg)
	ftrs.append((efe - efe_avg) / efe_std)
	
	return numpy.array(ftrs)

def nameFtrs():
	ftrs = []
	ftrs.append('Generated MFE')
	ftrs.append('Generated MFEz')
	ftrs.append('Generated EFE')
	ftrs.append('Generated EFEz')
	return ftrs
