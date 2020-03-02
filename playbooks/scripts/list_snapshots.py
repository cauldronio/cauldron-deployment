import subprocess
import json
import argparse


class ElasticSearchSnapshots:
    def __init__(self, ssh_host, elastic_container, admin_password):
        self.ssh_host = ssh_host
        self.elastic_container = elastic_container
        self.admin_password = admin_password

    def list_snapshots(self):
        """elastic_container
        Return the list of snapshots of a ElasticSearch cluster running inside a Docker container in a remote host.
        :return:
        """
        info_snaps = list()
        repos = self.repository_list()

        cmd = ["ssh", self.ssh_host]
        docker_curl_fmt = "docker exec {} curl -k -XGET https://admin:{}@localhost:9200/_snapshot/{}/_all"

        for repo in repos:
            cmd = ["ssh", self.ssh_host, docker_curl_fmt.format(self.elastic_container,
                                                                self.admin_password,
                                                                repo)]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                snapshots_repo = json.loads(result.stdout)
            except json.decoder.JSONDecodeError:
                print(f"Error from server: {result.stdout.decode('utf-8')}")
                snapshots_repo = {'snapshots': []}
            for snap in snapshots_repo['snapshots']:
                info_snaps.append({
                    'repository': repo,
                    'snapshot_name': snap['snapshot'],
                    'start_time': snap['start_time'],
                    'state': snap['state'],
                    'end_time': snap['end_time']
                })
        return info_snaps

    def repository_list(self):
        """
        Get a list of the repositories configured for the ElasticSearch cluster for snapshots
        :return:
        """
        docker_curl_url = "docker exec {} " \
                          "curl -k -XGET https://admin:{}@localhost:9200/_snapshot/_all".format(self.elastic_container,
                                                                                                self.admin_password)
        cmd = ["ssh", self.ssh_host, docker_curl_url]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            data = json.loads(result.stdout)
        except json.decoder.JSONDecodeError:
            print(f"Error from server: {result.stdout.decode('utf-8')}")
            data = {}
        return data.keys()

    @staticmethod
    def beauty_list(snap_list):
        if len(snap_list) == 0:
            print("No snapshots found")
            return
        print("{: <30} {: <30} {: <30} {: <30} {: <10}".format("REPOSITORY", "NAME", "START TIME", "FINISH TIME", "STATUS"))
        print("{: <30} {: <30} {: <30} {: <30} {: <10}".format("=" * 10, "=" * 4, "=" * 10, "=" * 11, "=" * 6))
        for snap in snap_list:
            print("{: <30} {: <30} {: <30} {: <30} {: <10} ".format(snap['repository'],
                                                                    snap['snapshot_name'],
                                                                    snap['start_time'],
                                                                    snap['end_time'],
                                                                    snap['state']))


def setup_args():
    parser = argparse.ArgumentParser(description='List the snapshots available in a ElasticSearch instance '
                                                 'running in Docker.')
    parser.add_argument('--ssh', dest='ssh_host', action='store', required=True,
                        help='remote ssh, i.e. --ssh user@host')
    parser.add_argument('--password', dest='admin_password', action='store', required=True,
                        help='admin password for ElasticSearch.')
    parser.add_argument('--container', dest='elastic_container', action='store',
                        default='elastic_service',
                        help='ElasticSearch Docker container (default: elastic_service)')

    return parser.parse_args()


if __name__ == "__main__":
    args = setup_args()
    es_snapshots = ElasticSearchSnapshots(args.ssh_host, args.elastic_container, args.admin_password)
    snapshots_list = es_snapshots.list_snapshots()
    ElasticSearchSnapshots.beauty_list(snapshots_list)
