
delay = {

    # delay for switching between UI "pages"
    # only in places where a delay of 0 didn't work
    "animation": .4,

    # the delay from when overwatch is opened to the sign in box
    # also the delay from sign in to welcome page
    # most of the delay is due to network conditions
    "overwatch": 9,

    # time from hitting the "Create Game" button to having an interface again
    "ow_lobby": .9,
    "download": 2,

    # if the queue is empty, 
    # "queue_wait": .9,

    # other values
    
    # typing speed
    # too fast can mess up text (.0009 fails approx one in twenty attempts)
    "typing": .009,
    
    # polling interval for application window
    # interval for Save File queue
    "interval": .2,
}