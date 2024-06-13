import os
import platform

class hostinfo:
    def __init__(self) -> None:
        host = os.uname()

        self.machine_name = host.nodename

        self.OS = host.sysname

        self.kernel_ver = host.release

        self.ver = host.version

        os_name = platform.system()

        print(os_name)

