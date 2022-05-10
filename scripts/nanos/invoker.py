#!/usr/local/bin/python3
import time
from multiprocessing.pool import ThreadPool
import requests
import logging
import json
import argparse
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    parser.add_argument('--type', metavar='type', type=str, help='Test type', default=None, required=True)
    
    args = parser.parse_args()
    if args.params is not None:
        args.params = json.loads(args.params)
    return (args, parser)


def invoke(args):
    s = time.time()
    url = f"http://192.168.178.72:8080/{args.func_names}"
    res = {}
    e = 0
    try:
        response = requests.get(url)
        res = response.json()
        e = time.time() - s
    except requests.exceptions.RequestException as e:
        pass
    else:
        return (res, e)

def parse_response(res) :
        return res

def handler(event, args):
    p = ThreadPool(64)
    res = []
    start_time = time.time()
    invocation_size = event['invoke_size']
    for _ in range(int(invocation_size)):
        res.append(p.apply_async(invoke, args=(args,)))
    all_result = {}
    
    for idx, i in enumerate(res):
        r = i.get()
        print(r)
        rdict = {
            'message' : None,
            'version': 0,
            'client_info': {'elapsed_time': 0, "blocking": True}
        }
        # text = r[0].decode("ascii").split("\n",1)[1]
        if r is not None:
            rdict = parse_response(r[0])
            rdict['client_info'] = {'elapsed_time': r[1], "blocking": True}
        all_result[idx + 1] = rdict
    
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
    # cmd = f"wsk -i action invoke {args.func_names} --blocking"
    res = handler(event, args)
    
    params_fstr = ''.join(e for e in str(args.params) if e.isalnum() or e == ":") if args.params is not None else 'no_parmas'
    script_dir = os.path.dirname(__file__)
    out_put_file_path = "../publication_results/files/invoke.{}.{}.{}.{}.{}.{}.log".format("nanos", args.isize,
    args.func_names, args.type, params_fstr, args.concurrent)
    output_fname = os.path.join(script_dir, out_put_file_path)

    # output_fname = ("../publication_results/invoke.{}.{}.{}.{}.{}.log".format("nanos", args.isize,
    #     args.func_names, params_fstr, args.concurrent))

    to_file(output_fname, res)
    # for i in res:
    #    print(i.get()) 
