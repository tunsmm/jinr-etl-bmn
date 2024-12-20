from typing import Generator, List, Tuple, Optional
import datetime

from aiogram.types import InputFile, BufferedInputFile
from sqlalchemy.orm import Session

# from sys import path as syspath
# from os import path as ospath
# syspath.append(ospath.join(ospath.dirname(ospath.realpath(__file__)),'..','dags'))

from models.db import FileCopyHistory
from services.db_operations.file_copy_history import (
    filter_file_copy_history_between_dates, 
    filter_not_copied_files,
)
from db_utils import create_sa_engine_to_main_db, create_tables_in_db

create_tables_in_db()

def get_filter_file_copy_history(filtered_entries: List[FileCopyHistory]) -> Tuple[Optional[str], Optional[int]]:
    filtered_entries = filter_file_copy_history_between_dates()
    file_names = [entry.file_name for entry in filtered_entries]
    completed_count = sum(1 for entry in filtered_entries if entry.copy_ended_at is not None)
    message = f"{file_names} + {completed_count}"
    file = None
    return message, file


class StatsFlow:
    def __init__(self):
        self.start_datetime_filter = datetime.datetime.now()
        self.end_datetime_filter = None
        self.last_datetime_get_not_copied_files = None

    def get_filter_file_copy_history(self) -> Tuple[Optional[str], Optional[InputFile]]:
        self.end_datetime_filter = datetime.datetime.now()
        with create_sa_engine_to_main_db() as engine:
            with Session(engine) as session:
                filtered_entries = filter_file_copy_history_between_dates(
                    session,
                    "copy_ended_at",
                    self.start_datetime_filter,
                    self.end_datetime_filter,
                )

        if not filtered_entries:
            return None, None

        file_names = "\n".join([entry.file_name for entry in filtered_entries])
        completed_count = sum(1 for entry in filtered_entries if entry.copy_ended_at is not None)
        message = f"There are {completed_count} files copied.\nFilenames in .txt file below."
        
        # Кодируем строку в байты и создаем класс для передачи файла
        file_names_bytes = file_names.encode('utf-8')
        buffered_file = BufferedInputFile(file=file_names_bytes, filename='file_names.txt')

        self.start_datetime_filter = self.end_datetime_filter
        
        return message, buffered_file
    
    def get_not_copied_files(self) -> Tuple[Optional[str], Optional[InputFile]]:
        if (
            self.last_datetime_get_not_copied_files and 
            self.last_datetime_get_not_copied_files < datetime.datetime.now() - datetime.timedelta(seconds=1)
        ):
            self.last_datetime_get_not_copied_files = datetime.datetime.now()
        else:
            return None, None

        with create_sa_engine_to_main_db() as engine:
            with Session(engine) as session:
                filtered_entries = filter_not_copied_files(
                    session,
                    self.last_datetime_get_not_copied_files - datetime.timedelta(seconds=1),
                )

        if not filtered_entries:
            return None, None

        file_names = "\n".join([entry.file_name for entry in filtered_entries])
        completed_count = sum(1 for entry in filtered_entries if entry.copy_ended_at is not None)
        message = f"There are {completed_count} files that still are not copied.\nFilenames in .txt file below."
        
        # Кодируем строку в байты и создаем класс для передачи файла
        file_names_bytes = file_names.encode('utf-8')
        buffered_file = BufferedInputFile(file=file_names_bytes, filename='file_names.txt')
        
        return message, buffered_file
    
    def execute_pipeline_methods(self) -> Generator:
        """Вызывает все методы получения истории копирования файлов"""
        yield self.get_filter_file_copy_history
        yield self.get_not_copied_files
