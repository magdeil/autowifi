import json
from netmiko import ConnectHandler

with open('autoAP-jsn.json') as f:
    data = json.load(f)

device = data['aironetInfo']
config = data['aironetConfig']

conn = ConnectHandler(
    device_type=device['device_type'],
    host=device['host'],
    username=device['username'],
    password=device['password'],
    secret=device['secret']
)
conn.enable()

commands = [
    f"hostname {config['hostname']}",
    "default interface Dot11Radio0",
    "interface Dot11Radio0",
    "no shutdown",
    f"channel {config['channel']}",
    f"encryption mode ciphers {config['encr_mod']}",
    f"ssid {config['ssid']}",
    "authentication open",
    "guest-mode",
    "authentication key-management wpa",
    f"wpa-psk ascii {config['wifi_pass']}",
    "exit",
    "interface Dot11Radio0",
    f"ssid {config['ssid']}",
    "bridge-group 1",
    "exit",
    "interface Dot11Radio1",
    "shutdown",
    "exit",
    "dot11 network-map",
    "end",
    "write memory"
]

output = conn.send_config_set(commands)
print(output)
conn.disconnect()

with open('show_run_output.txt', 'w') as f:
    f.write(output)

print("\n✅ Configuration completed successfully!")
