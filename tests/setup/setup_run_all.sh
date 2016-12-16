#!/bin/bash
set -euxo pipefail

type -t virtualenv || { echo please install /usr/bin/virtualenv ; exit 1 ; }
type -t pip || { echo please install /usr/bin/pip ; exit 1 ; }
type -t wget || { echo please install /usr/bin/wget ; exit 1 ; }
type -t unzip || { echo please install /usr/bin/unzip ; exit 1 ; }

# different connection classes to test
#TEST_ES_CONNECTION=${TEST_ES_CONNECTION:-RequestsHttpConnection}
export TEST_ES_CONNECTION=${TEST_ES_CONNECTION:-Urllib3HttpConnection}
export IS_ES_SECURED=${IS_ES_SECURED:-true}
export ES_VER=${ES_VER:-2.4.2}
export SG_VER=${SG_VER:-2.4.2.9}
export SG_SSL_VER=${SG_SSL_VER:-2.4.2.19}
export ES_CONF=${ES_CONF:-./tests/conf}
export ES_HOME=${ES_HOME:-/tmp/elasticsearch}
export TMP_DIR=${TMP_DIR:-/tmp}

if [ ! -f ${TMP_DIR}/es.zip ] ; then
    wget -O ${TMP_DIR}/es.zip "https://oss.sonatype.org/service/local/artifact/maven/redirect?r=releases&g=org.elasticsearch.distribution.zip&a=elasticsearch&e=zip&v=${ES_VER}"
fi

if [ ! -d $ES_HOME ] ; then
    unzip ${TMP_DIR}/es.zip -d ${TMP_DIR}
    mv ${TMP_DIR}/elasticsearch-${ES_VER} ${ES_HOME}
fi

rm -rf $ES_HOME/{data,plugins,logs}
./tests/setup/sg_init.sh

virtualenv -q .venv
PS1=
. .venv/bin/activate
pip install -e .[test]

python setup.py test
