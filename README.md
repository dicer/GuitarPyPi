GuitarPyPi
==========

Play real music on your Guitar Hero(R)-controller connected to a RaspberryPi (that's the "Pi")!
The goal is to use the controller to play a predefined set of chords.

GuitarPyPi is written in Python (that's the "Py"), heavily relying on the pygames library.

The guitar sounds are stored as OGG files. By default there are 13 powercords (E to E8 in halftones) recorded 
with a distorted 1988 Fender Stratocaster. Every chord is sampled as open and muted. 
Feel free to use your own samples in WAV or OGG format. OGG is the preferred format as it seems to have a slightly lower latency.

How to play
-----------
The five colored buttons on the neck of the guitar are used to select the chord you want to play. 
Assuming no button pressed is also a state, there are six chords.

The selected chord is played when the trigger is pulled up or pushed down. You can change the chords while holding the trigger or even play all chords simultaneously (except for the no-button-chord of course).

To fulfill the need of different strumming styles (open and muted) the open chords are played when the trigger is pushed down
and the muted when pulled up.

The "back" and "start" buttons will be used to select different songs. Because there might be no display connected to your Pi, a sample is played back when the song is switched to know which song is active (not yet implemented).


Configuration (not yet implemented)
-----------------------------------
The configuration is done in an XML-file. There is a set of main properties for the application and a set of song-configurations
which contain the mapping of the buttons to samples.

The application config has following attributes:
- JoystickId: The joystick id of your guitar. In most cases it is 0 for /dev/input/js0. 
- For the following refer to http://www.pygame.org/docs/ref/mixer.html for detailed information.
	- SampleRate: The sample rate youre samples are recorded with. (defaults to 22050). It is highly reccomended to use 22050 Hz as samplerate. Works fine also with 44.1K samples but allowes a buffersize of 1 instead of 512. 
	- BitDepth: The bit depth youre samples are recorded with (defaults to -16)
	- Channels: The number of channels in your samples (1 = mono, 2 = stereo)
	- BufferSize: Number of samples sent to the OS at once. Lower number gives lower latency (the time between you trigger and hear the sound) but can lead to dropouts.
- ReadySound: a Sample that is played when the system is ready (usefull if you have no display)

A song configration has following attributes:
- MutedSounds: Path to OGG-files with the open samples for Button 0-5
- OpenSounds: Path to OGG-files with the muted samples for Button 0-5
- LoadSound: a Sound that is played when the song is selected

Of cource using open/muted sounds is not a dogma. It can also be used to have more different sounds in a song.

*Note:* at the moment there is only one hard coded song. 

Installation
------------
- Checkout the repository from github.com to ~/GuitarPyPi
- make sure you have the guitar connected and your OS recognizes it as a joystick.
	- ls /dev/input should list you 'js0'
	- dmesg |grep Guitar should show two lines, one listed as 'input'
	- jstest /dev/input/js0 should show you the changes of button states.
	- If not you need to install the xpad-module (driver). For linux 3.6.11+ you find it precompiled in /lib. In the very last part of /doc/HowToCompile_xmod_driver.txt you find instructions to install the module.
- go to ~/GuitarPyPi/src
- make sure the GuitarPyPi.py is executable
- run ./GuitarPyPi.py

Requirements
------------
For the RedOctane USB-controller youn need
- a RaspberryPi Model B (Model A untested)
- An SD-card with Raspbian (Kernel 3.6.11+) and installed xpad kernel module


Roadmap
-------
*Soon:*
- Configuration via XML
- Support of bluetooth controllers
- Create a "headless" raspbian installation, that automatically starts GuitarPyPi after boot.
- Configure a background track for each song for playing along

*Later:*
- A display connected to the Pi's GPIO
- Do something with the other buttons/tremolo
- ...


Useful information
------------------

If you need to get sample ogg files, you can use the following handy service:
http://speechutil.appspot.com/convert/ogg?file=1&text=ddddd
Or if it sounds funny use this and encode yourself:
http://speechutil.appspot.com/convert/wav?file=1&text=ddddd