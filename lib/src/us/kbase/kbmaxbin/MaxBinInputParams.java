
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
 * out_header: output file header
 * workspace_name: the name of the workspace it gets saved to.
 * semi-required: at least one of the following parameters is needed
 * abund_list: contig abundance file(s)/shock_id(s)
 * reads_list: reads file(s)/shock_id(s) in fasta or fastq format
 * optional params:
 * thread: number of threads; default 1
 * reassembly: specify this option if you want to reassemble the bins.
 *             note that at least one reads file needs to be designated.
 * prob_threshold: minimum probability for EM algorithm; default 0.8
 * markerset: choose between 107 marker genes by default or 40 marker genes
 * ref: http://downloads.jbei.org/data/microbial_communities/MaxBin/README.txt
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "contig_file",
    "out_header",
    "workspace_name",
    "abund_list",
    "reads_list",
    "thread",
    "reassembly",
    "prob_threshold",
    "markerset"
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
    private us.kbase.kbmaxbin.File contigFile;
    @JsonProperty("out_header")
    private String outHeader;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("abund_list")
    private List<us.kbase.kbmaxbin.File> abundList;
    @JsonProperty("reads_list")
    private List<us.kbase.kbmaxbin.File> readsList;
    @JsonProperty("thread")
    private Long thread;
    @JsonProperty("reassembly")
    private Long reassembly;
    @JsonProperty("prob_threshold")
    private Double probThreshold;
    @JsonProperty("markerset")
    private Long markerset;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: File</p>
     * <pre>
     * File structure for input/output file
     * </pre>
     * 
     */
    @JsonProperty("contig_file")
    public us.kbase.kbmaxbin.File getContigFile() {
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
    public void setContigFile(us.kbase.kbmaxbin.File contigFile) {
        this.contigFile = contigFile;
    }

    public MaxBinInputParams withContigFile(us.kbase.kbmaxbin.File contigFile) {
        this.contigFile = contigFile;
        return this;
    }

    @JsonProperty("out_header")
    public String getOutHeader() {
        return outHeader;
    }

    @JsonProperty("out_header")
    public void setOutHeader(String outHeader) {
        this.outHeader = outHeader;
    }

    public MaxBinInputParams withOutHeader(String outHeader) {
        this.outHeader = outHeader;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public MaxBinInputParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("abund_list")
    public List<us.kbase.kbmaxbin.File> getAbundList() {
        return abundList;
    }

    @JsonProperty("abund_list")
    public void setAbundList(List<us.kbase.kbmaxbin.File> abundList) {
        this.abundList = abundList;
    }

    public MaxBinInputParams withAbundList(List<us.kbase.kbmaxbin.File> abundList) {
        this.abundList = abundList;
        return this;
    }

    @JsonProperty("reads_list")
    public List<us.kbase.kbmaxbin.File> getReadsList() {
        return readsList;
    }

    @JsonProperty("reads_list")
    public void setReadsList(List<us.kbase.kbmaxbin.File> readsList) {
        this.readsList = readsList;
    }

    public MaxBinInputParams withReadsList(List<us.kbase.kbmaxbin.File> readsList) {
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

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((("MaxBinInputParams"+" [contigFile=")+ contigFile)+", outHeader=")+ outHeader)+", workspaceName=")+ workspaceName)+", abundList=")+ abundList)+", readsList=")+ readsList)+", thread=")+ thread)+", reassembly=")+ reassembly)+", probThreshold=")+ probThreshold)+", markerset=")+ markerset)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
