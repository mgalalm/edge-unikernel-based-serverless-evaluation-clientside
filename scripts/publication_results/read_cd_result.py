from matplotlib import markers
import matplotlib.pyplot as plt
import json
import os
from enum import Enum
import csv

COLOR_CONSTS = {1: 'grey', 2: 'green', 0: 'red'}
MARKER_CONSTS = {1: '.', 2: '+', 0: 'x'}
cnt=0
o_x = list(range(4))
o_y = list(range(4))
n_x = list(range(4))
n_y = list(range(4))
elastic_list = list(range(4))
axes = list(range(5))
axes2 = list(range(5))

def read_versions(platform):
    result = []
    count = 1
    for idx in range(1, 11):
        data = load_data(platform, idx)
        for key in data:
            if 'version' in data[key]:
                version = int(data[key]['version'])
                # marker, color = '.', 'grey' if version == 1 else '+', 'green'
                result.append([count, version, data[key]['client_info']['elapsed_time']])
                count += 1
    return result

def load_data(platform, idx):
    script_dir = os.path.dirname(__file__)
    rel_path = f'files/invoke.{platform}.16.helloworld.cd_{idx}.no_parmas.True.log'
    output_fname = os.path.join(script_dir, rel_path)
    f = open(output_fname)
    data = json.load(f)
    return data

nanos = read_versions("nanos")
openwhisk  = read_versions("openwhisk")

fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(6, 4))
fig.text(0.5, .99, 'Source Code Changes', ha='center', va='top')
fig.text(0.5, 0.00, 'Function Invocations', ha='center') 
fig.text(0.06, 0.5, 'Execution in seconds', va='center', rotation='vertical')

axes[cnt] = plt.subplot(1,2,cnt+1)
o_x[cnt] = [x[0] for x in openwhisk ]
o_y[cnt] = [x[2] for x in openwhisk ]
markers = [MARKER_CONSTS[x[1]] for x in openwhisk ]
colors = [ COLOR_CONSTS[x[1]]  for x in openwhisk ]
for x, y, c, m in zip(o_x[cnt],o_y[cnt], colors, markers):
    axes[cnt].scatter(x, y, alpha=0.8, c=c, marker=m, )  


axes[cnt].set_title('OpenWhisk')
axes[cnt].set_ylim([0,20])
results = zip(o_x[cnt],o_y[cnt], colors, markers)
grey_count = 0
green_count = 0 
red_count = 0 
for x, y, c, m in results:
    if c == 'grey':
        grey_count +=1

    elif c == 'green':
        green_count += 1
    else:
        red_count += 1
print(grey_count, green_count, red_count)


cnt += 1
axes[cnt] = plt.subplot(1,2,cnt+1)
o_x[cnt] = [x[0] for x in nanos]
o_y[cnt] = [x[2] for x in nanos]
axes[cnt].set_ylim([0,20])
markers = [MARKER_CONSTS[x[1]] for x in nanos ]
colors = [ COLOR_CONSTS[x[1]]  for x in nanos ]
for x, y, c, m in zip(o_x[cnt],o_y[cnt], colors, markers):
    axes[cnt].scatter(x, y, alpha=0.8, c=c, marker=m, )  
axes[cnt].set_title('NanoFaaS')
plt.savefig('cd', bbox_inches='tight')
results = zip(o_x[cnt],o_y[cnt], colors, markers)
grey_count = 0
green_count = 0 
red_count = 0 
for x, y, c, m in results:
    if c == 'grey':
        grey_count +=1

    elif c == 'green':
        green_count += 1
    else:
        red_count += 1
print(grey_count, green_count, red_count)
# plt.show()
# print(nanos)