# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import shutil

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
          'missing_contig_file': {'path': 'path'},
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"contig_file" parameter is required, but missing'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'path': 'path'},
          'missing_out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"out_header" parameter is required, but missing'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'path': 'path'},
          'out_header': 'out_header',
          'missing_workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"workspace_name" parameter is required, but missing'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'path': 'path'},
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'missing_reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"reads_list" parameter is required, but missing'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': 'not a dict',
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'abund_list': 'abund_list',
          'reads_list': 'reads_list'
        }
        error_msg = 'contig_file is not type dict as required '
        error_msg += '\[dict format: \{path/shock_id: string\}\]'
        with self.assertRaisesRegexp(ValueError, error_msg):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'path': 'path', 'shock_id': 'shock_id'},
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'abund_list': 'abund_list',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, 'Please provide one and only one path/shock_id key'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'missing_path': 'path'},
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'abund_list': 'abund_list',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, 'Please provide one and only one path/shock_id key'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'missing_shock_id': 'shock_id'},
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, 'Please provide one and only one path/shock_id key'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'path': 'path', 'invalid_shock_id': 'shock_id'},
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, 'Please provide one and only one path/shock_id key'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'invalid_path': 'path', 'invalid_shock_id': 'shock_id'},
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, 'Please provide one and only one path/shock_id key'):
            self.getImpl().run_max_bin(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'contig_file': {'invalid_path': 'path', 'invalid_shock_id': 'shock_id'},
          'out_header': 'out_header',
          'workspace_name': 'workspace_name',
          'reads_list': 'reads_list'
        }
        with self.assertRaisesRegexp(
                    ValueError, 'Please provide one and only one path/shock_id key'):
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

    def test_MaxBinUtil_stage_file_list(self):

        abund_filename = '20x.abund'
        abund_path = os.path.join(self.scratch, abund_filename)
        shutil.copy(os.path.join("data", "jbei_set1", abund_filename), abund_path)

        # test absolute file path
        abund_file_list = {
            'path': [abund_path, abund_path]
        }

        abund_list_file = self.maxbin_runner._stage_file_list(abund_file_list)

        with open(abund_list_file) as file:
            result_file_list = file.readlines()

        self.assertEquals(len(result_file_list), len(abund_file_list.get('path')))
        for item in result_file_list:
            file_path = item.partition('\n')[0]
            self.assertEquals(abund_filename, os.path.basename(file_path))

        # test shock id
        abund_shock_id = self.dfu.file_to_shock({'file_path': abund_path})['shock_id']
        abund_file_list = {
            'shock_id': [abund_shock_id, abund_shock_id]
        }

        abund_list_file = self.maxbin_runner._stage_file_list(abund_file_list)

        with open(abund_list_file) as file:
            result_file_list = file.readlines()

        self.assertEquals(len(result_file_list), len(abund_file_list.get('shock_id')))
        for item in result_file_list:
            file_path = item.partition('\n')[0]
            self.assertEquals(abund_filename, os.path.basename(file_path))

        # test mix absolute file path and shock id
        abund_file_list = {
            'shock_id': [abund_shock_id],
            'path': [abund_path]
        }

        abund_list_file = self.maxbin_runner._stage_file_list(abund_file_list)

        with open(abund_list_file) as file:
            result_file_list = file.readlines()

        self.assertEquals(len(result_file_list), len(abund_file_list.keys()))
        for item in result_file_list:
            file_path = item.partition('\n')[0]
            self.assertEquals(abund_filename, os.path.basename(file_path))

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

    def test_MaxBinUtil_stage_reads_list_file(self):
        # test SingleEndLibrary
        reads_list = [self.se_reads_ref, self.se_reads_ref]

        reads_list_file = self.maxbin_runner._stage_reads_list_file(reads_list)

        with open(reads_list_file) as file:
            result_file_list = file.readlines()

        self.assertEquals(len(result_file_list), len(reads_list))
        for item in result_file_list:
            self.assertRegexpMatches(item, r'.*\.single\.fastq.*')

        print result_file_list

        # test PairedEndLibrary
        reads_list = [self.pe_reads_ref, self.pe_reads_ref]

        reads_list_file = self.maxbin_runner._stage_reads_list_file(reads_list)

        with open(reads_list_file) as file:
            result_file_list = file.readlines()

        self.assertEquals(len(result_file_list), len(reads_list))
        for item in result_file_list:
            self.assertRegexpMatches(item, r'.*\.inter\.fastq.*')

        print result_file_list

    def test_run_maxbin_single_reads(self):

        contig_filename = '20x.scaffold.gz'
        contig_path = os.path.join(self.scratch, contig_filename)
        shutil.copy(os.path.join("data", "jbei_set1", contig_filename), contig_path)

        input_params = {
            'contig_file': {'path': contig_path},
            'out_header': 'out_header',
            'workspace_name': self.getWsName(),
            'reads_list': [self.pe_reads_ref],
            'thread': 4,
            'prob_threshold': 0.5,
            'markerset': 40,
            'min_contig_length': 2000,
            'plotmarker': 1
        }

        result = self.getImpl().run_max_bin(self.getContext(), input_params)[0]

        self.assertTrue('result_directory' in result)
        self.assertTrue('obj_ref' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)

        # expect_files = [
        #     'out_header.001.fasta',
        #     'out_header.002.fasta',
        #     'out_header.003.fasta',
        #     'out_header.log',
        #     'out_header.marker',
        #     'out_header.marker_of_each_bin.tar.gz',
        #     'out_header.noclass',
        #     'out_header.summary',
        #     'out_header.tooshort',
        #     'out_header.abund1']

        # self.assertItemsEqual(os.listdir(result.get('result_directory')), expect_files)

    def test_run_maxbin_multi_reads(self):

        contig_filename = '20x.scaffold.gz'
        contig_path = os.path.join(self.scratch, contig_filename)
        shutil.copy(os.path.join("data", "jbei_set1", contig_filename), contig_path)

        input_params = {
            'contig_file': {'path': contig_path},
            'out_header': 'out_header',
            'workspace_name': self.getWsName(),
            'reads_list': [self.pe_reads_ref, self.pe_reads_ref, self.se_reads_ref],
            'thread': 4,
            'prob_threshold': 0.5,
            'markerset': 40,
            'min_contig_length': 2000,
            'plotmarker': 1
        }

        result = self.getImpl().run_max_bin(self.getContext(), input_params)[0]

        self.assertTrue('result_directory' in result)
        self.assertTrue('obj_ref' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)

        expect_files = [
            'out_header.001.fasta',
            'out_header.002.fasta',
            'out_header.003.fasta',
            'out_header.abundance',
            'out_header.log',
            'out_header.marker',
            'out_header.marker_of_each_bin.tar.gz',
            'out_header.noclass',
            'out_header.summary',
            'out_header.tooshort',
            'out_header.abund1',
            'out_header.abund2',
            'out_header.abund3']

        self.assertItemsEqual(os.listdir(result.get('result_directory')), expect_files)
