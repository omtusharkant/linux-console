import psutil

while True:
    cpu_percent = psutil.cpu_percent(interval=1)

    print(cpu_percent)