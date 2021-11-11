
import os
import re
import shutil
from sys import argv

print("Uninstalling can_decoder app...")
path_to_app = "/etc/capsule/can_decoder"
path_to_log = "/var/log/capsule/can_decoder.log"
path_to_conf = "/etc/capsule/can_decoder/config.yaml"
path_to_services = "/etc/systemd/system/can_decoder.service"
if "-y" in argv and os.path.exists(path_to_conf):
    print("Remove folder", path_to_conf)
    shutil.rmtree(path_to_conf)
elif input("Want to remove config ? y/[N]").capitalize() == "Y" and os.path.exists(path_to_conf):
    print("Remove folder", path_to_conf)
    shutil.rmtree(path_to_conf)
if os.path.exists(path_to_log):
    print("Remove log ", path_to_log)
    os.remove(path_to_log)
if os.path.exists(path_to_services):
    print("Remove can_decoder service")
    os.system("systemctl stop can_decoder.service")
    os.system("systemctl disable can_decoder.service")
    os.remove(path_to_services)
    os.system("systemctl daemon-reload")