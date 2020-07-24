echo "This script define some methods for snapshots, don't try to execute it directly"
exit 1

PASSWORD="test-password"
ELASTIC_CONTAINER="odfe-cauldron"
SNAPSHOT_NAME="test_snapshot"

# Create a new snapshot with the name $SNAPSHOT_NAME
docker exec $ELASTIC_CONTAINER curl -k -XPUT "https://admin:$PASSWORD@localhost:9200/_snapshot/cauldron_backup/$SNAPSHOT_NAME" -H 'Content-Type: application/json' -d'
{
  "indices": "*",
  "ignore_unavailable": true,
  "include_global_state": false,
}
'

# See all the snapshots created
docker exec $ELASTIC_CONTAINER curl -k -XGET "https://admin:$PASSWORD@localhost:9200/_snapshot/cauldron_backup/_all"


# Restore all the indices except .opendistro_security with the name "$NAME-restored". It uses the $SNAPSHOT_NAME backup
docker exec $ELASTIC_CONTAINER curl -k -XPOST "https://admin:$PASSWORD@localhost:9200/_snapshot/cauldron_backup/$SNAPSHOT_NAME/_restore" -H 'Content-Type: application/json' -d'
{
  "indices": "-.opendistro_security",
  "ignore_unavailable": true,
  "include_global_state": false,
  "include_aliases": false,
  "rename_pattern": "(.+)",
  "rename_replacement": "$1-restored"
}
'


# See the indices restored
docker exec $ELASTIC_CONTAINER curl -k -XGET "https://admin:$PASSWORD@localhost:9200/_cat/indices" | grep restored


# Delete and reindex the restored indices.
for index in git_raw_index git_enrich_index git_aoc_enriched_index github_raw_index github_enrich_index gitlab_raw_index gitlab_enriched_index meetup_raw_index meetup_enriched_index ; do
    echo $index-restored
    docker exec $ELASTIC_CONTAINER curl -k -XDELETE "https://admin:$PASSWORD@localhost:9200/$index"


    docker exec $ELASTIC_CONTAINER curl -k -XPOST "https://admin:$PASSWORD@localhost:9200/_reindex?pretty" -H 'Content-Type: application/json' -d'
    {
      "source": {
        "index": "'$index'-restored"
      },
      "dest": {
        "index": "'$index'"
      }
    }
    '
done
