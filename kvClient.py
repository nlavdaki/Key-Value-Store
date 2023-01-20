import argparse
import json
import requests
import random
import sympy
from sympy.parsing.sympy_parser import parse_expr

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server-file', required=True, help='file containing a list of servers and their ports')
    parser.add_argument('-i', '--data-file', required=True, help='file containing the data to index')
    parser.add_argument('-k', '--replication-factor', type=int, default=1, help='number of servers to replicate data to')
    args = parser.parse_args()

    # read list of servers from file
    with open(args.server_file, 'r') as f:
        servers = [line.strip().split() for line in f]

    # read data from file
    with open(args.data_file, 'r') as f:
        lines = f.read().splitlines()
        for i in range(len(lines) - 1):
            lines[i] += ","
    #jsonise data
        d = "".join(lines)
        d = "{" + d + "}"
        da = json.dumps(d)
        dat = json.loads(da)
        data = json.loads(dat)

    for key, value in data.items():
    # choose k randomly servers to send the put request to
        chosen_servers = random.sample(servers, args.replication_factor)
        for server in chosen_servers:
            ip, port = server[0], server[1]
            url = f'http://{ip}:{port}/put'
            payload = {"key": key, "value": value}
            r = requests.put(url, json=payload)
            if r.status_code == 200:
                print(f"OK! {key} -> {value} stored succesfully")
            else:
                try:
                    print(f'ERROR! {key} -> {value} unsuccesfull storing')
            except requests.exceptions.ConnectionError:
                print(f'Error connecting to {ip}:{port}')
    while True:
        command = input("Enter command (GET key, DELETE key, QUERY key.subkey, COMPUTE f(x,y,...) WHERE x = QUERY key1.key2 AND y = QUERY key3 AND …): ")
        command_parts = command.strip().split()
        if command_parts[0] == "GET":
            key = command_parts[1]
            for server in servers:
                ip, port = server[0], server[1]
                url = f'http://{ip}:{port}/get/{key}'
                try:
                    r = requests.get(url)
                    if r.status_code == 200:
                        val = (r.text).replace('  "___":','').replace('  ', ' ').replace('\n', ' ')
                        print(f'GET {key} -> {val}')
                    else:
                        print(f'NOT FOUND : Error getting key {key} from {ip}:{port}: {r.text}')
                except requests.exceptions.ConnectionError:
                    print(f'Error connecting to server: {ip}:{port}')

        elif command_parts[0] == "DELETE":
            key = command_parts[1]
            for server in servers:
                ip, port = server[0], server[1]
                url = f'http://{ip}:{port}/delete/{key}'
                try:
                    r = requests.delete(url)
                    if r.status_code == 200:
                        print(f'DELETE {key} successful on {ip}:{port}')
                    else:
                        print(f'Error deleting key {key} from {ip}:{port}: {r.text}')
                except requests.exceptions.ConnectionError:
                    print(f'Error connecting to server {ip}:{port}')

        elif command_parts[0] == "QUERY":
            key = command_parts[1]
            for server in servers:
                ip, port = server[0], server[1]
                url = f'http://{ip}:{port}/query/{key}'
                try:
                    r = requests.get(url)
                    if r.status_code == 200:
                        if 'error' in r.json():
                            print(r.json()['error'])
                        else:
                            print(f'QUERY {key} : {r.json()["value"]}')
                except requests.exceptions.ConnectionError:
                    print(f'Error {r.status_code}  connecting to server {ip}:{port}')

        elif command_parts[0] == "COMPUTE":
            formula = command_parts[1]
            expression=sympy.parse_expr(formula)
            variables=expression.free_symbols
            values={}
            for variable in variables:
                key=command_parts[command_parts.index(str(variable)) + 3]
                for server in servers:
                    ip, port = server[0], server[1]
                    url = f'http://{ip}:{port}/compute/{key}'
                    try:
                        r=requests.get(url)
                        if r.status_code == 200:
                            val = {r.json()["value"]}
                            if 'error' in val:
                                print('error:' + str(val))
                            else:
                                values[variable] = float(val.pop())
                        else:
                            print(f'NOT FOUND : Error getting key {key} from {ip}:{port}: {r.text}')
                    except requests.exceptions.ConnectionError:
                        print(f'Error connecting to server: {ip}:{port}')
            result = expression.subs(values).evalf()
            print(f'COMPUTE {formula} -> {result}')

        else:
            print("Invalid command")



