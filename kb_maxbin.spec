/*
A KBase module: kb_maxbin
*/

module kb_maxbin {

    /* A boolean - 0 for false, 1 for true.
        @range (0, 1)
    */
    typedef int boolean;

    /*
        File structure for input/output file
    */

    typedef structure {
        string path;
        string shock_id;
    } File;

    /*  
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
    */
    typedef structure {
        File contig_file;
        string out_header;
        string workspace_name;

        list<File> abund_list;
        list<File> reads_list;

        int thread;
        boolean reassembly;
        float prob_threshold;
        int markerset;
    } MaxBinInputParams;

    /*
        result_folder: folder path that holds all files generated by run_max_bin
        report_name: report name generated by KBaseReport
        report_ref: report reference generated by KBaseReport
    */
    typedef structure{
        string result_directory;
        string obj_ref;
        string report_name;
        string report_ref;
    }MaxBinResult;

    funcdef run_max_bin(MaxBinInputParams params)
        returns (MaxBinResult returnVal) authentication required;

};