# -*- coding: utf-8 -*-

import data
import logging
from galaxy.datatypes.sniff import *
import commands

log = logging.getLogger(__name__)


class GenericMolFile(data.Text):
    file_ext = "mol2/pdb/pdbqt"

    def check_filetype(self, filename):
        self.no_mols = commands.getstatusoutput("grep -c @\<TRIPOS\>MOLECULE "+filename)
        if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
            self.file_ext = "mol2"
            return True
        self.no_mols = commands.getstatusoutput("grep -c HEADER "+filename)
        if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
            self.file_ext = "pdb"
            return True
        self.no_mols = commands.getstatusoutput("grep -c COMPND "+filename)
        if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
            self.file_ext = "pdbqt"
            return True
        return False

    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            if(self.check_filetype(dataset.file_name)):
                if (self.no_mols[1] == '1'):
                    dataset.blurb = "1 molecule"
                else:
                    dataset.blurb = "%s molecules" % self.no_mols[1]
            dataset.peek = data.get_file_peek(dataset.file_name, is_multi_byte=is_multi_byte)
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def get_mime(self):
        return 'text/plain'


class GenericMultiMolFile(GenericMolFile):
    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            self.sniff(dataset.file_name)
            if (self.no_mols[1] == '1'):
                dataset.blurb = "1 molecule"
            else:
                dataset.blurb = "%s molecules" % self.no_mols[1]
            dataset.peek = data.get_file_peek(dataset.file_name, is_multi_byte=is_multi_byte)
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'


class MOL2(GenericMultiMolFile):
    file_ext = "mol2"

    def sniff(self, filename):
        self.no_mols = commands.getstatusoutput("grep -c @\<TRIPOS\>MOLECULE "+filename)
        if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
            return True
        else:
            return False

    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            self.sniff(dataset.file_name)
            dataset.blurb = "compound structure file used by autodock vina"
        else:
            dataset.peek = "file does not exist"
            dataset.blurb = "file purged from disk"


class PDBQT(GenericMolFile):
    file_ext = "pdbqt"

    def sniff(self, filename):
        self.no_mols = commands.getstatusoutput("grep -c COMPND "+filename)
        if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
            return True
        else:
            self.no_mols = commands.getstatusoutput("grep -c REMARK "+filename)
            if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
                return True
            else:
                self.no_mols = commands.getstatusoutput("grep -c ATOM "+filename)
                if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
                    return True

    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            self.sniff(dataset.file_name)
            dataset.blurb = "protein structure file used by autodock vina"
        else:
            dataset.peek = "file does not exist"
            dataset.blurb = "file purged from disk"

class PDB(GenericMolFile):
    file_ext = "pdb"

    def sniff(self, filename):
        self.no_mols = commands.getstatusoutput("grep -c HEADER "+filename)
        if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
            return True
        else:
            self.no_mols = commands.getstatusoutput("grep -c ATOM "+filename)
            if (self.no_mols[0] == 0) & (self.no_mols[1] > 0):
                return True
            else:
                return False

    def set_peek(self, dataset, is_multi_byte=False):

        if not dataset.dataset.purged:
            self.sniff(dataset.file_name)
            dataset.blurb = "protein structure file"
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'