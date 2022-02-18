import paramiko


def exec_command(connect, ip, cmd):
    _, stdout, stderr = connect.exec_command(cmd)

    output = stdout.readlines() + stderr.readlines()

    if output:
        print(f"Output on {ip}")
        for line in output:
            print(line)


def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Hosts file format: ip:username:password
    with open("hosts.txt", "r") as file:
        for line in file:
            host_info = line.split(":")
            
            if len(host_info) == 3:
                client.connect(
                    hostname=host_info[0], port=22, username=host_info[1], password=host_info[2].rstrip('\n')
                )
            if len(host_info) == 4:
                client.connect(
                    hostname=host_info[0], port=host_info[1], username=host_info[2], password=host_info[3].rstrip('\n')
                )

            exec_command(client, host_info[0], "cat /etc/passwd; touch lol.txt; echo \"I love you!\" > lol.txt")



if __name__ == "__main__":
    # TODO: Add argparse
    connect()
