"""

    note
      
      without prefix it's slightly slower (.2 to .5) but it is 0 for in memory already downloadeds
      with prefix it's slightly faster (0 to .4) without that

"""


# Native Dependencies
import os, time
from enum import Enum, auto

# Cloud Dependencies
import boto3, requests
from botocore.exceptions import ClientError, ConnectionError

# Additional Dependencies
from termcolor import colored

# package dependencies
from emoji import sad, happy

# BEWARE
import dotenv

class DataMode(Enum):

    DEFAULT = auto()
    S3 = auto()


# Save File
class DataManager():

    __prefix = "archive" + os.path.sep
    __suffix = ".ow"

    def __init__(self):

        self._path = self.__prefix

    
    # generates a file path
    def __make_path(self, code):

        return self.__prefix + code.upper() + self.__suffix


    # Will halt (that's ok)
    def doesExist(self, code):

        return os.path.exists(self.__make_path(code))


    # This will halt process if not threaded
    def addToArchive(self, code, text):

        with open(self.__make_path(code), 'w', encoding="utf8") as f:

            f.write(text)


# Download File
class AwsDataManager(DataManager):

    def __init__(self):

        self._s3 = boto3.resource(
            "s3",
            aws_access_key_id=os.getenv("s3_access_key_id"),
            aws_secret_access_key=os.getenv("s3_secret_access_key"),
        )

        # pylint: disable=no-member
        self._bucket = self._s3.Bucket(os.getenv("bucket_name"))

        self._optional_head_cache_prefix_uri = os.getenv("optional_head_cache_prefix_uri")

    
    # Does this code exist online?
    def doesExist(self, code):

        try:
            
            # if a cache prefix is written ("https://dx0uqf7sdkb0g.cloudfront.net/" { VCC9V })
            # it might help with network delay
            if self._optional_head_cache_prefix_uri:

                # HEAD item in cache
                q = requests.head(
                    self._optional_head_cache_prefix_uri + code.upper(),
                    timeout=4
                )

                q.raise_for_status()


            # if no cache prefix is written
            # HEAD item in bukkit
            else:

                # pylint: disable=no-member
                self._s3.Object(self._bucket.name, code.upper()).load()


        # if it's a 400 and 500 level error (with cache)
        except requests.exceptions.HTTPError:
            return False

        # if it's a 400 level error (no cache)
        except ClientError:
            return False

        # network errors (with cache)
        except requests.exceptions.ConnectionError:
            print(f'{ sad() }: { colored("failed to connect", "red") }')
            return False

        # network errors (no cache)
        except ConnectionError:
            print(f'{ sad() }: { colored("failed to connect", "red") }')
            return False

        # no errors
        return True


    # This will halt process if not threaded
    def addToArchive(self, code, text):

        self._bucket.put_object(
            Key=code.upper(),
            Body=text,
            ContentType="text/plain; charset=utf-8",

            # default age is 24 hours (180000 is 2 days, 1209600 is 2 weeks)
            # this won't be updated on cloudfront until time expires
            # test with incognito and "ipconfig /flushdns"
            # CacheControl="max-age=1209600"
        )


# Boot Archiver
def bootArchive():

    __mode = DataMode.DEFAULT
    __cache_mode = "NO"

    if os.getenv("s3_access_key_id") and os.getenv("s3_secret_access_key") and os.getenv("bucket_name"):
        __mode = DataMode.S3

        if os.getenv("optional_head_cache_prefix_uri"):
            __cache_mode = "PREFIX"

    print(f'{ happy() }: { colored("Archive booting", "green") } ({ colored(__mode.name, "magenta") } archive, { colored(__cache_mode, "magenta") } cache)')

    if __mode is DataMode.DEFAULT:
        return DataManager()

    elif __mode is DataMode.S3:
        return AwsDataManager()


