
import time
import json
import os
import uuid
import errno
import subprocess
import sys
import zipfile
from Bio import SeqIO

from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from MetagenomeUtils.MetagenomeUtilsClient import MetagenomeUtils


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
        for p in ['assembly_ref', 'binned_contig_name', 'workspace_name', 'reads_list']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

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

    def _stage_reads_list_file(self, reads_list):
        """
        _stage_reads_list_file: download fastq file associated to reads to scratch area
                          and write result_file_path to file
        """

        log('Processing reads object list: {}'.format(reads_list))

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)
        result_file = os.path.join(result_directory, 'reads_list_file.txt')

        result_file_path = []

        reads = self.ru.download_reads({'read_libraries': reads_list,
                                        'interleaved': 'true'})['files']

        for read_obj in reads_list:
            files = reads[read_obj]['files']
            result_file_path.append(files['fwd'])
            if 'rev' in files and files['rev'] is not None:
                result_file_path.append(files['rev'])

        log('Saving reads file path(s) to: {}'.format(result_file))
        with open(result_file, 'w') as file_handler:
            for item in result_file_path:
                file_handler.write("{}\n".format(item))

        return result_file

    def _get_contig_file(self, assembly_ref):
        """
        _get_contig_file: get contif file from GenomeAssembly object
        """

        contig_file = self.au.get_assembly_as_fasta({'ref': assembly_ref}).get('path')

        sys.stdout.flush()
        contig_file = self.dfu.unpack_file({'file_path': contig_file})['file_path']

        return contig_file

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

    def _generate_output_file_list(self, result_directory):
        """
        _generate_output_file_list: zip result files and generate file_links for report
        """
        log('Start packing result files')
        output_files = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file = os.path.join(output_directory, 'maxbin_result.zip')
        report_file = None

        with zipfile.ZipFile(result_file, 'w',
                             zipfile.ZIP_DEFLATED,
                             allowZip64=True) as zip_file:
            for root, dirs, files in os.walk(result_directory):
                for file in files:
                    if not (file.endswith('.fasta') or file.endswith('.DS_Store')):
                        zip_file.write(os.path.join(root, file), file)
                    if file.endswith('.marker.pdf'):
                        report_file = os.path.join(root, file)

        output_files.append({'path': result_file,
                             'name': os.path.basename(result_file),
                             'label': os.path.basename(result_file),
                             'description': 'File(s) generated by MaxBin2 App'})

        if report_file:
            output_files.append({'path': report_file,
                                 'name': os.path.basename(report_file),
                                 'label': os.path.basename(report_file),
                                 'description': 'Visualization of the marker by MaxBin2 App'})

        return output_files

    def _generate_html_report(self, result_directory, assembly_ref, binned_contig_obj_ref, header):
        """
        _generate_html_report: generate html summary report
        """

        log('Start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'report.html')

        Overview_Content = ''

        (binned_contig_count, input_contig_count,
         too_short_count, total_bins_count, total_binned_contig_len,
         totoal_contig_length, total_short_contig_len) = self._generate_overview_info(
                                                            assembly_ref,
                                                            binned_contig_obj_ref,
                                                            result_directory)
        Overview_Content += '<p>Bins: {}</p>'.format(total_bins_count)
        Overview_Content += '<p>Input Contigs: {}</p>'.format(input_contig_count)
        Overview_Content += '<p>Binned Contigs: {} ({:.1%})</p>'.format(
                                            binned_contig_count,
                                            binned_contig_count/float(input_contig_count))
        Overview_Content += '<p>Unbinned Contigs: {} ({:.1%})</p>'.format(
                                            input_contig_count - binned_contig_count,
                                            1 - binned_contig_count/float(input_contig_count))
        Overview_Content += '<p>Contigs Too Short: {} ({:.1%})</p>'.format(
                                            too_short_count,
                                            too_short_count/float(input_contig_count))
        Overview_Content += '<p>Summed Length of Binned Contigs: {} ({:.1%})</p>'.format(
                                            total_binned_contig_len,
                                            total_binned_contig_len/float(totoal_contig_length))
        Overview_Content += '<p>Summed Length of Unbinned Contigs: {} ({:.1%})</p>'.format(
                                            totoal_contig_length - total_binned_contig_len,
                                            1 - total_binned_contig_len/float(totoal_contig_length))
        Overview_Content += '<p>Summed Length of Short Contigs: {} ({:.1%})</p>'.format(
                                            total_short_contig_len,
                                            total_short_contig_len/float(totoal_contig_length))

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>Overview_Content</p>',
                                                          Overview_Content)
                result_file.write(report_template)

        html_report.append({'path': result_file_path,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for MaxBin2 App'})
        return html_report

    def _generate_overview_info(self, assembly_ref, binned_contig_obj_ref, result_directory):
        """
        _generate_overview_info: generate overview information from assembly and binnedcontig
        """

        assembly = self.dfu.get_objects({'object_refs': [assembly_ref]})['data'][0]
        binned_contig = self.dfu.get_objects({'object_refs': [binned_contig_obj_ref]})['data'][0]

        input_contig_count = assembly.get('data').get('num_contigs')

        totoal_contig_length = 0
        for contig_id, contig in assembly.get('data').get('contigs').items():
            totoal_contig_length += int(contig.get('length'))

        binned_contig_count = 0
        total_bins = binned_contig.get('data').get('bins')
        total_binned_contig_len = binned_contig.get('data').get('total_contig_len')
        total_bins_count = len(total_bins)
        for bin in total_bins:
            binned_contig_count += len(bin.get('contigs'))

        too_short_count = 0
        total_short_contig_len = 0
        result_files = os.listdir(result_directory)
        for file_name in result_files:
            if file_name.endswith('.tooshort'):
                for record in SeqIO.parse(os.path.join(result_directory, file_name), "fasta"):
                    total_short_contig_len += len(str(record.seq))
                    too_short_count += 1

        return (binned_contig_count, input_contig_count,
                too_short_count, total_bins_count, total_binned_contig_len,
                totoal_contig_length, total_short_contig_len)

    def _generate_report(self, binned_contig_obj_ref, result_directory, params):
        """
        generate_report: generate summary report

        """
        log('Generating report')

        output_files = self._generate_output_file_list(result_directory)

        output_html_files = self._generate_html_report(result_directory,
                                                       params.get('assembly_ref'),
                                                       binned_contig_obj_ref,
                                                       params.get('out_header'))

        created_objects = []
        created_objects.append({"ref": binned_contig_obj_ref,
                                "description": "BinnedContigs from MaxBin2"})

        report_params = {
              'message': '',
              'workspace_name': params.get('workspace_name'),
              'objects_created': created_objects,
              'file_links': output_files,
              'html_links': output_html_files,
              'direct_html_link_index': 0,
              'html_window_height': 266,
              'report_object_name': 'kb_maxbin_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)
        self.ru = ReadsUtils(self.callback_url)
        self.au = AssemblyUtil(self.callback_url)
        self.mgu = MetagenomeUtils(self.callback_url)

    def run_maxbin(self, params):
        """
        run_maxbin: run_MaxBin.pl app

        required params:
            assembly_ref: Metagenome assembly object reference
            binned_contig_name: BinnedContig object name and output file header
            workspace_name: the name of the workspace it gets saved to.
            reads_list: list of reads object (PairedEndLibrary/SingleEndLibrary)
                        upon which MaxBin will be run

        optional params:
            thread: number of threads; default 1
            reassembly: specify this option if you want to reassemble the bins.
                        note that at least one reads file needs to be designated.
            prob_threshold: minimum probability for EM algorithm; default 0.8
            markerset: choose between 107 marker genes by default or 40 marker genes
            min_contig_length: minimum contig length; default 1000
            plotmarker: specify this option if you want to plot the markers in each contig

        ref: http://downloads.jbei.org/data/microbial_communities/MaxBin/README.txt
        """
        log('--->\nrunning MaxBinUtil.run_maxbin\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_maxbin_params(params)
        params['out_header'] = 'Bin'

        contig_file = self._get_contig_file(params.get('assembly_ref'))
        params['contig_file_path'] = contig_file

        reads_list_file = self._stage_reads_list_file(params.get('reads_list'))
        params['reads_list_file'] = reads_list_file

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)

        command = self._generate_command(params)

        cwd = os.getcwd()
        log('changing working dir to {}'.format(result_directory))
        os.chdir(result_directory)
        self._run_command(command)
        os.chdir(cwd)
        log('changing working dir to {}'.format(cwd))

        log('Saved result files to: {}'.format(result_directory))
        log('Generated files:\n{}'.format('\n'.join(os.listdir(result_directory))))

        generate_binned_contig_param = {
            'file_directory': result_directory,
            'assembly_ref': params.get('assembly_ref'),
            'binned_contig_name': params.get('binned_contig_name'),
            'workspace_name': params.get('workspace_name')
        }
        binned_contig_obj_ref = self.mgu.file_to_binned_contigs(
                                    generate_binned_contig_param).get('binned_contig_obj_ref')

        reportVal = self._generate_report(binned_contig_obj_ref, result_directory, params)

        returnVal = {
            'result_directory': result_directory,
            'binned_contig_obj_ref': binned_contig_obj_ref
        }

        returnVal.update(reportVal)

        return returnVal
