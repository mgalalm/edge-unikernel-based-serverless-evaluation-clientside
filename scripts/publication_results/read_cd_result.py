import json
import os


def read_versions(platform, rel_path):
    script_dir = os.path.dirname(__file__)
   
    output_fname = os.path.join(script_dir, rel_path)
    f = open(output_fname)
    data = json.load(f)
    for key in data:
        if 'version' in data[key]:
            platform.append(data[key]['version'])
nanos = []
openwhisk = []
nanos_path = 'files/invoke.nanos.16.helloworld..False.log'
ow_path = 'files/invoke.openwhisk.16.helloworld..False.log'
read_versions(nanos, nanos_path)
read_versions(openwhisk, ow_path)

print(openwhisk, nanos)