
import time
import json
import os
import uuid
import errno
import subprocess
import shutil
import sys
import re

from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class MaxBinUtil:
    MAXBIN_TOOLKIT_PATH = '/kb/deployment/bin/MaxBin'

    def _validate_run_maxbin_params(self, params):
        """
        _validate_run_maxbin_params:
                validates params passed to run_maxbin method

        """
        log('Start validating run_maxbin params')

        # check for required parameters
        for p in ['contig_file', 'out_header', 'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        contig_file = params.get('contig_file')
        if not isinstance(contig_file, dict):
            error_msg = 'contig_file is not type dict as required '
            error_msg += '[dict format: {path/shock_id: string}]'
            raise ValueError(error_msg)

        valid_file_keys = {'path', 'shock_id'}
        if not(set(contig_file.keys()) < valid_file_keys):
            raise ValueError('Please provide one and only one path/shock_id key')

        if not(params.get('abund_list') or params.get('reads_list')):
            raise ValueError('Please provide at least one abund_list or reads_list')

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _run_command(self, command):
        """
        _run_command: run command and print result
        """

        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            log('Executed commend:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running commend:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)

    def _stage_file(self, file):
        """
        _stage_file: download local file/ shock file to scratch area
        """

        log('Processing file: {}'.format(file))

        input_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(input_directory)

        if file.get('path'):
            # handle local file
            local_file_path = file['path']
            file_path = os.path.join(input_directory, os.path.basename(local_file_path))
            log('Moving file from {} to {}'.format(local_file_path, file_path))
            shutil.copy2(local_file_path, file_path)

        if file.get('shock_id'):
            # handle shock file
            log('Downloading file from SHOCK node: {}-{}'.format(self.shock_url,
                                                                 file['shock_id']))
            sys.stdout.flush()
            file_name = self.dfu.shock_to_file({'file_path': input_directory,
                                                'shock_id': file['shock_id']
                                                })['node_file_name']
            file_path = os.path.join(input_directory, file_name)

        sys.stdout.flush()
        file_path = self.dfu.unpack_file({'file_path': file_path})['file_path']

        return file_path

    def _stage_file_list(self, file_list):
        """
        _stage_file_list: download list of local file/ shock file to scratch area
                          and write result_file_path to file
        """

        log('Processing file list: {}'.format(file_list))

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)
        result_file = os.path.join(result_directory, 'result.txt')

        result_file_path = []

        if 'shock_id' in file_list:
            for file in file_list.get('shock_id'):
                file_path = self._stage_file({'shock_id': file})
                result_file_path.append(file_path)

        if 'path' in file_list:
            for file in file_list.get('path'):
                file_path = self._stage_file({'path': file})
                result_file_path.append(file_path)

        log('Saving file path(s) to: {}'.format(result_file))
        with open(result_file, 'w') as file_handler:
            for item in result_file_path:
                file_handler.write("{}\n".format(item))

        return result_file

    def _generate_command(self, params):
        """
        _generate_command: generate run_MaxBin.pl params
        """

        command = self.MAXBIN_TOOLKIT_PATH + '/run_MaxBin.pl '

        command += '-contig {} -out {} '.format(params.get('contig_file_path'),
                                                params.get('out_header'))

        if params.get('abund_list_file'):
            command += '-abund_list {} '.format(params.get('abund_list_file'))

        if params.get('reads_list_file'):
            command += '-reads_list {} '.format(params.get('reads_list_file'))

        if params.get('thread'):
            command += '-thread {} '.format(params.get('thread'))

        if params.get('prob_threshold'):
            command += '-prob_threshold {} '.format(params.get('prob_threshold'))

        if params.get('markerset'):
            command += '-markerset {} '.format(params.get('markerset'))

        if params.get('min_contig_length'):
            command += '-min_contig_length {} '.format(params.get('min_contig_length'))

        if params.get('plotmarker'):
            command += '-plotmarker '

        if params.get('reassembly'):
            command += '-reassembly '

        log('Generated run_MaxBin command: {}'.format(command))

        return command

    def _generate_report(self, result_directory, params):
        """
        generate_report: generate summary report

        """
        log('Generating report')

        uuid_string = str(uuid.uuid4())
        upload_message = 'Job Finished\n\n'

        file_list = os.listdir(result_directory)
        header = params.get('out_header')

        # upload_message += '--------------------------\nSummary:\n\n'
        # with open(os.path.join(result_directory, header + '.summary'), 'r') as summary_file:
        #     first_line = True
        #     lines = summary_file.readlines()
        #     for line in lines:
        #         if first_line:
        #             line_list = line.split('\t')
        #             upload_message += line_list[0] + 2 * '\t' + line_list[1] + '\t'
        #             upload_message += line_list[3] + '\t' + line_list[4]
        #             first_line = False
        #         else:
        #             line_list = line.split('\t')
        #             upload_message += line_list[0] + '\t' + line_list[1] + 2 * '\t'
        #             upload_message += line_list[3] + 2 * '\t' + line_list[4]

        # upload_message += '--------------------------\nOutput files for this run: \n\n'
        # if header + '.summary' in file_list:
        #     upload_message += 'Summary file: {}.summary\n'.format(header)
        #     file_list.remove(header + '.summary')

        # if header + '.marker' in file_list:
        #     upload_message += 'Marker counts: {}.marker\n'.format(header)
        #     file_list.remove(header + '.marker')

        # if header + '.marker_of_each_bin.tar.gz' in file_list:
        #     upload_message += 'Marker genes for each bin: '
        #     upload_message += '{}.marker_of_each_bin.tar.gz\n'.format(header)
        #     file_list.remove(header + '.marker_of_each_bin.tar.gz')

        # if header + '.001.fasta' in file_list:
        #     upload_message += 'Bin files: '
        #     bin_file = []
        #     for file_name in file_list:
        #         if re.match(header + '\.\d{3}\.fasta', file_name):
        #             bin_file.append(file_name)

        #     bin_file.sort()
        #     upload_message += '{} - {}\n'.format(bin_file[0], bin_file[-1])
        #     file_list = [item for item in file_list if item not in bin_file]

        # if header + '.noclass' in file_list:
        #     upload_message += 'Unbinned sequences: {}.noclass\n'.format(header)
        #     file_list.remove(header + '.noclass')

        # if header + '.tooshort' in file_list:
        #     upload_message += 'Short sequences: {}.tooshort\n'.format(header)
        #     file_list.remove(header + '.tooshort')

        # if header + '.log' in file_list:
        #     upload_message += 'Log file: {}.log\n'.format(header)
        #     file_list.remove(header + '.log')

        # if header + '.marker.pdf' in file_list:
        #     upload_message += 'Visualization file: {}.marker.pdf\n'.format(header)
        #     file_list.remove(header + '.marker.pdf')

        # if file_list:
        #     upload_message += 'Other files:\n{}'.format('\n'.join(file_list))

        log('Report message:\n{}'.format(upload_message))

        report_params = {
              'message': upload_message,
              'workspace_name': params.get('workspace_name'),
              'report_object_name': 'kb_maxbin_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = config['scratch']
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)

    def run_maxbin(self, params):
        """
        run_maxbin: run_MaxBin.pl app

        required params:
            contig_file: contig file path/shock_id in File structure
            out_header: output file header
            workspace_name: the name of the workspace it gets saved to.

        semi-required: at least one of the following parameters is needed
            abund_list: contig abundance file(s)/shock_id(s)
            reads_list: reads file(s)/shock_id(s) in fasta or fastq format

        optional params:
            thread: number of threads; default 1
            reassembly: specify this option if you want to reassemble the bins.
                        note that at least one reads file needs to be designated.
            prob_threshold: minimum probability for EM algorithm; default 0.8
            markerset: choose between 107 marker genes by default or 40 marker genes

        ref: http://downloads.jbei.org/data/microbial_communities/MaxBin/README.txt
        """
        log('--->\nrunning MaxBinUtil.run_maxbin\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_maxbin_params(params)

        contig_file = self._stage_file(params.get('contig_file'))
        params['contig_file_path'] = contig_file

        if params.get('abund_list'):
            abund_list_file = self._stage_file_list(params.get('abund_list'))
            params['abund_list_file'] = abund_list_file

        if params.get('reads_list'):
            reads_list_file = self._stage_file_list(params.get('reads_list'))
            params['reads_list_file'] = reads_list_file

        command = self._generate_command(params)

        existing_files = []
        for subdir, dirs, files in os.walk('./'):
            for file in files:
                existing_files.append(file)

        self._run_command(command)

        new_files = []
        for subdir, dirs, files in os.walk('./'):
            for file in files:
                if file not in existing_files:
                    new_files.append(file)

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)

        for file in new_files:
            shutil.copy(file, result_directory)

        log('Saved result files to: {}'.format(result_directory))
        log('Gernated files:\n{}'.format('\n'.join(os.listdir(result_directory))))

        reportVal = self._generate_report(result_directory, params)

        returnVal = {
            'result_directory': result_directory,
            'obj_ref': 'obj_ref'
        }

        returnVal.update(reportVal)

        return returnVal
