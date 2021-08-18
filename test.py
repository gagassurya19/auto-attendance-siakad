from randomproxy import Random_Proxy
import json
# Create a class
proxy = Random_Proxy()

url = 'https://siswa.smktelkom-mlg.sch.id'
request_type = "post"

# Using Proxy {'https': '34.138.225.120:8888'}
r = proxy.Proxy_Request(url=url, request_type=request_type)
parseproxy = json.loads(json.dumps(r))
ipport = parseproxy["https"]