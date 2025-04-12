import argparse
import subprocess

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

def main():
    parser = argparse.ArgumentParser(prog='postgres-install')
    parser.add_argument("hosts", nargs="+", help="Comma-separated list of IPs or hostnames")
    args = parser.parse_args()

    # generate_inventory(args.hosts)

    print("Gathering facts about conjunction of services...")
    run_ansible("gather_facts.ansible.yaml")

    # print("Then less busy host will be chosen and postgress will be installed...")



main()