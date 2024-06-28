import os
import platform
import psutil


class HostInfo:
    def __init__(self) -> None:
        host = os.uname()
        self.machine_name = host.nodename
        self.OS = host.sysname
        self.kernel_ver = host.release
        self.ver = host.version
        os_name = platform.system()
        print(os_name)

    def get_Host_info(self):
        return {
            "machine_name": self.machine_name,
            "OS": self.OS,
            "kernel_ver": self.kernel_ver,
            "ver": self.ver
        }
    
    def get_uptime():
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            days = int(uptime_seconds // (24 * 3600))
            uptime_seconds %= (24 * 3600)
            hours = int(uptime_seconds // 3600)
            uptime_seconds %= 3600
            minutes = int(uptime_seconds // 60)
            seconds = int(uptime_seconds % 60)
            return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

print(HostInfo.get_uptime())

class ResourceUsage:

    @staticmethod
    def cpu_info():
        return f"{psutil.cpu_percent(interval=1)}"

    @staticmethod
    def ram_info():
        return f"{psutil.virtual_memory().percent}"
        
    @staticmethod
    def disk_info():
        du = psutil.disk_usage('/')
        return f"{du.percent}"

    @staticmethod
    def network_info():
        interface = ResourceUsage.active_interface()
        net_io = psutil.net_io_counters(pernic=True)
        if interface:
            if interface in net_io:
                counters = net_io[interface]
                return {
                    "interface": interface,
                    
                    "packets_sent": counters.packets_sent,
                    "packets_recv": counters.packets_recv,
                    
                }
            else:
                return {"error": f"Interface {interface} not found"}
        else:
            network_data = {}
            for iface, counters in net_io.items():
                network_data[iface] = {
                    
                    "packets_sent": counters.packets_sent,
                    "packets_recv": counters.packets_recv,
                    
                }
            return network_data

    @staticmethod
    def active_interface():
        net_io = psutil.net_io_counters(pernic=True)
        active_iface = None
        max_data = 0
        for iface, counters in net_io.items():
            total_data = counters.bytes_sent + counters.bytes_recv
            if total_data > max_data:
                max_data = total_data
                active_iface = iface
        return active_iface

    
    @staticmethod
    def get_packets_sent():
        interface = ResourceUsage.active_interface()
        net_io = psutil.net_io_counters(pernic=True)
        if interface:
            if interface in net_io:
                return net_io[interface].packets_sent
            else:
                return {"error": f"Interface {interface} not found"}
        else:
            packets_sent_data = {iface: counters.packets_sent for iface, counters in net_io.items()}
            return packets_sent_data

    @staticmethod
    def get_packets_recv():
        interface = ResourceUsage.active_interface()
        net_io = psutil.net_io_counters(pernic=True)
        if interface:
            if interface in net_io:
                return net_io[interface].packets_recv
            else:
                return {"error": f"Interface {interface} not found"}
        else:
            packets_recv_data = {iface: counters.packets_recv for iface, counters in net_io.items()}
            return packets_recv_data
