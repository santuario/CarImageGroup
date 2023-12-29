import paramiko
import tarfile
import os
import sys

class SFTPDownloader:
    """
    Class to handle downloading and unpacking files from an SFTP server.

    Attributes:
    host : str
        Hostname of the SFTP server.
    port : int
        Port number for the SFTP connection.
    username : str
        Username for SFTP authentication.
    password : str
        Password for SFTP authentication.
    remote_file_path : str
        Path of the file on the SFTP server to download.
    local_directory : str
        Local directory to store the downloaded file.
    """

    def __init__(self, host, port, username, password, remote_file_path, local_directory):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.remote_file_path = remote_file_path
        self.local_directory = local_directory

    def download_and_unpack(self):
        """
        Connects to the SFTP server, downloads the specified file, and unpacks it.
        """
        try:
            # Establishing SFTP Connection
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Download file
            local_file_path = os.path.join(self.local_directory, "image_test.tar.gz")
            sftp.get(self.remote_file_path, local_file_path)
            sftp.close()
            transport.close()
            print("Download completed successfully.")

            # Unpack the tar.gz file
            with tarfile.open(local_file_path, "r:gz") as tar_ref:
                tar_ref.extractall(self.local_directory)
            print("Unpacking completed successfully.")

        except paramiko.SSHException as ssh_err:
            print(f"SSH error occurred: {ssh_err}")
        except FileNotFoundError as fnf_err:
            print(f"File not found error: {fnf_err}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Main script
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <remote_file_path> <local_directory>")
        sys.exit(1)

    # Replace these with environment variables or secure credential storage
    host = ""
    port = 22
    username = ""
    password = ""

    remote_file_path = sys.argv[1]
    local_directory = sys.argv[2]

    downloader = SFTPDownloader(host, port, username, password, remote_file_path, local_directory)
    downloader.download_and_unpack()
