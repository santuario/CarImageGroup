import paramiko
import tarfile
import os

# SFTP Connection Details
host = "stdatalabelling.blob.core.windows.net"
port = 22
username = "techchallenge@stdatalabelling"
password = "NICKUeWQuX+O815kMn8BIgcx5rDHJCNA"
remote_file_path = 'REMOTE_FILE'  # Update this with the exact path
local_directory = 'DIR'  # The directory where you want to store the dataset

# Function to download the dataset
def download_dataset():
    try:
        # Establishing SFTP Connection
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Download file
        local_file_path = os.path.join(local_directory, "image_test.tar.gz")
        sftp.get(remote_file_path, local_file_path)
        sftp.close()
        transport.close()
        print("Download completed successfully.")

        # Unpack the tar.gz file
        with tarfile.open(local_file_path, "r:gz") as tar_ref:
            tar_ref.extractall(local_directory)
        print("Unpacking completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the download function
download_dataset()
