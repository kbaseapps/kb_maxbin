# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import shutil
import zipfile

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_maxbin.kb_maxbinImpl import kb_maxbin
from kb_maxbin.kb_maxbinServer import MethodContext
from kb_maxbin.authclient import KBaseAuth as _KBaseAuth
from kb_maxbin.Utils.MaxBinUtil import MaxBinUtil
from DataFileUtil.DataFileUtilClient import DataFileUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil


class kb_maxbinTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_maxbin'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(cls.token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': cls.token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_maxbin',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_maxbin(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        wsName = "test_kb_maxbin_" + str(suffix)
        cls.ws_info = cls.wsClient.create_workspace({'workspace': wsName})
        cls.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=cls.token)
        cls.ru = ReadsUtils(os.environ['SDK_CALLBACK_URL'], token=cls.token)
        cls.au = AssemblyUtil(os.environ['SDK_CALLBACK_URL'], token=cls.token)
        cls.maxbin_runner = MaxBinUtil(cls.cfg)
        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def prepare_data(cls):
        # building SingleEndLibrary
        se_reads_filename = 'Sample1.fastq'
        se_reads_path = os.path.join(cls.scratch, se_reads_filename)
        shutil.copy(os.path.join("data", "reads_file", se_reads_filename), se_reads_path)
        se_reads_params = {
            'fwd_file': se_reads_path,
            'sequencing_tech': 'Unknown',
            'wsname': cls.ws_info[1],
            'name': 'MySingleEndLibrary'
        }
        cls.se_reads_ref = cls.ru.upload_reads(se_reads_params)['obj_ref']

        # building PairedEndLibrary
        fwd_reads_filename = 'small.forward.fq'
        fwd_reads_path = os.path.join(cls.scratch, fwd_reads_filename)
        shutil.copy(os.path.join("data", "reads_file", fwd_reads_filename), fwd_reads_path)

        rev_reads_filename = 'small.reverse.fq'
        rev_reads_path = os.path.join(cls.scratch, rev_reads_filename)
        shutil.copy(os.path.join("data", "reads_file", rev_reads_filename), rev_reads_path)
        pe_reads_params = {
            'fwd_file': fwd_reads_path,
            'rev_file': rev_reads_path,
            'sequencing_tech': 'Unknown',
            'wsname': cls.ws_info[1],
            'name': 'MyPairedEndLibrary'
        }
        cls.pe_reads_ref = cls.ru.upload_reads(pe_reads_params)['obj_ref']

        # building Assembly
        assembly_filename = '20x.fna'
        cls.assembly_fasta_file_path = os.path.join(cls.scratch, assembly_filename)
        shutil.copy(os.path.join("data", assembly_filename), cls.assembly_fasta_file_path)

        assembly_params = {
            'file': {'path': cls.assembly_fasta_file_path},
            'workspace_name': cls.ws_info[1],
            'assembly_name': 'MyAssembly'
        }
        cls.assembly_ref = cls.au.save_assembly_from_fasta(assembly_params)

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.ws_info[1]

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_bad_run_maxbin_params(self):
        invalidate_input_params = {
          'missing_assembly_ref': 'assembly_ref',
          'binned_contig_name': 'binned_contig_name',
          'workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"assembly_ref" parameter is required, but missing'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'assembly_ref': 'assembly_ref',
          'missing_binned_contig_name': 'binned_contig_name',
          'workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"binned_contig_name" parameter is required, but missing'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'assembly_ref': 'assembly_ref',
          'binned_contig_name': 'binned_contig_name',
          'missing_workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"workspace_name" parameter is required, but missing'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'assembly_ref': 'assembly_ref',
          'binned_contig_name': 'binned_contig_name',
          'workspace_name': 'workspace_name',
          'missing_reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"reads_list" parameter is required, but missing'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

    def test_MaxBinUtil_stage_file(self):

        contig_filename = '20x.scaffold.gz'
        contig_path = os.path.join(self.scratch, contig_filename)
        shutil.copy(os.path.join("data", "jbei_set1", contig_filename), contig_path)

        # test absolute file path
        contig_file = {'path': contig_path}

        contig_file_path = self.maxbin_runner._stage_file(contig_file)

        self.assertEquals(contig_filename.rpartition('.')[0], os.path.basename(contig_file_path))

        # test shock id
        contig_shock_id = self.dfu.file_to_shock({'file_path': contig_path})['shock_id']
        contig_file = {'shock_id': contig_shock_id}

        contig_file_path = self.maxbin_runner._stage_file(contig_file)

        self.assertEquals(contig_filename.rpartition('.')[0], os.path.basename(contig_file_path))

    def test_MaxBinUtil_generate_command(self):
        input_params = {
            'contig_file_path': 'mycontig',
            'out_header': 'myout',
            'abund_list_file': 'abund_list_file'
        }

        expect_command = '/kb/deployment/bin/MaxBin/run_MaxBin.pl '
        expect_command += '-contig mycontig -out myout -abund_list abund_list_file '
        command = self.maxbin_runner._generate_command(input_params)
        self.assertEquals(command, expect_command)

        input_params = {
            'contig_file_path': 'mycontig',
            'out_header': 'myout',
            'reads_list_file': 'reads_list_file'
        }

        expect_command = '/kb/deployment/bin/MaxBin/run_MaxBin.pl '
        expect_command += '-contig mycontig -out myout -reads_list reads_list_file '
        command = self.maxbin_runner._generate_command(input_params)
        self.assertEquals(command, expect_command)

        input_params = {
            'contig_file_path': 'mycontig',
            'out_header': 'myout',
            'reads_list_file': 'reads_list_file',
            'abund_list_file': 'abund_list_file'
        }

        expect_command = '/kb/deployment/bin/MaxBin/run_MaxBin.pl '
        expect_command += '-contig mycontig -out myout '
        expect_command += '-abund_list abund_list_file -reads_list reads_list_file '
        command = self.maxbin_runner._generate_command(input_params)
        self.assertEquals(command, expect_command)

        input_params = {
            'contig_file_path': 'mycontig',
            'out_header': 'myout',
            'reads_list_file': 'reads_list_file',
            'abund_list_file': 'abund_list_file',
            'thread': 4,
            'prob_threshold': 0.5,
            'markerset': 40,
            'reassembly': 1,
            'min_contig_length': 600,
            'plotmarker': 1
        }

        expect_command = '/kb/deployment/bin/MaxBin/run_MaxBin.pl '
        expect_command += '-contig mycontig -out myout '
        expect_command += '-abund_list abund_list_file -reads_list reads_list_file '
        expect_command += '-thread 4 -prob_threshold 0.5 -markerset 40 '
        expect_command += '-min_contig_length 600 -plotmarker -reassembly '
        command = self.maxbin_runner._generate_command(input_params)
        self.assertEquals(command, expect_command)

    def test_MaxBinUtil_generate_output_file_list(self):

        result_file_file_directory = 'MaxBin_result'
        result_file_path = os.path.join(self.scratch, result_file_file_directory)
        if not os.path.exists(result_file_path):
            os.makedirs(result_file_path)

        for item in os.listdir(os.path.join("data", "MaxBin_Result_Sample")):
            shutil.copy(os.path.join("data", "MaxBin_Result_Sample", item),
                        os.path.join(result_file_path, item))

        output_file = self.maxbin_runner._generate_output_file_list(result_file_path)[0]

        self.assertTrue('path' in output_file)
        output_file_path = output_file.get('path')
        expect_file_set = set(['out_header.abund1',
                               'out_header.abund2',
                               'out_header.abund3',
                               'out_header.marker',
                               'out_header.marker_of_each_bin.tar.gz',
                               'out_header.summary',
                               'out_header.noclass',
                               'out_header.log',
                               'out_header.abundance',
                               'out_header.tooshort'])

        with zipfile.ZipFile(output_file_path) as z:
            self.assertEqual(set(z.namelist()), expect_file_set)

        self.assertEquals(output_file.get('description'), 'File(s) generated by MaxBin2 App')
        self.assertEquals(output_file.get('name'), 'maxbin_result.zip')
        self.assertEquals(output_file.get('label'), 'maxbin_result.zip')

    def test_MaxBinUtil_stage_reads_list_file(self):
        # test SingleEndLibrary
        reads_list = [self.se_reads_ref, self.se_reads_ref]

        reads_list_file = self.maxbin_runner._stage_reads_list_file(reads_list)

        with open(reads_list_file) as file:
            result_file_list = file.readlines()

        self.assertEquals(len(result_file_list), len(reads_list))
        for item in result_file_list:
            self.assertRegexpMatches(item, r'.*\.single\.fastq.*')

        # test PairedEndLibrary
        reads_list = [self.pe_reads_ref, self.pe_reads_ref]

        reads_list_file = self.maxbin_runner._stage_reads_list_file(reads_list)

        with open(reads_list_file) as file:
            result_file_list = file.readlines()

        self.assertEquals(len(result_file_list), len(reads_list))
        for item in result_file_list:
            self.assertRegexpMatches(item, r'.*\.inter\.fastq.*')

    def test_MaxBinUtil_get_contig_file(self):
        contig_file = self.maxbin_runner._get_contig_file(self.assembly_ref)

        with open(contig_file, 'r') as file:
            contig_file_content = file.readlines()

        with open(self.assembly_fasta_file_path, 'r') as file:
            expect_contig_file_content = file.readlines()

        self.assertItemsEqual(contig_file_content, expect_contig_file_content)

    def test_run_maxbin_single_reads(self):

        input_params = {
            'assembly_ref': self.assembly_ref,
            'binned_contig_name': 'out_header',
            'workspace_name': self.getWsName(),
            'reads_list': [self.pe_reads_ref],
            'thread': 1,
            'prob_threshold': 0.5,
            'markerset': 170,
            'min_contig_length': 2000,
            'plotmarker': 1
        }

        result = self.getImpl().run_max_bin(self.getContext(), input_params)[0]

        self.assertTrue('result_directory' in result)
        self.assertTrue('binned_contig_obj_ref' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)

    def test_run_maxbin_multi_reads(self):

        input_params = {
            'assembly_ref': self.assembly_ref,
            'binned_contig_name': 'out_header',
            'workspace_name': self.getWsName(),
            'reads_list': [self.pe_reads_ref, self.pe_reads_ref, self.se_reads_ref],
            'thread': 4,
            'prob_threshold': 0.7,
            'markerset': 40,
            'min_contig_length': 1500,
            'plotmarker': 1
        }

        result = self.getImpl().run_max_bin(self.getContext(), input_params)[0]

        self.assertTrue('result_directory' in result)
        self.assertTrue('binned_contig_obj_ref' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)
