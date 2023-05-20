import datetime
import platform
import hashlib
import time

from browser_history import get_history

my_system = platform.uname()

print(f"System: {my_system.system}")
print(f"Node Name: {my_system.node}")
print(f"Release: {my_system.release}")
print(f"Version: {my_system.version}")
print(f"Machine: {my_system.machine}")
print(f"Processor: {my_system.processor}")


# his is a list of (datetime.datetime, url) tuples
def cisloZeStringu(string: str):
    cislo = 0
    for char in string:
        cislo += ord(char)

    print(cislo)
    return cislo
def vytvorSeminko():
    seminko = datetime.datetime.now().timestamp()
    seminko *= cisloZeStringu(my_system.release)
    seminko %= cisloZeStringu(my_system.processor)
    seminko *= -(((cisloZeStringu(my_system.node) + datetime.datetime.now().timestamp()) % 2)-1)
    return seminko
timer = time.perf_counter()


history = get_history().histories[:5]
print("Browser: " + str(cisloZeStringu(str(hashlib.md5(str(history).encode()).hexdigest()))))

print(vytvorSeminko())

print(f"Program běžel na: {time.perf_counter() - timer:0.04f} sekund")