
import os
import re
import shutil

print("Configuring can_decoder app...")
path_to_app = "/etc/capsule/can_decoder"
path_to_log = "/var/log/capsule"
path_to_conf = "/etc/capsule/can_decoder/config.yaml"
path_to_services = "/etc/systemd/system/can_decoder.service"
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
    print("Create can_decoder configuration")
    shutil.copy2(os.path.join(os.path.dirname(__file__), "default_config.yaml"), path_to_conf)
    os.chown(path_to_conf, 1000, 0) # Rudloff id and group Root
    os.chmod(path_to_conf, 0o775) # Give all read access but Rudloff write access
if not os.path.exists(path_to_services):
    print("Create can_decoder service")
    shutil.copy2(os.path.join(os.path.dirname(__file__), "can_decoder.service"), path_to_services)
    os.chmod(path_to_services, 0o644) # Give all read access but Rudloff write access
    os.system("systemctl daemon-reload")
    os.system("systemctl enable can_decoder.service")