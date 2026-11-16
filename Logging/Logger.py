import logging

logging.basicConfig(
    filename="ProjPSU.log",
    level=logging.ERROR,
    format="%(asctime)s -- %(levelname)s -- %(message)s",
    encoding="urf-8"
)

class Logger:
    @staticmethod
    def info(message: str) -> None:
        logging.info(message)

    @staticmethod
    def error(message: str) -> None:
        logging.error(message)
