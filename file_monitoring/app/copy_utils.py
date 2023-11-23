import subprocess

from config.logger import logger


def copy_files(file_names, local_dir, remote_dir, server_address, username):
    for fname in file_names:
        local_path = local_dir + fname
        remote_path = f"{username}@{server_address}:{remote_dir}"
        remote_path = f"{remote_dir}"  # Path to test
        copy_file_to_server_via_scp(local_path, remote_path)
        logger.info(f'File {fname} has been copied')
    logger.info(f'All files have been copied')


def copy_file_to_server_via_scp(local_path, remote_path):
    """
    Copy from local server to remote. 

    Input:
        - local_path (str) is something like '/home/sergiy/file'
        - remote_path (str) is something like 'root@losst.pro:/root/'
    """
    subprocess.run(["scp", local_path, remote_path])
