import os
from datetime import datetime
import time
from threading import Thread
from . import plc_api
from .config import COLLECT_OPTION
from .config import TEST_OPTION


count = 0

def send(sender, id, is_normal, collect_time):
    #time.sleep(0.08)
    i = 0
    if is_normal == 0:
        i += 1
    global count
    current_time = datetime.now()
    lead_time = current_time - collect_time
    print('Send result, id:', id, '/ result:', is_normal, '/ lead_time:', lead_time.total_seconds())
    #process_time = COLLECT_OPTION['collect_cycle'] - read_time.total_seconds() - 0.01
    #process_time = 0.3  - read_time.total_seconds()
    #process_time = 0.2
    #if process_time < 0:
    #    sender.send_result(collect_time.timestamp(), 0, 'sender')
    #else:
    #    time.sleep(process_time)

    # sender.send_result(collect_time.timestamp(), 0 if not is_normal else 1, 'sender')
    # log_dir = '/app/result'
    # logfile = log_dir + '/result.txt'
    # count += 1
    # with open(logfile, 'a+') as f:
    #     f.write('count : '+ str(count) + 'Send result, id:'+ str(id)+ '/ result:'+ str(is_normal)+ '/ lead_time:'+ str(lead_time.total_seconds()) + '\n')


def run(meta, data, push):
    _id = meta['id']
    collect_time = meta['time']
    is_normal = data

    if TEST_OPTION['mode'] == 'jump':
        if _id % 2 == 0:
            is_normal = False
        else:
            is_normal = True
    #plc_api.send_result(collect_time.timestamp(), 0 if not is_normal else 1, 'sender')
    #send(plc_api, _id, is_normal, collet_time)
    p = Thread(target=send, args=(plc_api, _id, is_normal, collect_time))
    p.start()
    
