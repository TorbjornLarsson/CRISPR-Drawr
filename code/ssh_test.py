# This Visual Studio Code test script was started before WSL2 and VirtualBox 
# routing problems were discovered.
# The imported suggestions had problems of their own, and scrap parts are
# mostly left in.

# Test extracting the DHCP address
import pynat
ip_info = pynat.get_ip_info()
print(ip_info)
print(ip_info[1])

import paramiko

#import time

ssh = paramiko.SSHClient() #SSHClient() is the paramiko object</n>

#Below lines adds the server key automatically to know_hosts file.use anyone one of the below

#ssh.load_system_host_keys() 

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#ssh.connect('130.229.141.158', port=2222, username='crispor', password='crispor')
ssh.connect(ip_info[1], port=2222, username='crispor', password='crispor')

#time.sleep(5)

#I have mentioned time because some servers or endpoint prints there own information after 
#loggin in e.g. the version, model and uptime information, so its better to give some time 
#before executing the command.

#Here we execute the command, stdin for input, stdout for output, stderr for error

#stdin, stdout, stderr = ssh.exec_command('xstatus Time')

#Here we are reading the lines from output.

#output = stdout.readlines() 

#print(output)

_stdin, _stdout,_stderr = ssh.exec_command("df")
print(_stdout.read().decode())

_stdin, _stdout, _stderr = ssh.exec_command('ls -al')
print(_stdout.read().decode())

ssh.close()

# import spur

# shell = spur.SshShell(hostname="localhost", port=2222, username="crispor", password="crispor")
# result = shell.run(["echo", "-n", "hello"])
# print(result.output) # prints hello


# import paramiko

# client = paramiko.client.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect('localhost', port=2222, username='crispor', password='crispor')
# _stdin, _stdout,_stderr = client.exec_command("df")
# print(_stdout.read().decode())
# client.close()


#import subprocess

#Python 2
#ssh crispor@localhost -p 2222

#retcode = subprocess.Popen("ssh {user}@{host} {cmd}".format(user='crispor', host='localhost', cmd='ls -l'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#print(retcode)

    # import paramiko
# ssh = paramiko.SSHClient()
# ssh.connect(hostname="127.0.0.1", port=2222, username="crispor", password="crispor", timeout=10)
# print(type(stdin))  # <class 'paramiko.channel.ChannelStdinFile'>
# print(type(stdout))  # <class 'paramiko.channel.ChannelFile'>
# print(type(stderr))  # <class 'paramiko.channel.ChannelStderrFile'>

# # Print output of command. Will wait for command to finish.
# print(f'STDOUT: {stdout.read().decode("utf8")}')
# print(f'STDERR: {stderr.read().decode("utf8")}')

# # Get return code from command (0 is default for success)
# print(f'Return code: {stdout.channel.recv_exit_status()}')

# # Because they are file objects, they need to be closed
# stdin.close()
# stdout.close()
# stderr.close()

# # Close the client itself
# client.close()

# output = stdout.readlines()

# for line in output:
#     print(line.rstrip())

# hostname = 'localhost'
# port = 2222

# username = 'crispor'
# password = 'crispor'

# cmd = 'uname'

# import paramiko
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('127.0.0.1', username='crispor', password='crispor',look_for_keys=False)

#with paramiko.SSHClient() as client:

#     client.load_system_host_keys()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    client.connect(hostname, port, username, password)

#     (stdin, stdout, stderr) = client.exec_command(cmd)

#     output = stdout.read()
#     print(str(output, 'utf8'))

#from paramiko import SSHClient

# Connect
client = paramiko.SSHClient()
#client.load_system_host_keys(None)
#client.set_missing_host_key_policy(None)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect('130.229.141.158', port=2222, username='crispor', password='crispor')
client.connect(ip_info[1], port=2222, username='crispor', password='crispor')

# Run a command (execute PHP interpreter)
_stdin, _stdout, _stderr = client.exec_command('ls')
print(type(_stdin))  # <class 'paramiko.channel.ChannelStdinFile'>
print(type(_stdout))  # <class 'paramiko.channel.ChannelFile'>
print(type(_stderr))  # <class 'paramiko.channel.ChannelStderrFile'>

# Print output of command. Will wait for command to finish.
print(f'STDOUT: {_stdout.read().decode("utf8")}')
print(f'STDERR: {_stderr.read().decode("utf8")}')

# Get return code from command (0 is default for success)
print(f'Return code: {_stdout.channel.recv_exit_status()}')

# Because they are file objects, they need to be closed
_stdin.close()
_stdout.close()
_stderr.close()

# Close the client itself
client.close()



