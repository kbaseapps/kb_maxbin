package kb_maxbin::kb_maxbinClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

kb_maxbin::kb_maxbinClient

=head1 DESCRIPTION


A KBase module: kb_maxbin


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => kb_maxbin::kb_maxbinClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 run_max_bin

  $returnVal = $obj->run_max_bin($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_maxbin.MaxBinInputParams
$returnVal is a kb_maxbin.MaxBinResult
MaxBinInputParams is a reference to a hash where the following keys are defined:
	contig_file has a value which is a kb_maxbin.File
	out_header has a value which is a string
	workspace_name has a value which is a string
	abund_list has a value which is a reference to a list where each element is a kb_maxbin.File
	reads_list has a value which is a reference to a list where each element is a kb_maxbin.File
	thread has a value which is an int
	reassembly has a value which is a kb_maxbin.boolean
	prob_threshold has a value which is a float
	markerset has a value which is an int
File is a reference to a hash where the following keys are defined:
	path has a value which is a string
	shock_id has a value which is a string
boolean is an int
MaxBinResult is a reference to a hash where the following keys are defined:
	result_directory has a value which is a string
	obj_ref has a value which is a string
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_maxbin.MaxBinInputParams
$returnVal is a kb_maxbin.MaxBinResult
MaxBinInputParams is a reference to a hash where the following keys are defined:
	contig_file has a value which is a kb_maxbin.File
	out_header has a value which is a string
	workspace_name has a value which is a string
	abund_list has a value which is a reference to a list where each element is a kb_maxbin.File
	reads_list has a value which is a reference to a list where each element is a kb_maxbin.File
	thread has a value which is an int
	reassembly has a value which is a kb_maxbin.boolean
	prob_threshold has a value which is a float
	markerset has a value which is an int
File is a reference to a hash where the following keys are defined:
	path has a value which is a string
	shock_id has a value which is a string
boolean is an int
MaxBinResult is a reference to a hash where the following keys are defined:
	result_directory has a value which is a string
	obj_ref has a value which is a string
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub run_max_bin
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function run_max_bin (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to run_max_bin:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'run_max_bin');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_maxbin.run_max_bin",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'run_max_bin',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method run_max_bin",
					    status_line => $self->{client}->status_line,
					    method_name => 'run_max_bin',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "kb_maxbin.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_maxbin.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'run_max_bin',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method run_max_bin",
            status_line => $self->{client}->status_line,
            method_name => 'run_max_bin',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for kb_maxbin::kb_maxbinClient\n";
    }
    if ($sMajor == 0) {
        warn "kb_maxbin::kb_maxbinClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 boolean

=over 4



=item Description

A boolean - 0 for false, 1 for true.
@range (0, 1)


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 File

=over 4



=item Description

File structure for input/output file


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
path has a value which is a string
shock_id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
path has a value which is a string
shock_id has a value which is a string


=end text

=back



=head2 MaxBinInputParams

=over 4



=item Description

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


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
contig_file has a value which is a kb_maxbin.File
out_header has a value which is a string
workspace_name has a value which is a string
abund_list has a value which is a reference to a list where each element is a kb_maxbin.File
reads_list has a value which is a reference to a list where each element is a kb_maxbin.File
thread has a value which is an int
reassembly has a value which is a kb_maxbin.boolean
prob_threshold has a value which is a float
markerset has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
contig_file has a value which is a kb_maxbin.File
out_header has a value which is a string
workspace_name has a value which is a string
abund_list has a value which is a reference to a list where each element is a kb_maxbin.File
reads_list has a value which is a reference to a list where each element is a kb_maxbin.File
thread has a value which is an int
reassembly has a value which is a kb_maxbin.boolean
prob_threshold has a value which is a float
markerset has a value which is an int


=end text

=back



=head2 MaxBinResult

=over 4



=item Description

result_folder: folder path that holds all files generated by run_max_bin
report_name: report name generated by KBaseReport
report_ref: report reference generated by KBaseReport


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
result_directory has a value which is a string
obj_ref has a value which is a string
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
result_directory has a value which is a string
obj_ref has a value which is a string
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=cut

package kb_maxbin::kb_maxbinClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
