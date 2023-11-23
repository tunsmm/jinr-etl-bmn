import os
import time

from config.logger import logger
from config.settings import REMOTE_SERVER, REMOTE_USER

from copy_utils import copy_files


# Путь к директории, которую нужно мониторить
directory_to_monitor = os.getcwd() + "/dir_to_monitor/"
directory_to_monitor = "/dir_to_monitor/"
# directory_to_monitor = "/opt/airflow/dir_to_monitor/"
if directory_to_monitor:
    os.makedirs(directory_to_monitor, exist_ok=True)


def detect_new_files(directory_to_monitor):
    file_set = set() 
    def get_new_files():
        nonlocal file_set
        current_files = set(os.listdir(directory_to_monitor))
        new_files = current_files - file_set
        file_set = current_files
        return new_files
    return get_new_files


# SLEEP_SECONDS = 3
# detecter = detect_new_files(directory_to_monitor)
# while True:
#     print('Start task...')
#     new_files = detecter()
    
#     if new_files:
#         logger.info(f"There are {len(new_files)} new files with names: {new_files}")
#         copy_files(
#             file_names=new_files,
#             local_dir=directory_to_monitor,
#             remote_dir=os.getcwd() + "/dir_to_copy/",  # TODO: it should be passed by .env
#             server_address=REMOTE_SERVER, 
#             username=REMOTE_USER,
#         )
#     else:
#         logger.info('There is no new files')

#     time.sleep(SLEEP_SECONDS)


detecter = detect_new_files(directory_to_monitor)
logger.info(f"directory_to_monitor is {directory_to_monitor}")
def monitoring_workflow():
    logger.info("Start run_monitoring_task")
    new_files = detecter()
    if new_files:
        logger.info(f"There are {len(new_files)} new files with names: {new_files}")
        copy_files(
            file_names=new_files,
            local_dir=directory_to_monitor,
            # remote_dir=os.getcwd() + "/dir_to_copy/",  # TODO: it should be passed by .env
            remote_dir="/dir_to_copy/",  # TODO: it should be passed by .env
            server_address=REMOTE_SERVER, 
            username=REMOTE_USER,
        )
        logger.info("Copying is finished")
    else:
        logger.info('There is no new files')
