import argparse
import subprocess
import re
import os

def generate_inventory(ip_list):
    with open("inventory.txt", "w") as f:
        f.write("[all]\n")
        for ip in ip_list:
            f.write(f"{ip} ansible_user=root ansible_port=7730\n")

def run_ansible(playbook):
    cmd = ["ansible-playbook", f"./playbooks/{playbook}", "-i", "inventory.txt"]
    return subprocess.run(cmd)

def choose_least_load():
    with open("load_report.txt", "r") as f:
        data = {}
        for line in f.readlines():
            splitted = line.split(": ")
            data[splitted[0]] = splitted[2]

        dataCleaned = {}

        for ip, memValue in data.items():
            digitalsMem = re.findall(r'0\.\d+', memValue)
            dataCleaned[ip] = float(digitalsMem[0])
        
        sortedDict = dict(sorted(dataCleaned.items(), key=lambda item: item[1]))

        lessMemIp = list(sortedDict.items())[0]
        otherIp = list(sortedDict.items())[1]

        return str(lessMemIp[0]), str(otherIp[0])
    
def check_db_up(leastLoadIp):
    env = os.environ.copy()
    env["PGPASSWORD"] = "student"

    cmd = ["psql", "-h", f"{leastLoadIp}", "-U", "student", "-d", "student", "-c", "SELECT 1;"] 
    return subprocess.run(cmd, env=env)







def main():
    parser = argparse.ArgumentParser(prog='postgres-install')
    parser.add_argument("hosts", nargs="+", help="Comma-separated list of IPs or hostnames")
    args = parser.parse_args()

    generate_inventory(args.hosts)

    print("Gathering facts about conjunction of services...")

    run_ansible("gather_facts.ansible.yaml")

    print("Choosing less busy host...")

    leastLoadIp, otherIp = choose_least_load()
    leastLoadList = []
    leastLoadList.append(leastLoadIp)

    generate_inventory(leastLoadList)

    run_ansible("installPostgres.ansible.yaml")

    run_ansible("addUser.ansible.yaml")

    res = check_db_up("188.243.207.170")

    if(res.returncode != 0):
        print("DATABASE NOT WORKING")
    else:
        print("DATABASE IS WORKING")




    






main()