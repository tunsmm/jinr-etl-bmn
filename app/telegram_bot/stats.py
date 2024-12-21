from typing import Generator, Tuple, Optional
import datetime

from aiogram.types import InputFile, BufferedInputFile
from sqlalchemy.orm import Session

from config.logger import logger
from services.db_operations.file_copy_history import (
    filter_file_copy_history_between_dates, 
    filter_not_copied_files,
)
from db_utils import create_sa_engine_to_main_db, create_tables_in_db

create_tables_in_db()


class StatsFlow:
    def __init__(self):
        self.start_datetime_filter = datetime.datetime.now()
        self.end_datetime_filter = None
        logger.info(f'StatsFlow is started with start_datetime_filter = {self.start_datetime_filter}')

    def get_filter_file_copy_history(self) -> Tuple[Optional[str], Optional[InputFile]]:
        self.end_datetime_filter = datetime.datetime.now()
        with create_sa_engine_to_main_db() as engine:
            with Session(engine) as session:
                logger.info(f'get_filter_file_copy_history | {self.start_datetime_filter} - {self.end_datetime_filter}')
                filtered_entries = filter_file_copy_history_between_dates(
                    session,
                    "copy_ended_at",
                    self.start_datetime_filter,
                    self.end_datetime_filter,
                )

        if not filtered_entries:
            logger.info('get_filter_file_copy_history | no filtered_entries')
            return None, None

        file_names = "\n".join([entry.file_name for entry in filtered_entries])
        completed_count = sum(1 for entry in filtered_entries if entry.copy_ended_at is not None)
        message = f"There are {completed_count} files copied.\nFilenames in .txt file below."
        logger.info(f'get_filter_file_copy_history | message is {message}')
        
        # Encode the string to bytes and create a class to transfer as a file
        file_names_bytes = file_names.encode('utf-8')
        buffered_file = BufferedInputFile(file=file_names_bytes, filename='file_names.txt')

        self.start_datetime_filter = self.end_datetime_filter
        
        return message, buffered_file
    
    def get_not_copied_files(self) -> Tuple[Optional[str], Optional[InputFile]]:
        threshold_date = datetime.datetime.now() - datetime.timedelta(hours=1)
        with create_sa_engine_to_main_db() as engine:
            with Session(engine) as session:
                filtered_entries = filter_not_copied_files(
                    session,
                    threshold_date,
                )

        if not filtered_entries:
            logger.info(f'get_not_copied_files | All files above {threshold_date} are copied')
            return None, None

        file_names = "\n".join([entry.file_name for entry in filtered_entries])
        message = f"There are {len(filtered_entries)} files that still are not copied."
        
        # Encode the string to bytes and create a class to transfer as a file
        file_names_bytes = file_names.encode('utf-8')
        buffered_file = BufferedInputFile(file=file_names_bytes, filename='file_names.txt')
        
        return message, buffered_file
    
    def execute_pipeline_methods(self) -> Generator:
        """Call all methods to retrieve file copy history"""
        # yield self.get_filter_file_copy_history
        yield self.get_not_copied_files
