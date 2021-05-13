from netmiko import ConnectHandler

device_ip = '10.0.15.108'
username = 'admin'
password = 'cisco'

device_params = {'device_type' : 'cisco_ios',
					'ip' : device_ip,
					'username' : username,
					'password' : password
				}

with ConnectHandler(**device_params) as ssh:
	print('Configuring device CSR1000v...')

	#Configure Loopback Interface
	ssh.send_config_from_file('Config_Loopback.txt')
	ssh.save_config()

	#Monitor interfaces
	print(ssh.send_command('sh ip int br'))
	