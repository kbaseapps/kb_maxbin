
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
 * <p>Original spec-file type: BinnedAssembly</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "bin_ids",
    "bin2contig_id",
    "contig_id2contig_ref"
})
public class BinnedAssembly {

    @JsonProperty("bin_ids")
    private List<String> binIds;
    @JsonProperty("bin2contig_id")
    private Map<String, List<String>> bin2contigId;
    @JsonProperty("contig_id2contig_ref")
    private Map<String, String> contigId2contigRef;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("bin_ids")
    public List<String> getBinIds() {
        return binIds;
    }

    @JsonProperty("bin_ids")
    public void setBinIds(List<String> binIds) {
        this.binIds = binIds;
    }

    public BinnedAssembly withBinIds(List<String> binIds) {
        this.binIds = binIds;
        return this;
    }

    @JsonProperty("bin2contig_id")
    public Map<String, List<String>> getBin2contigId() {
        return bin2contigId;
    }

    @JsonProperty("bin2contig_id")
    public void setBin2contigId(Map<String, List<String>> bin2contigId) {
        this.bin2contigId = bin2contigId;
    }

    public BinnedAssembly withBin2contigId(Map<String, List<String>> bin2contigId) {
        this.bin2contigId = bin2contigId;
        return this;
    }

    @JsonProperty("contig_id2contig_ref")
    public Map<String, String> getContigId2contigRef() {
        return contigId2contigRef;
    }

    @JsonProperty("contig_id2contig_ref")
    public void setContigId2contigRef(Map<String, String> contigId2contigRef) {
        this.contigId2contigRef = contigId2contigRef;
    }

    public BinnedAssembly withContigId2contigRef(Map<String, String> contigId2contigRef) {
        this.contigId2contigRef = contigId2contigRef;
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
        return ((((((((("BinnedAssembly"+" [binIds=")+ binIds)+", bin2contigId=")+ bin2contigId)+", contigId2contigRef=")+ contigId2contigRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
