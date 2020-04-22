

<div align="center" style="padding: 20px; text-align: center">
	<img src="https://archive.workshopcodes.com/jetpack-jumbo.png" />
</div>

<div align="center">
<br />
<small>Not affiliated with Blizzard Entertainment<sup>®</sup> or Overwatch<sup>®</sup></small>
<br />
<small>please <a target="_blank" href="https://www.linkedin.com/in/russell-sorin/">hire me</a> blizzard >:( </small>
</div>

### What is Workshop Pet?

- Workshop Pet is a program that allows you to download and save multiple workshop files very quickly by automating in-game input. You can choose to either download the program and save files manually or to add them to the [online archive](https://archive.workshopcodes.com/)

* It powers [archive.workshopcodes.com](http://archive.worshopcodes.com/) which is an archival microservice for [workshopcodes.com](https://workshopcodes.com/). If you are just worried about saving your workshop codes, you can import them on that site and they will be saved to the archive too

	* An example is available here @ https://archive.workshopcodes.com/GC26Y
	* If ya want any help please join the discord @  https://discord.gg/Rju6xv9

### What's the point?
* A few workshop creators I'm friends with were concerned with the possibility of their games being deleted, I made this code archiver to help. It allows you to download all your workshop games quickly to your PC and lets you rest easy knowing they are backed up

* Powers the [workshop archive](https://archive.workshopcodes.com/) which is an online version


```
If you would like to help maintain the online version and..
  a. Have a PC that can play overwatch at at 20 fps or more
  b. Don't mind running PET when you're not using it

You can arm PET in CAT mode (Code Archive Tranceiver) which directly updates the online archive with any
codes waiting to be saved. If you want to do this please join our discord (above) and ask about it
```

# How can I download my workshop games?

* If you are worried about your games, in most cases you can just import them in our discord (above) with a command ex. `!archive GC26Y, AX9GA` and the bot will add it to the [online archive](https://archive.workshopcodes.com/). If you need to save many files to PC, you can run this program on your computer

	1. Actually downloading and running PET is not the best option for most people


##### BEWARE
* DOWNLOADING THIS PROGRAM IS NOT THE BEST OPTION CURRENTLY - I'm working on making an actual interface, unless you want to edit the python code please use the online archive or wait for the next update




------------
------------


### Python Jargon

I wrote this program using python. It's the first intermediate project I've coded with python so please let me know how any of the code I wrote could be improved. I'd love to incorperate best python practices because I've mostly just been googling syntax as of now

I want to make this a GUI program (so people can have a better time), if anyone can give advice that that would be awesome :)

### Features:

* #### Multithreading

	* I had to incorperate multithreading because when working in CAT mode as an AWS microservice, it turns out the python API for the AWS is thread blocking which is not something I expected coming in to python after working with asyncronous javascript for most of my back ends
	
	* There are 2 main threads with 2 temporary threads that handle just the critical thread blocking operations (Deleting items in the queue and Archiving items)
		1. Main thread handles automation and the general functions
		2. Queue thread just handles recieving items from the queue and updating the queue so that the automation can perform the download tasks

* #### Performance

	* Automation timings are adjustable in the python code, as of now the only major performance bottlenecks are network delays from the overwatch client which can't be helped. I incorperated multithreading to reduce the CAT mode timings from about 9 seconds per item to 4 seconds. Default file IO is 4 seconds per item.

	* If armed in CAT mode (online archiver), PET will use SQS to manage the queue which is quick and minimizes any tight coupling that would have occured with a RabbitMQ VPS and any monolithic message queue. Due to this, PET can have multiple instances at the same time with no interference 
		1. AWS is great but I'm not necessarily supportive of Amazon as a company
		2. A goal of this project was to learn python microservices which is why I chose AWS and python
    
  * [workshop archive](https://archive.workshopcodes.com/) is delivered via a cloudfront distribution (similar to playoverwatch.com) which allows quick access to codes

#### Assumptions

* Overwatch is starting in windowed mode and can handle 20 fps
* No keyboard input is sent during automation process

#### pip packages

* pyautogui
* pygetwindow
* pyperclip
* python-dotenv
* termcolor
* requests
* boto3
