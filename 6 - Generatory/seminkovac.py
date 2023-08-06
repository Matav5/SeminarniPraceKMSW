import datetime
import platform
import hashlib
import random
import time
import numpy
import psutil
import matplotlib.pyplot as plt

timer = time.perf_counter()

my_system = platform.uname()
psutil.cpu_percent()
print(datetime.datetime.now().timestamp() )
print(f"System: {my_system.system}")
print(f"Node Name: {my_system.node}")
print(f"Release: {my_system.release}")
print(f"Version: {my_system.version}")
print(f"Machine: {my_system.machine}")
print(f"Processor: {my_system.processor}")
print(datetime.datetime.now().timestamp() )

# his is a list of (datetime.datetime, url) tuples
def cisloZeStringu(string: str):
    cislo = 0
    for char in string:
        cislo += ord(char)
    return cislo
def vytvorSeminko():
    seminko = psutil.disk_usage(psutil.disk_partitions()[0].device).percent
    seminko *= datetime.datetime.now().timestamp() * (10**6) % (10**6)
    seminko *= cisloZeStringu(my_system.release)
    seminko *= cisloZeStringu(my_system.processor)
    seminko *= cisloZeStringu(my_system.node) 
    return numpy.uint(seminko % (2**16))


print(vytvorSeminko())

testSeminek = list()
for i in range(1000):
    seminko = vytvorSeminko()
    print(seminko)
    testSeminek.append(seminko)

testSeminekRandom = list()
for i in range(1000):
    testSeminekRandom.append(random.randint(0,2**16))

print(numpy.average(testSeminek))
print(numpy.average(testSeminekRandom))

print(f"Program běžel na: {time.perf_counter() - timer:0.04f} sekund")

plt.axis()