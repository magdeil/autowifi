import json
from netmiko import ConnectHandler

with open('autoAP-jsn.json') as f:
    data = json.load(f)

conn = ConnectHandler(**data['aironetInfo'])
conn.enable()

output = conn.send_config_set([
    f"hostname {data['aironetConfig']['hostname']}",
    "default interface Dot11Radio0",
    "interface Dot11Radio0",
    "no shutdown",
    f"channel {data['aironetConfig']['channel']}",
    f"encryption mode ciphers {data['aironetConfig']['encr_mod']}",
    f"dot11 ssid {data['aironetConfig']['ssid']}",
    "authentication open",
    "guest-mode",
    "authentication key-management wpa",
    f"wpa-psk ascii {data['aironetConfig']['wifi_pass']}",
    "exit",
    "exit",
    "write memory"
])

print(output)
conn.disconnect()

with open('show_run_output.txt', 'w') as f:
    f.write(output)

print("\n✅ Configuration completed!")
