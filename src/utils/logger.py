import logging
import sys
import os
import json
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any
from src.core.config import settings

class KSTFormatter(logging.Formatter):
    """Formatter that converts timestamps to KST."""
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp, tz=ZoneInfo("UTC"))
        return dt.astimezone(ZoneInfo("Asia/Seoul"))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

class LoggerManager:
    _instance = None
    _lock = threading.Lock()
    _logger = None

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def __init__(self):
        if LoggerManager._instance is not None:
            raise Exception("This class is a singleton!")
        self._initialize_logger()

    def _initialize_logger(self):
        self._logger = logging.getLogger("LLM_Project_Module")
        self._logger.setLevel(logging.INFO)
        
        # Prevent adding handlers multiple times
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = KSTFormatter(
                fmt='[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        
        # Ensure log directory exists for file logs (cost/api)
        os.makedirs(os.path.dirname(settings.COST_LOG_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(settings.API_REQUEST_LOG_PATH), exist_ok=True)
        
        # Global Exception Hook
        sys.excepthook = self.handle_exception

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self._logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    def get_logger(self):
        return self._logger

    def _write_jsonl(self, file_path: str, data: Dict[str, Any]):
        """Internal helper for writing structured logs"""
        with self._lock:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def log_cost(self, data: Dict[str, Any]):
        self._write_jsonl(settings.COST_LOG_PATH, data)

    def log_api_request(self, data: Dict[str, Any]):
        self._write_jsonl(settings.API_REQUEST_LOG_PATH, data)

# Convenience instance
logger_manager = LoggerManager.get_instance()
logger = logger_manager.get_logger()

