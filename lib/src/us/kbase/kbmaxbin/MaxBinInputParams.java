
package us.kbase.kbmaxbin;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: MaxBinInputParams</p>
 * <pre>
 * required params:
 * contig_file: contig file path/shock_id in File structure
 * assembly_ref: Genome assembly object reference
 * out_header: output file header
 * workspace_name: the name of the workspace it gets saved to.
 * reads_list: list of reads object (PairedEndLibrary/SingleEndLibrary) upon which MaxBin will be run
 * optional params:
 * thread: number of threads; default 1
 * reassembly: specify this option if you want to reassemble the bins.
 *             note that at least one reads file needs to be designated.
 * prob_threshold: minimum probability for EM algorithm; default 0.8
 * markerset: choose between 107 marker genes by default or 40 marker genes
 * min_contig_length: minimum contig length; default 1000
 * plotmarker: specify this option if you want to plot the markers in each contig
 * ref: http://downloads.jbei.org/data/microbial_communities/MaxBin/README.txt
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "contig_file",
    "assembly_ref",
    "out_header",
    "workspace_name",
    "reads_list",
    "thread",
    "reassembly",
    "prob_threshold",
    "markerset",
    "min_contig_length",
    "plotmarker"
})
public class MaxBinInputParams {

    /**
     * <p>Original spec-file type: File</p>
     * <pre>
     * File structure for input/output file
     * </pre>
     * 
     */
    @JsonProperty("contig_file")
    private File contigFile;
    @JsonProperty("assembly_ref")
    private java.lang.String assemblyRef;
    @JsonProperty("out_header")
    private java.lang.String outHeader;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("reads_list")
    private List<String> readsList;
    @JsonProperty("thread")
    private Long thread;
    @JsonProperty("reassembly")
    private Long reassembly;
    @JsonProperty("prob_threshold")
    private Double probThreshold;
    @JsonProperty("markerset")
    private Long markerset;
    @JsonProperty("min_contig_length")
    private Long minContigLength;
    @JsonProperty("plotmarker")
    private Long plotmarker;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    /**
     * <p>Original spec-file type: File</p>
     * <pre>
     * File structure for input/output file
     * </pre>
     * 
     */
    @JsonProperty("contig_file")
    public File getContigFile() {
        return contigFile;
    }

    /**
     * <p>Original spec-file type: File</p>
     * <pre>
     * File structure for input/output file
     * </pre>
     * 
     */
    @JsonProperty("contig_file")
    public void setContigFile(File contigFile) {
        this.contigFile = contigFile;
    }

    public MaxBinInputParams withContigFile(File contigFile) {
        this.contigFile = contigFile;
        return this;
    }

    @JsonProperty("assembly_ref")
    public java.lang.String getAssemblyRef() {
        return assemblyRef;
    }

    @JsonProperty("assembly_ref")
    public void setAssemblyRef(java.lang.String assemblyRef) {
        this.assemblyRef = assemblyRef;
    }

    public MaxBinInputParams withAssemblyRef(java.lang.String assemblyRef) {
        this.assemblyRef = assemblyRef;
        return this;
    }

    @JsonProperty("out_header")
    public java.lang.String getOutHeader() {
        return outHeader;
    }

    @JsonProperty("out_header")
    public void setOutHeader(java.lang.String outHeader) {
        this.outHeader = outHeader;
    }

    public MaxBinInputParams withOutHeader(java.lang.String outHeader) {
        this.outHeader = outHeader;
        return this;
    }

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public MaxBinInputParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("reads_list")
    public List<String> getReadsList() {
        return readsList;
    }

    @JsonProperty("reads_list")
    public void setReadsList(List<String> readsList) {
        this.readsList = readsList;
    }

    public MaxBinInputParams withReadsList(List<String> readsList) {
        this.readsList = readsList;
        return this;
    }

    @JsonProperty("thread")
    public Long getThread() {
        return thread;
    }

    @JsonProperty("thread")
    public void setThread(Long thread) {
        this.thread = thread;
    }

    public MaxBinInputParams withThread(Long thread) {
        this.thread = thread;
        return this;
    }

    @JsonProperty("reassembly")
    public Long getReassembly() {
        return reassembly;
    }

    @JsonProperty("reassembly")
    public void setReassembly(Long reassembly) {
        this.reassembly = reassembly;
    }

    public MaxBinInputParams withReassembly(Long reassembly) {
        this.reassembly = reassembly;
        return this;
    }

    @JsonProperty("prob_threshold")
    public Double getProbThreshold() {
        return probThreshold;
    }

    @JsonProperty("prob_threshold")
    public void setProbThreshold(Double probThreshold) {
        this.probThreshold = probThreshold;
    }

    public MaxBinInputParams withProbThreshold(Double probThreshold) {
        this.probThreshold = probThreshold;
        return this;
    }

    @JsonProperty("markerset")
    public Long getMarkerset() {
        return markerset;
    }

    @JsonProperty("markerset")
    public void setMarkerset(Long markerset) {
        this.markerset = markerset;
    }

    public MaxBinInputParams withMarkerset(Long markerset) {
        this.markerset = markerset;
        return this;
    }

    @JsonProperty("min_contig_length")
    public Long getMinContigLength() {
        return minContigLength;
    }

    @JsonProperty("min_contig_length")
    public void setMinContigLength(Long minContigLength) {
        this.minContigLength = minContigLength;
    }

    public MaxBinInputParams withMinContigLength(Long minContigLength) {
        this.minContigLength = minContigLength;
        return this;
    }

    @JsonProperty("plotmarker")
    public Long getPlotmarker() {
        return plotmarker;
    }

    @JsonProperty("plotmarker")
    public void setPlotmarker(Long plotmarker) {
        this.plotmarker = plotmarker;
    }

    public MaxBinInputParams withPlotmarker(Long plotmarker) {
        this.plotmarker = plotmarker;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((((((((("MaxBinInputParams"+" [contigFile=")+ contigFile)+", assemblyRef=")+ assemblyRef)+", outHeader=")+ outHeader)+", workspaceName=")+ workspaceName)+", readsList=")+ readsList)+", thread=")+ thread)+", reassembly=")+ reassembly)+", probThreshold=")+ probThreshold)+", markerset=")+ markerset)+", minContigLength=")+ minContigLength)+", plotmarker=")+ plotmarker)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
