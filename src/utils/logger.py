"""로깅 유틸리티 - Singleton 패턴"""

import logging
import sys
from datetime import datetime
import pytz

# 한국 시간대 설정
KST = pytz.timezone('Asia/Seoul')


class ConsoleFormatter(logging.Formatter):
    """색상 포함 콘솔 포맷터"""
    
    COLORS = {
        logging.DEBUG: '\x1b[34;20m',      # 파랑
        logging.INFO: '\x1b[38;20m',       # 회색
        logging.WARNING: '\x1b[33;20m',    # 노랑
        logging.ERROR: '\x1b[31;20m',      # 빨강
        logging.CRITICAL: '\x1b[31;1m',    # 진빨강
    }
    RESET = '\x1b[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        # 한국 시간으로 변환
        ct = datetime.fromtimestamp(record.created, tz=KST)
        record.asctime = ct.strftime("%Y-%m-%d %H:%M:%S")
        
        # 색상 포맷
        color = self.COLORS.get(record.levelno, self.RESET)
        log_fmt = (
            f"{color}"
            f"[%(asctime)s] %(levelname)-8s >> %(filename)s : %(lineno)d - %(message)s"
            f"{self.RESET}"
        )
        
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LoggerManager:
    """Singleton: 로거 관리"""
    
    _instance = None
    
    def __init__(self):
        self.logger = self._create_logger()
    
    @staticmethod
    def get_instance():
        """싱글톤 인스턴스 반환"""
        if LoggerManager._instance is None:
            LoggerManager._instance = LoggerManager()
        return LoggerManager._instance
    
    def _create_logger(self) -> logging.Logger:
        """로거 생성"""
        logger = logging.getLogger("app")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        logger.handlers.clear()
        
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(ConsoleFormatter())
        logger.addHandler(handler)
        
        return logger
    
    def get_logger(self):
        """로거 반환"""
        return self.logger


# 싱글톤 인스턴스
logger = LoggerManager.get_instance().get_logger()

# 예외 처리 후킹
def _exception_hook(exc_type, exc_value, exc_traceback):
    if not issubclass(exc_type, KeyboardInterrupt):
        logger.critical(
            "Unexpected exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = _exception_hook
