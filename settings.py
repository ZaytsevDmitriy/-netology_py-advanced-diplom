import os

with open('.env', 'r') as file:
    while True:
        line = file.readline().rstrip()
        if not line:
            break
        os.environ[line[:line.find("=")]] = line[line.find("=") + 1:]
        if os.environ[line[:line.find("=")]]==os.environ['GROUP_TOKEN']:
            GROUP_TOKEN = os.environ['GROUP_TOKEN']
        else :
            USER_TOKEN = os.environ['USER_TOKEN']
        if not line:
            break




