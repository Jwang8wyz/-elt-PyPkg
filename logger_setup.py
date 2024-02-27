import os
import logging
from datetime import datetime

class LoggerSetup:
    def __init__(self, app_name, log_level=logging.ERROR):
        self.app_name = app_name
        # Here, log_level is dynamically set based on the input parameter.
        self.log_level = log_level
        self.log_directory = self.create_log_directory()
        self.log_file_name = self.create_log_file_name()

    def create_log_directory(self):
        """Creates a directory for logs based on the current date."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        directory = f'/elt/logs/{self.app_name}/{current_date}'
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def create_log_file_name(self):
        """Generates a dynamic file name including the current date."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        return f'{self.log_directory}/{self.app_name}_DAILY_{current_date}.log'

    def configure_logging(self):
        """Configures logging to file and console with dynamic naming."""
        # Check if any handlers are already configured to avoid duplication
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(level=self.log_level,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                handlers=[logging.FileHandler(self.log_file_name),
                                          logging.StreamHandler()])
        else:
            # Clear existing handlers if reconfiguring
            logging.getLogger().handlers = []

            logging.basicConfig(level=self.log_level,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                handlers=[logging.FileHandler(self.log_file_name),
                                          logging.StreamHandler()])

# Example usage
# if __name__ == "__main__":
    # # Now you can pass the log level directly when creating an instance
    # logger_setup = LoggerSetup(app_name='jwang_app_log', log_level=logging.ERROR)
    # logger_setup.configure_logging()

    # # Now you can use logging as usual in your application
    # logging.error("This is a test error log.")