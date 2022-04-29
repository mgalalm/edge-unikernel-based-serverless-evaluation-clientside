#!/usr/bin/python3
from subprocess import check_output
from multiprocessing.pool import ThreadPool
import time
import json
import argparse
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
 ./invoker.py  2  myaction117
'''
def argument_parser(parser=None):
    if not parser:
        parser = argparse.ArgumentParser(description="OpenWhisk invocation")
    parser.add_argument('isize', metavar='cnt', type=int, help='number of'
            + ' invocation')
    parser.add_argument('func_names', metavar='fnames', type=str, help='Function'
            + ' name(s) to invoke')
    parser.add_argument('--params', metavar='params', type=str, help='parameters'
            + ' to a function (json)', default=None, required=False)
    parser.add_argument('--concurrent', action='store_true', dest='concurrent', 
            default=False, help='Concurrency concurrent|sequential')
 
    args = parser.parse_args()
    if args.params is not None:
        args.params = json.loads(args.params)
    return (args, parser)

def invoke( cmd):
    s = time.time()
    res =  check_output(cmd.split())
    e = time.time() - s
    return (res, e)

def parse_response(text) :

        res = json.loads(text)
        message = res['response']['result']['message']
        return {
            "message": message,
            "raw": str(res),
            "activationId": res["activationId"]
        }


def handler(event, cmd):
    p = ThreadPool(64)
    res = []
    start_time = time.time()
    invocation_size = event['invoke_size']
    for _ in range(int(invocation_size)):
        res.append(p.apply_async(invoke, args=(cmd,)))
    all_result = {}
    
    for i in res:
        r = i.get()
        text = r[0].decode("ascii").split("\n",1)[1]
        rdict = parse_response(text)
        rdict['client_info'] = {'elapsed_time': r[1], "blocking": True}
        all_result[rdict['activationId']] = rdict
    
    end_time = time.time()
    p.close()
    p.join()
   
    elapsed_time = end_time - start_time
    logging.info(f"total elapsed_time: {elapsed_time}")
    
    all_result['client_info'] = {'start_time': '{}'.format(start_time),
            'end_time': '{}'.format(end_time),
            'total_elapsed_time': '{}'.format(elapsed_time)}
    
    return all_result


def to_file(fname, data):
    with open(fname, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    args, parser = argument_parser()
    event = {}
    event['invoke_size'] = args.isize
    cmd = f"wsk -i action invoke {args.func_names} --blocking"
    res = handler(event, cmd)
    # print(res['client_info']['total_elapsed_time'])
    
    params_fstr = ''.join(e for e in str(args.params) if e.isalnum() or e == ":") if args.params is not None else ''
    
    output_fname = ("../publication_results/invoke.{}.{}.{}.{}.{}.log".format("openwhisk", args.isize,
        args.func_names, params_fstr, args.concurrent))

    to_file(output_fname, res)