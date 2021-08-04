
import os
import re
import shutil

print("Configuring gps_measure app...")
path_to_app = "/etc/capsule/gps_measure"
path_to_log = "/var/log/capsule/gps_measure"
path_to_conf = "/etc/capsule/gps_measure/config.yaml"
path_to_conf = "/etc/capsule/gps_measure/config.yaml"
path_to_services = "/etc/systemd/system/gps_measure.service"
path_to_udev_rules = "/etc/udev/rules.d/gps-local.rules"
if not os.path.exists(path_to_app):
    print("Create folder", path_to_app)
    os.makedirs(path_to_app, 0o775)
    os.chown(path_to_app, 1000, 0) # Rudloff id and group Root
    os.chmod(path_to_app, 0o775) # Give all read access but Rudloff write access
if not os.path.exists(path_to_log):
    print("Create folder", path_to_log)
    os.makedirs(path_to_log, 0o644)
    os.chown(path_to_log, 1000, 0) # Rudloff id and group Root
    os.chmod(path_to_log, 0o775) # Give all read access but Rudloff write access
if not os.path.exists(path_to_conf):
    print("Create gps_measure configuration")
    shutil.copy2(os.path.join(os.path.dirname(__file__), "default_config.yaml"), path_to_conf)
    os.chown(path_to_conf, 1000, 0) # Rudloff id and group Root
    os.chmod(path_to_conf, 0o775) # Give all read access but Rudloff write access
if not os.path.exists(path_to_services):
    print("Create gps_measure service")
    shutil.copy2(os.path.join(os.path.dirname(__file__), "gps_measure.service"), path_to_services)
    os.chmod(path_to_services, 0o775) # Give all read access but Rudloff write access
    os.system("systemctl daemon-reload")
    os.system("systemctl enable gps_measure.service")
if not os.path.exists(path_to_udev_rules):
    print("Create udev rules")
    with open(path_to_udev_rules, "w") as f:
        f.write("SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"1546\", ATTRS{idProduct}==\"01a7\", SYMLINK+=\"gps_receiver\"\n")
else:
    print("Find devices in udev rules")
    with open(path_to_udev_rules, "r+") as f:
        # If we do not find the udev rules then create it
        if not re.search("ATTRS{idVendor}==\"1546\"", f.read()):
            print("Create udev rules")
            f.write("SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"1546\", ATTRS{idProduct}==\"01a7\", SYMLINK+=\"gps_receiver\"\n")
        else:
            print("Udev rule already created")
os.system("udevadm trigger")