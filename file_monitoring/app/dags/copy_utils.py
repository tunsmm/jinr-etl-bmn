import os
import subprocess
import uuid
import zlib
from concurrent.futures import ThreadPoolExecutor

from config.logger import logger
from config.settings import NUMBER_OF_WORKERS_FOR_COPY_FILES

from db_utils import create_tables_in_db

create_tables_in_db()


def make_remote_path(
    unique_id: uuid.UUID, remote_dir: str, server_address: str, username: str
):
    remote_path = f"{username}@{server_address}:{remote_dir}"
    remote_path = f"{remote_dir}"  # Path to test
    logger.info(f"{unique_id} | remote_path is {remote_path}")
    return remote_path


def calculate_adler32(file_path: str) -> int:
    """Calculate the Adler-32 checksum of a file."""
    with open(file_path, 'rb') as f:
        return zlib.adler32(f.read()) & 0xffffffff


def copy_files(
    unique_id: uuid.UUID,
    file_names: list[str],
    local_dir: str,
    remote_dir: str,
    server_address: str,
    username: str,
):
    remote_path = make_remote_path(
        unique_id=unique_id,
        remote_dir=remote_dir,
        server_address=server_address,
        username=username,
    )
    with ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS_FOR_COPY_FILES) as executor:
        futures = []
        for fname in file_names:
            future = executor.submit(copy_file, unique_id, local_dir, remote_path, fname)
            futures.append(future)

        for future in futures:
            result = future.result()

    logger.info(f"{unique_id} | All files have been copied.")


def copy_file(unique_id: uuid.UUID, local_dir: str, remote_path: str, fname: str, retries: int = 3):
    local_path = os.path.join(local_dir, fname)
    remote_path = os.path.join(remote_path, fname)
    
    # Calculate the checksum of the local file
    local_checksum = calculate_adler32(local_path)
    
    for attempt in range(retries):
        copy_file_to_server_via_scp(local_path, remote_path)
        
        # Calculate the checksum of the remote file
        # Здесь предполагается, что возможно получить доступ к файлу с текущего сервера
        remote_checksum = calculate_adler32(remote_path)

        if local_checksum == remote_checksum:
            logger.info(f"{unique_id} | File copied successfully: {fname} (Attempt {attempt + 1})")
            return fname
        logger.info(f"Checksum mismatch for {fname} (Attempt {attempt + 1}). Retrying...")
    
    raise Exception(f"Failed to copy file {fname} after {retries} attempts.")


def copy_file_to_server_via_scp(local_path: str, remote_path: str):
    """
    Copy from local server to remote.

    Input:
        - local_path (str) is something like '/home/sergiy/file'
        - remote_path (str) is something like 'root@losst.pro:/root/'
    """
    subprocess.run(["scp", local_path, remote_path])
