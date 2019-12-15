import pandas as pd

entry_template = """[program:{}]
command=python ./crawling.py run {}
autostart=true
autorestart=true
stderr_logfile=./Logs/{}/error.log
stdout_logfile=./Logs/{}/output.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 3
numprocs=1
"""

emoji_codes = pd.read_csv('../emoji_unicode.csv', header=None, names =['code', 'zipped'])
zipped = emoji_codes['zipped']

with open('supervisord.conf', 'w+') as file:
    for code in zipped:
        config = entry_template.format(code, code, code, code)
        file.write(config)
        file.write('\n')

    file.write('[supervisord]\n\n')
    file.write('[supervisorctl]\n\n')
    file.write('[inet_http_server]\nport = *:9001\n\n')
    file.write('[rpcinterface:supervisor]\nsupervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface')
