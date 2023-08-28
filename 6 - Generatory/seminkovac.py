import datetime
import platform
import hashlib
import random
import time
import numpy
import psutil
import matplotlib.pyplot as plt

timer = time.perf_counter()
print(help)
my_system = platform.uname()
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

def vytvorSeminko( predesli = 0, size=2**16):
    predesli = predesli % size
    if predesli == 0:
        predesli = size
    
    cpu_times = psutil.cpu_times()
    seminko = cpu_times.user * cpu_times.idle % (predesli) + 1
    seminko *= datetime.datetime.now().timestamp() * (10**6) % (10**6)
    seminko *= cisloZeStringu(my_system.release)
    seminko /= cisloZeStringu(my_system.processor)
    seminko *= cisloZeStringu(my_system.node) 
    return round(seminko % size)

def vygenerujSeminka( pocet):
    seminka = list()
    stejneSeminka = list()
    for i in range(pocet):
        seminko = vytvorSeminko(sum(seminka))
        if seminko in seminka:
            stejneSeminka.append((i,seminko))
        seminka.append(seminko)
    return (seminka,stejneSeminka)

vystup = vygenerujSeminka(1000)


print(f"Generátor běžel na: {time.perf_counter() - timer:0.04f} sekund")

testSeminekRandom = list()

for i in range(1000):
    testSeminekRandom.append(random.randint(0,2**16))

print(numpy.average(vystup[0]))
print(numpy.average(testSeminekRandom))
print(vystup[1])

print(f"Program běžel na: {time.perf_counter() - timer:0.04f} sekund")

