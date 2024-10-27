import pickle
import uuid

from config.logger import logger
from config.settings import META_INFO_FILE_PATH

from models import STATUS


def get_meta_info(unique_id: uuid.UUID) -> dict:
    try:
        with open(META_INFO_FILE_PATH, "rb") as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        logger.info(
            f"{unique_id} | meta_info file not found. Please check the file path: {META_INFO_FILE_PATH}."
        )
        with open(META_INFO_FILE_PATH, "wb") as file:
            pickle.dump({}, file)
        return {}
    except pickle.UnpicklingError as e:
        logger.info(f"{unique_id} | Error unpickling the file:\n{e}")
        raise


def rewrite_meta_info(unique_id: uuid.UUID, data: dict):
    try:
        with open(META_INFO_FILE_PATH, "wb") as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
    except OSError as e:
        logger.info(f"{unique_id} | Error writing to the file:\n{e}")


def set_in_progress(unique_id: uuid.UUID, data: dict):
    data["status"] = STATUS.IN_PROGRESS
    data["task_uuid"] = unique_id
    logger.info(f"{unique_id} STATUS.IN_PROGRESS")
    rewrite_meta_info(unique_id, data)


def set_finished(unique_id: uuid.UUID, data: dict):
    data["status"] = STATUS.FINISHED
    logger.info(f"{unique_id} STATUS.FINISHED")
    rewrite_meta_info(unique_id, data)


def set_failed(unique_id: uuid.UUID, data: dict):
    data["status"] = STATUS.FAILED
    logger.info(f"{unique_id} STATUS.FAILED")
    rewrite_meta_info(unique_id, data)
