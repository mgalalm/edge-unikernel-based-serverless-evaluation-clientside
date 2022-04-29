import matplotlib.pyplot as plt
import json
nanos = []
openwhisk = []
size = 16
for i in range(1, size + 1):
    f = open(f'../publication_results/invoke.nanos.{i}.helloworld..False.log')
    data = json.load(f)
    nanos.append(float(data['client_info']['total_elapsed_time']))
    f.close()
    f = open(f'../publication_results/invoke.openwhisk.{i}.helloworld..False.log')
    data = json.load(f)
    openwhisk.append(float(data['client_info']['total_elapsed_time']))
    f.close()
print(nanos, openwhisk)
plt.plot(range(1, size + 1),openwhisk, 'ro-', label="OW")
plt.plot(range(1, size + 1),nanos, 'bs--', label="NANOS")
# plt.plot([500,1000,2000,3000,10000],[500/4.881,1000/7.208,2000/9.643,3000/15.681,10000/65.649], 'bs--', label="NANOS")
plt.axis([0, size, 0, 60])
plt.xlabel('Concurrent calls')
plt.ylabel('Latency in seconds')
plt.legend(bbox_to_anchor=(1.02,1), loc=2, borderaxespad=0.)
# plt.savefig('test', bbox_inches='tight')
plt.show()