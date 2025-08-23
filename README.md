# ssh-logging
This is an SSH login tool I created from a python script.
Secure Logging more than ever is important in the modern day IT and cyber environment as remote work is more popular.
Any IT or Cybersecurity personel at some point will need to log in to a remote server, and without secure remote logging, their company systems and data are at risks of attacks.

## Purpose 
The tool assists professionals to access remote servers securely to perform their duties. 
The professional using this tool includes but not limited to DevOps/Cloud engineers, System admins.

## Requirements
- Python3 must be installed to run the tool
- A command-line interface(CLI)

## Usage
- Before running this tool, ensure you have manually logged in once to the target server (e.g., via ssh user@hostname).
- This ensures the server’s host key is added to your ~/.ssh/known_hosts file.”

From the command line, you run:
```bash
python3 ssh-logging.py --hostname <hostname> --username <username> --key <key> --command <command>
   ```

## Docker
I dockerised the tool for easy deployment and integration into CI/CD pipelines
This allows the tool to be readily available and makes it easy to use.
```bash
docker build -t ssh-logging .
docker run --rm ssh-logging --hostname <hostname> --username <username> --key <key> --command <command>

## Logging
The tool produces log files that are very important for tracking progress, debugging and troubleshooting

## Future improvements
I plan to improve the tool in future to include things like, 
- Add support for password-based SSH authentication(for legacy sytems that require a password for authentication)
- Improve error handling and logging with log rotation
- Add multi-server support
