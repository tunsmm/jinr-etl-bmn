import os
import uuid

from config.logger import logger
from config.settings import (
    DIRECTORY_TO_MONITOR,
    REMOTE_DIRECTORY,
    REMOTE_SERVER,
    REMOTE_USER,
)

from copy_utils import copy_files
from meta_info_utils import (
    get_meta_info,
    rewrite_meta_info,
    set_failed,
    set_finished,
    set_in_progress,
)
from models import STATUS


def detect_new_files(meta_info: dict, directory_to_monitor: str):
    old_files = meta_info.get("existed_files", set())
    current_files = set(os.listdir(directory_to_monitor))
    new_files = current_files - old_files
    return new_files


def monitoring_workflow():
    unique_id = uuid.uuid1()
    logger.info(f"{unique_id} | Start monitoring_workflow")

    try:
        meta_info = get_meta_info(unique_id)
        if meta_info.get("status") == STATUS.IN_PROGRESS:
            logger.info(f"{unique_id} | monitoring_workflow is already in progress")
            return
        set_in_progress(unique_id, meta_info)

        new_files = detect_new_files(meta_info, DIRECTORY_TO_MONITOR)
        if new_files:
            logger.info(
                f"{unique_id} | There are {len(new_files)} new files with names: {new_files}"
            )
            copy_files(
                unique_id=unique_id,
                file_names=new_files,
                local_dir=DIRECTORY_TO_MONITOR,
                remote_dir=REMOTE_DIRECTORY,
                server_address=REMOTE_SERVER,
                username=REMOTE_USER,
            )
            meta_info["existed_files"] = meta_info.get("existed_files", set()) | new_files
            rewrite_meta_info(unique_id, meta_info)
            logger.info(f"{unique_id} | Copying is finished")
        else:
            logger.info(f"{unique_id} | There is no new files")
    except Exception as e:
        logger.info(f"{unique_id} | Error in monitoring_workflow {e}")
        set_failed(unique_id, meta_info)
    else:
        set_finished(unique_id, meta_info)
