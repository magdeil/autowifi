import yaml
from netmiko import ConnectHandler

with open('autoAP.yml') as f:
    data = yaml.safe_load(f)

device = data['aironetInfo']
config = data['aironetConfig']

conn = ConnectHandler(**device)
conn.enable()

commands = [
    f"hostname {config['hostname']}",
    "default interface Dot11Radio0",
    "default interface GigabitEthernet0",
    "interface Dot11Radio0",
    "no shutdown",
    f"channel {config['channel']}",
    f"encryption mode ciphers {config['encr_mod']}",
    f"dot11 ssid {config['ssid']}",
    "authentication open",
    "guest-mode",
    "authentication key-management wpa",
    f"wpa-psk ascii {config['wifi_pass']}",
    "exit",
    "exit",
    "write memory"
]

output = conn.send_config_set(commands)
print(output)
conn.disconnect()

with open('show_run_output.txt', 'w') as f:
    f.write(output)

print("\n✅ Configuration completed successfully!")
