import paramiko
import argparse


def exec_command(connection, ip, cmd):
    """Executes commands on the server"""

    _, stdout, stderr = connection.exec_command(cmd)

    output = stdout.readlines() + stderr.readlines()

    if output:
        print(f"Output on {ip}")
        for line in output:
            print(line)


def connect():
    """Connects to the server"""

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    with open(args.hosts_file, "r") as file:
        for line in file:
            host_info = line.split(":")

            if len(host_info) == 3:
                client.connect(
                    hostname=host_info[0], port=22, username=host_info[1], password=host_info[2].rstrip('\n')
                )
            if len(host_info) == 4:
                client.connect(
                    hostname=host_info[0], port=int(host_info[1]), username=host_info[2],
                    password=host_info[3].rstrip('\n')
                )

            exec_command(client, host_info[0], args.cmd)


if __name__ == "__main__":
    usage_example = """
    Usage Example:
        python3 ssh_cmd.py -hf hosts.txt -c whoami
    """

    parser = argparse.ArgumentParser(epilog=usage_example, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hosts_file", "-hf", help="File with servers and credentials.\n"
                                                    "Hosts file example: ip:username:password")
    parser.add_argument("--cmd", "-c", help="Command that will be executed on the server")
    args = parser.parse_args()

    connect()
