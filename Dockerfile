FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.


# To install all the dependencies
RUN apt-get update && apt-get install -y build-essential wget make curl unzip python autoconf && \
    apt-get install -y r-base r-cran-gplots

# To download the Maxbin software and untar it
RUN mkdir MaxBin && cd MaxBin && \
    wget https://sourceforge.net/projects/maxbin2/files/MaxBin-2.2.4.tar.gz/download --no-check-certificate &&\
    tar xvf download && \
    cd MaxBin-2.2.4/src && \
    make && \
    cd .. && \
    ./autobuild_auxiliary && \
    cd .. && \
    cp -R MaxBin-2.2.4 /kb/deployment/bin/MaxBin

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
