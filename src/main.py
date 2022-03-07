
# Local
from api_handler import ApiHandler
from logger import Logger

def main() -> None:
    logger = Logger("Main")
    logger.verbose("Starting application...")
    api = ApiHandler()


if __name__ == "__main__":
    main()