# anime-downloader
This webcrawler can automatically download all ongoing anime(filters anime that you are watching), but this gonna take a few steps to setup

Pre-requisites:
  1- Python 3.0+
  2- IDM (Internet Download Manager)
  3- Chrome

What you'll need to do to setup:
  1- go to command prompt and write the following commands:
  "pip install selenium"
  "pip install idm"
  (without the ")
  2- download the version of chrome driver that your browser is compatible with (most probably the latest stable version, just google chrome driver and you'll be able to download    a  file called "chromedriver.exe") (you'll need to update this if a new version comes out and old version is not compatible anymore, but the program will tell you if it is        outdated)
  3- extract the rar and place the chromedriver in the same folder as Core.py.
  4- launch validAnimeDownload.py, it will tell you if you have missed a step or any other problem, if all is good, it will create a cache folder and say that the program as          created the required files
  5- go to the cache folder and open valid animes.txt, here you will list the anime that you are watching (go to animekisa.tv and copy the exact name as on the website)
  6- launch the validAnimesDownload.py and it will download the available episodes (by default it will download to "D:\Animes" in 720p, see below how to change that)

How to change its settings:
  open the validAnimesDownload.py using a text editor or ide and you will see some options (starting from line 22) that you can change, eg download location, resolution etc (there   will be comments explaining what the settings do)

  I'll probably make a video to further explain this but for now if anyone needs help im here

Disclaimer:
  this script is in beta version, i have tested and not found any major issues but there can be various bugs. if you find any tell me about it and ill see if i can fix it
