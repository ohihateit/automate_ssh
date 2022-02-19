import paramiko
import argparse


def exec_command(connection, ip, cmd):
    """Executes command on the server"""

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

    if args.hosts_file:
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
    else:
        client.connect(
            hostname=args.ip, port=22, username=args.username, password=args.password.rstrip('\n')
        )

        exec_command(client, args.ip, args.cmd)


if __name__ == "__main__":
    usage_example = """
    Usage Example:
        python3 ssh_cmd.py -hf hosts.txt -c whoami
        python3 ssh_cmd.py -i 192.168.80.128 -u username -p password -c whoami
    """

    parser = argparse.ArgumentParser(epilog=usage_example, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hosts_file", "-hf", help="File with servers and credentials.\n"
                                                    "Hosts file example: ip:username:password")
    parser.add_argument("--cmd", "-c", help="Command that will be executed on the server")
    parser.add_argument("--ip", "-i", help="Server IP")

    args, _ = parser.parse_known_args()

    if args.ip:
        parser.add_argument("--username", "-u", help="User on the server", required=True)
        parser.add_argument("--password", "-p", help="Password for the user on the server", required=True)

        args = parser.parse_args()

    connect()
