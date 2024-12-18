from datetime import datetime
from typing import List, Tuple

from sqlalchemy.orm import Session

from models.db import FileCopyHistory


def create_file_copy_history(session: Session, file_name: str, file_size: int, file_hash_before: str):
    """Создание новой записи в истории копирования файлов."""
    history_entry = FileCopyHistory(
        file_name=file_name,
        file_size=file_size,
        file_hash_before=file_hash_before,
        copy_started_at=datetime.now()
    )
    session.add(history_entry)
    session.commit()
    return history_entry.id  # Возвращаем ID созданной записи


def update_file_copy_history(session: Session, entry_id: int, file_hash_after: str):
    """Обновление записи в истории копирования файлов."""
    history_entry = session.query(FileCopyHistory).filter(FileCopyHistory.id == entry_id).first()
    if history_entry:
        history_entry.file_hash_after = file_hash_after
        history_entry.copy_ended_at = datetime.now()
        session.commit()


def filter_file_copy_history_between_dates(
    session: Session,
    field_name: str,
    start_date: datetime = None,
    end_date: datetime = None,
) -> List[FileCopyHistory]:
    """Фильтрует записи в интервале дат по указанному полю."""
    field = getattr(FileCopyHistory, field_name, None)

    if field is None:
        raise ValueError(f"Field '{field_name}' does not exist in the FileCopyHistory model.")
    
    match (start_date, end_date):
        case (None, None):
            raise ValueError("Both dates cannot be None.")
        case (None, _):
            return session.query(FileCopyHistory).filter(field <= end_date).all()
        case (_, None):
            return session.query(FileCopyHistory).filter(field >= start_date).all()
        case (_, _):
            return session.query(FileCopyHistory).filter(field.between(start_date, end_date)).all()
