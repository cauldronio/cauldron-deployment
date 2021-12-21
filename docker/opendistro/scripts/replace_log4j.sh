#!/bin/bash
#
# Credits to Robert Spier
#

find /usr/share/elasticsearch -name 'log4j-*.jar' | while read f; do
    base=$(basename $(echo $f | sed -e 's/-[0-9]\+\.[0-9]\+\.[0-9]\+\.jar$//'))
    dir=$(dirname $f)
    rm $f
    ln -f /usr/local/lib/${base}.jar $dir
done
