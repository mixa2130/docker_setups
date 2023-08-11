import sys
import re

for line in sys.stdin:
    ip, _http_url, page_size, http_status, _client_app_info, creation_date = line.strip().split('\t')
    http_url = re.sub(r'.\w+/', '.com/', _http_url)
    client_app_info = _client_app_info.split()[0]
    print('\t'.join([ip, creation_date, http_url, page_size, http_status, client_app_info]))
