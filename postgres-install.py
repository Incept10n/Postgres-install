import argparse
import subprocess
import re

def generate_inventory(ip_list):
    with open("inventory.txt", "w") as f:
        f.write("[all]\n")
        for ip in ip_list:
            f.write(f"{ip}\n")

def run_ansible(playbook, limit=None):
    cmd = ["ansible-playbook", f"./playbooks/{playbook}", "-i", "inventory.txt"]
    if limit:
        cmd += ["--limit", limit]
    return subprocess.run(cmd)

def choose_least_load():
    with open("freemem_report.txt", "r") as f:
        data = {}
        for line in f.readlines():
            splitted = line.split(": ")
            data[splitted[0]] = splitted[2]

        dataCleaned = {}

        for ip, memValue in data.items():
            digitalsMem = re.findall(r'\d+', memValue)
            dataCleaned[ip] = int(digitalsMem[0])
        
        sortedDict = dict(sorted(dataCleaned.items(), key=lambda item: item[1]))

        lessMemIp = list(sortedDict.items())[0]

        return str(lessMemIp[0])
        






def main():
    parser = argparse.ArgumentParser(prog='postgres-install')
    parser.add_argument("hosts", nargs="+", help="Comma-separated list of IPs or hostnames")
    args = parser.parse_args()

    # generate_inventory(args.hosts)

    print("Gathering facts about conjunction of services...")

    # run_ansible("gather_facts.ansible.yaml")

    choose_least_load()



    # print("Then less busy host will be chosen and postgress will be installed...")





main()