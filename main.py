import subprocess

serverProcess = subprocess.Popen(["start", "cmd", "/k", "python", "server.py"], shell=True)

clientProcess1 = subprocess.Popen(["start", "cmd", "/k", "python", "client.py"], shell=True)
clientProcess2 = subprocess.Popen(["start", "cmd", "/k", "python", "client.py"], shell=True)
clientProcess3 = subprocess.Popen(["start", "cmd", "/k", "python", "client.py"], shell=True)
# clientProcess4 = subprocess.Popen(["start", "cmd", "/k", "python", "client.py"], shell=True)
# clientProcess5 = subprocess.Popen(["start", "cmd", "/k", "python", "client.py"], shell=True)
# clientProcess6 = subprocess.Popen(["start", "cmd", "/k", "python", "client.py"], shell=True)
