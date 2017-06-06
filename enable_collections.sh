#!/bin/sh
node_port=$1
user=$2
pass=$3
bucket=$4

if [ $# -ne 4 ]; then
    echo "Usage: enable_colections.sh node:port user password bucket"
    exit 1
fi

echo "Enabling collections on $node_port for bucket $bucket"

curl -i -u $user:$pass --data '[ns_config:set({node, N, memcached_config_extra}, [{collections_prototype, true}]) || N <- ns_node_disco:nodes_wanted()].' http://$node_port/diag/eval
curl -i -u $user:$pass --data "ns_bucket:update_bucket_props(\"$bucket\", [{extra_config_string, \"collections_prototype_enabled=true\"}])." http://$node_port/diag/eval
curl -u $user:$pass -X POST http://$node_port/pools/default/settings/memcached/node/self  --data privilege_debug=false

echo
echo "Restarting memcached"
pkill memcached
