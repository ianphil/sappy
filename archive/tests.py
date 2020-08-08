import os.path
from Services.config import Config
from Services.logger import Logger

#### Services Tests ####

# Logger Service
TEST_LOG_FILENAME = "logs/tests.log"
logger = Logger(TEST_LOG_FILENAME, "TEST")
logger.log_info("From Tests.py")
if os.path.isfile(TEST_LOG_FILENAME):
    print("SERVICE:\t\t-Logger test \t\tPassed")
else:
    print("SERVICE:\t\t-Logger test \t\tFailed")

# Config Service
secrets = Config("secrets_example.json").get_secrets()

if secrets.documentdb_collection == "<col_name>":
    print("SERVICE:\t\t-Config test \t\tPassed")
else:
    print("SERVICE:\t\t-Config test \t\tFailed")
