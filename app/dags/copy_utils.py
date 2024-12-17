import os
import subprocess
import uuid
import zlib
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy.orm import Session

from config.logger import logger
from config.settings import NUMBER_OF_WORKERS_FOR_COPY_FILES
from db_utils import create_sa_engine_to_main_db, create_tables_in_db
from services.db_operations.file_copy_history import create_file_copy_history, update_file_copy_history

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
    
    # Получаем размер файла
    file_size = os.path.getsize(local_path)
    size_in_megabytes_binary = round(file_size / (1024 ** 2), 2)
    logger.info(f'{fname} file_size is {size_in_megabytes_binary} MB')

    # Calculate the checksum of the local file
    local_checksum = calculate_adler32(local_path)

    with create_sa_engine_to_main_db() as engine:
        with Session(engine) as session:
            # Создаем запись в истории копирования
            entry_id = create_file_copy_history(session, fname, file_size, str(local_checksum))

            for attempt in range(retries):
                copy_file_to_server_via_scp(local_path, remote_path)

                # Calculate the checksum of the remote file
                remote_checksum = calculate_adler32(remote_path)

                if local_checksum == remote_checksum:
                    logger.info(f"{unique_id} | File copied successfully: {fname} (Attempt {attempt + 1})")
                    # Обновляем запись в истории копирования
                    update_file_copy_history(session, entry_id, str(remote_checksum))
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
    subprocess.run(["xrdcp", local_path, remote_path])
