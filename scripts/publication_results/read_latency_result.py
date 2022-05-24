from email import header
from wsgiref import headers
import matplotlib.pyplot as plt
import json
import os
import csv

nanos = []
openwhisk = []
size = 16
script_dir = os.path.dirname(__file__)
for i in range(1, size + 1):
     
    rel_path = f'files/invoke.nanos.{i}.helloworld.latency.no_parmas.True.log'
    output_fname = os.path.join(script_dir, rel_path)
    f = open(output_fname)
    data = json.load(f)
    nanos.append(float(data['client_info']['total_elapsed_time']))
    f.close()
    
    rel_path = f'files/invoke.openwhisk.{i}.helloworld.latency.no_parmas.True.log'
    output_fname = os.path.join(script_dir, rel_path)
    f = open(output_fname)
    data = json.load(f)
    openwhisk.append(float(data['client_info']['total_elapsed_time']))
    f.close()

plt.plot(range(1, size + 1),openwhisk, 'ro-', label="OpenWhisk")
plt.plot(range(1, size + 1),nanos, 'bs--', label="NanoFaaS")
# plt.plot([500,1000,2000,3000,10000],[500/4.881,1000/7.208,2000/9.643,3000/15.681,10000/65.649], 'bs--', label="NANOS")
plt.axis([0, size, 0, 100])
plt.xlabel('Concurrent calls')
plt.ylabel('Latency in seconds')
plt.legend(bbox_to_anchor=(1.02,1), loc=2, borderaxespad=0.)
changes = []
for x1, x2 in zip(nanos, openwhisk):
    try:
        pct = (x2 - x1) * 100 / x1
    except ZeroDivisionError:
        pct = None
    changes.append(pct)
rows  = zip(range(1,17), openwhisk, nanos, changes)
with open("latency_results.csv", "w") as f:
    fieldnames = ['# of invocations','openwhisk', 'nanos', 'changes']
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    for row in rows:
        writer.writerow(row)
plt.savefig('latency', bbox_inches='tight')
# plt.show()