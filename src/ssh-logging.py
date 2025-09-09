import paramiko
import argparse
import logging
import os
from pathlib import Path

log_file = Path(__file__).with_name('secure_ssh.log')

# i configure logging because i want the script to generate logs
logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s-%(levelname)s-%(message)s'
        )

def linux_server_secure_logging(hostname, username, command, key):
    ssh_client = paramiko.SSHClient() # ssh client
    try:
        ssh_client.set_missing_host_key_policy(paramiko.RejectPolicy()) # adding host key policy, AutoReject=Secure
        ssh_client.load_system_host_keys() # checking known host list

        # connecting to the server via ssh
        ssh_client.connect(
                hostname=hostname,
                username=username,
                key_filename=key
                )

        print('Connected securely using existing credentials')
        logging.info('Connected securely using existing credentials')

        # executing commands after logging in the server
        stdin,stdout, stderr = ssh_client.exec_command(command)
        print(f'Executing command {command}')
        logging.info(f'Executing command {command}')

        output = stdout.read().decode()
        error =  stderr.read().decode()
        
        print(f'stdout: {output}')
        logging.info(f'stdout: {output}')
        
        if error.strip(): # to avoid logging blank spaces , we are only going to log errors if there any errors.
            print(f'stderr: {error}')
            logging.error(f'stderr: {error}')

    except Exception as e:
       print(f'Error: {e}')
       logging.error(f'Error: {e}')

    finally:
       ssh_client.close()

def get_secrets():
    try:
        db_user = Path('/run/secrets/postgres_user').read_text().strip()
        db_password = Path('/run/secrets/postgres_password').read_text().strip()
        db_name = Path('/run/secrets/postgres_name').read_text().strip()

        return {
                "db_user": db_user,
                "db_password": db_passwdord,
                "db_name": db_name
                }
    except FileNotFoundError as e:
        print(f'Missing secrets file: {e}')
        logging.error('Missing secrets file: {e}')
    except Exception as e:
        print(f'Error reading secrets: {e}')
        logging.error(f'Error reading secrets: {e}')

def main():
    parser = argparse.ArgumentParser(description='logging securely into a server using ssh')
    parser.add_argument('--hostname', type=str, required=True, help='target server ip address')
    parser.add_argument('--username', type=str, required=True, help='target server username')
    parser.add_argument('--command', default='ls -la', help='command you want to run')
    parser.add_argument('--key', type=str, default=os.path.expanduser("~/.ssh/id_rsa"), help='path to private key')
    args = parser.parse_args()

    linux_server_secure_logging(args.hostname, args.username, args.command, args.key)
    get_secrets()

if __name__ == '__main__':
    main()
