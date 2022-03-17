import os
import sys
import wmi
import win32com.shell.shell as shell
import subprocess

ASADMIN = 'asadmin'

def get_elevated_privleges():
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)

def test():
    c = wmi.WMI()
    for item in c.Win32_PhysicalMedia():
        if "PHYSICALDRIVE" in str(item.Tag).upper():
            serialNo = item.SerialNumber
            break
    print(serialNo)
def get_hard_drive_serial():
    c = wmi.WMI()
    for item in c.Win32_PhysicalMedia():
        if "PHYSICALDRIVE" in str(item.Tag).upper():
            return str(item.SerialNumber)

    return None

def get_id():
    if 'nt' in os.name:
        return subprocess.Popen('dmidecode.exe -s system-uuid'.split())
    else:
        return subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())
    
# print ("HD Serial as Regular User: " + get_hard_drive_serial())
# get_elevated_privleges()
# print ("HD Serial as Admin User: " + get_hard_drive_serial())
# test()

# c = wmi.WMI()
# drive_letter = "C:"
# for physical_disk in c.Win32_DiskDrive ():
#   for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
#     for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
#       if logical_disk.Caption == drive_letter:
#         print(physical_disk.Caption, partition.Caption, logical_disk.Caption)

# import subprocess

# serials = subprocess.check_output('wmic diskdrive get SerialNumber').decode().split('\n')[1:]
# serials = [s.strip() for s in serials if s.strip()]
# print(serials)

# import wmi
# c = wmi.WMI()
# for item in c.Win32_PhysicalMedia():
#     print (item)
    
import win32api

print (win32api.GetVolumeInformation("C:\\"))