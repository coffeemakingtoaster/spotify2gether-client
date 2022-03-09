from coffeelog import BaseLogger
 

# Local
from api_handler import ApiHandler
from user_interface import Client

def main() -> None:
    logger = BaseLogger('Main')
    logger.verbose("Starting application...")
    # Generate API handler
    api = ApiHandler()
    
    # Start UI
    client = Client(api)
    client.start()


if __name__ == "__main__":
    main()