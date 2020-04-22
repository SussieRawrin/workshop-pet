"""

    # SQS notes

      • Any messages I get will be invisible for VisibilityTimeout (between 0 seconds and 12 hours)
      • Constantly ticking requests will have bad latency (do they have a limiter of the same window?)

      • long polling

        • WaitTimeSeconds (between 0 and 20, default 0)
        • this is best for good latency. Before, i had a ticker with a custom interval but it took a
          while to download in python. (Is there some limiter with the same window as VisibilityTimeout?)
        • it also reduces the number of empty requests. py will wait WaitTimeSeconds for a timeout.
          it's like sending a https request with a timeout of 20. (if there is no data, wait till there is)

        • note: if there are items available, it ill deliver x number of messages and quickly continue
          • MaxNumberOfMessages (between 1 and 10, default 1)
          • MaxNumberOfMessages won't always deliver x amount, but at least one
          • in this code i ask for as many messages as there are empty slots (_q max - _q length)
          • BEWARE make sure that it won't wait for MaxNum.. to be filled (it says it does on
            the docs but not when i tested it)


    # Coroutines vs Threads (Unity C#)
    # STUB https://support.unity3d.com/hc/en-us/articles/208707516-Why-should-I-use-Threads-instead-of-Coroutines-

      • Coroutines have nothing to do with Threads. Coroutine methods can be executed piece by piece
        over time, but all processes are still done by a single main Thread. If a Coroutine attempts
        to execute time-consuming operation, the whole application freezes for the time being.

      • Threads are different. The execution of separate Threads is managed by the operating
        system (this actually depends on the .NET implementation). If you have more than one
        logical CPU, many threads are executed on different CPUs. Thanks to that, any expensive
        operation will not freeze your game, but it might slow it down a little.

    # also notes
      > i deleted asyncio, async is only used in the automation bcuz this is on a new thread
      > move the python objects

"""

# native dependencies
import os, sys, re
from enum import Enum, auto

# Cloud Dependencies
import boto3

# package dependencies
from emoji import sad, happy
from timings import delay
# from pet import isQuit

# psudo threading
# note: not true threading because of python
from threading import Thread

# Additonal Dependencies
from termcolor import colored, cprint


# Queue Modes
class QueueMode(Enum):
    DEFAULT = auto(),
    SQS = auto(),


class QueueManager:

    __mode = QueueMode.DEFAULT
    _queue = []
    _max = 10

    # get the queue
    def getQueue(self):
        return self._queue

    # add an item
    def addCode(self, code):

        # Delete code if it's not in a format
        if not re.search("^[A-z0-9]{5}$", code):
            print(f'{ sad() }: received bad input { colored(code, "magenta") }')
            self.deleteCode(code)
            return

        # Add code to the queue (if not there)
        if code not in self._queue:
            self._queue.append(code)
    
    # delete a physical code
    def deleteCode(self, code):
        if code in self._queue:
            self._queue.remove(code)

    # gets next physical item
    def getNext(self):
        if self._queue:
            return self._queue[0]

    # is there any new items to download?
    # (network request here, ect..)
    def downloadNext(self):

        # if there is space in the queue
        if len(self._queue) < self._max:
            pass


class AwsQueueManager(QueueManager):

    # Modify web queue attributes (will modify the SQS config)
    __mode = QueueMode.SQS

    # Aws handles (key: code, value: handle)
    _queueItems = { }


    def __init__(self):

        # get SQS uri
        self._uri = os.getenv("queue_url")

        # Create SQS client
        sqs = boto3.resource("sqs",
            region_name=os.getenv("region"),
            aws_access_key_id=os.getenv("sqs_access_key_id"),
            aws_secret_access_key=os.getenv("sqs_secret_access_key"),
        )

        # pylint: disable=no-member
        self._awsQueue = sqs.Queue(self._uri)

        # if i wanted to write sqs config here i could do
        # STUB https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.set_attributes

        self.printRemaining()

    # get the next (possibly few) item(s)
    # stash them in pysical queue
    def downloadNext(self):

        # new message
        # these messages are not strictly in order

        # STUB AttributeNames=["ApproximateNumberOfMessages"]
        # > to get num of messages

        # how many pysical items can i fit?
        available = (self._max - len(self._queue))

        # if i can't fit any, quit
        if not available:
            return

        # download a few items that are waiting
        messages = self._awsQueue.receive_messages(
            QueueUrl=self._uri,

            # BEWARE review (is this needed for id ??)
            AttributeNames=["All"],

            # Queue attributes can also be set here
            # (this would not write sqs config)

            # try slightly longer than time to download a full queue
            VisibilityTimeout=40,

            # if broken, make sure long polling won't wait for max to fill
            MaxNumberOfMessages=available,

            # download timeout
            WaitTimeSeconds=20
        )

        # there may be multiple
        # (most likely on boot or under pressure)
        for item in messages:

            # if no new message
            if not item.body:
                return

            # grab code
            code = item.body.strip()
        
            # Add new codes to the queue
            if code not in self._queue:

                # Multiple handles may be sent, the newest one is the only one which will work
                # timeout is 20 seconds (on website)
                self._queueItems[code] = item

                self.addCode(code)

    # delete from physical and online queue
    def deleteCode(self, code):

        # delete from physical queue
        super().deleteCode(code)

        # get the newest handle
        item = self._queueItems.get(code)

        # now it opens another seperate thread to handle
        # quits mid-delete
        def __delete(self):

            # delete from online queue
            self._awsQueue.delete_messages(
                QueueUrl=self._uri,
                Entries=[{
                    "Id": item.message_id,
                    "ReceiptHandle": item.receipt_handle,
                }],
            )

        # new (not daemon) thread
        # will halt quit() without blocking
        Thread(target=__delete, args=(self,)).start()

    
    # WIP progress message
    def printRemaining(self):

        # queued = self._client.get_queue_attributes(
        #     QueueUrl=self._uri,
        #     AttributeNames=["ApproximateNumberOfMessages"],
        # ).get("Attributes").get("ApproximateNumberOfMessages")

        queued = self._awsQueue.attributes.get("ApproximateNumberOfMessages")

        print(colored(f'{ happy() }: { queued } items in SQS queue', "blue", attrs=["bold"]))
        print()
        

# queue process
def qdaemon(q: QueueManager):

    while True:

        # download the next item (data stream)
        q.downloadNext()


# boot queue
def bootQueue():

    mode = QueueMode.DEFAULT

    if (os.getenv("sqs_access_key_id") and os.getenv("sqs_secret_access_key") and os.getenv("queue_url")):
        mode = QueueMode.SQS

    print(f'{ happy() }: { colored("Queue booting in daemon thread", "blue") } ({ colored(mode.name, "magenta") }) queue')
    
    q = None

    if mode is QueueMode.DEFAULT:
        q = QueueManager()
    
    elif mode is QueueMode.SQS:
        q = AwsQueueManager()

    try:
        Thread(target=qdaemon, args=(q,), daemon=True).start()
        return q

    except Exception:
        raise