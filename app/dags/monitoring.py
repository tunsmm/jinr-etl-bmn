from datetime import datetime
import asyncio
import os
import time
import uuid

from airflow.models import Variable
from sqlalchemy.orm import Session

from config.logger import logger
from config.settings import (
    DIRECTORY_TO_MONITOR,
    REMOTE_DIRECTORY,
    REMOTE_SERVER,
    REMOTE_USER,
)
from copy_utils import copy_files
from db_utils import create_sa_engine_to_main_db, create_tables_in_db
from meta_info_utils import (
    get_meta_info,
    rewrite_meta_info,
    set_failed,
    set_finished,
    set_in_progress,
)
from models import STATUS, TelegramBot
from services.db_operations.file_copy_history import filter_file_copy_history_between_dates


def detect_new_files(meta_info: dict):
    old_files = meta_info.get("existed_files", set())
    current_files = set(os.listdir(DIRECTORY_TO_MONITOR))
    new_files = current_files - old_files
    return new_files


def process_transferring(is_new_files: bool):
    is_transferring = Variable.get("is_transferring", default_var=False)
    def send_tg_bot_message(text):
        TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'no_token')
        tg_bot = TelegramBot(TOKEN)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tg_bot.send_message_to_all(text=text))

    def get_files_count(start_time: float, end_time: float) -> int:
        create_tables_in_db()
        with create_sa_engine_to_main_db() as engine:
            with Session(engine) as session:
                filtered_entries = filter_file_copy_history_between_dates(
                    session,
                    "copy_ended_at",
                    datetime.fromtimestamp(start_time),
                    datetime.fromtimestamp(end_time),
                )
        if not filtered_entries:
            logger.info('get_filter_file_copy_history | no filtered_entries')
            return 0
        return sum(1 for entry in filtered_entries if entry.copy_ended_at is not None) or 0

    if is_new_files and not is_transferring:
        Variable.set(
            "is_transferring",
            True,
            "Flag to indicate whether is copying of files started."
        )
        start_time = time.time()
        Variable.set("start_time", start_time, "Time where copying of files has started.")
        send_tg_bot_message(text=f"Передача файлов начата в {start_time} от директории Х в Y")
    elif not is_new_files and is_transferring:  
        start_time = Variable.get("start_time", None)
        if start_time and time.time() > 3600:
            Variable.set(
                "is_transferring",
                False,
                "Flag to indicate whether is copying of files started."
            )
            files_count = get_files_count(start_time, time.time())
            send_tg_bot_message(
                text=f"Передача файлов завершена в {time.time()}. Передано {files_count} файлов."
            )


def monitoring_workflow():
    unique_id = uuid.uuid1()
    logger.info(f"{unique_id} | Start monitoring_workflow")

    try:
        meta_info = get_meta_info(unique_id)
        if meta_info.get("status") == STATUS.IN_PROGRESS:
            logger.info(f"{unique_id} | monitoring_workflow is already in progress. Exit.")
            return
        set_in_progress(unique_id, meta_info)

        new_files = detect_new_files(meta_info)
        if new_files:
            logger.info(f"{unique_id} | There are {len(new_files)} new files with names: {new_files}")
            process_transferring(is_new_files=True)
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
            logger.info(f"{unique_id} | Copying is finished.")
        else:
            logger.info(f"{unique_id} | There is no new files")
            process_transferring(is_new_files=False)

    except Exception as e:
        logger.info(f"{unique_id} | Error in monitoring_workflow {e}")
        set_failed(unique_id, meta_info)
    else:
        set_finished(unique_id, meta_info)
