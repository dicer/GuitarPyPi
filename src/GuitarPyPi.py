#!/usr/bin/python
import pygame
import sys
import Config
from pprint import pprint
from pygame.locals import *
from Config import InputEvent

NO_BUTTON_CHORD = 0

def main():
    global inputDriver, chordsOpen, chordsMuted, chordsToPlay, playing, playOpen, songs, currentSong

    print "Initialization start..."

    # We need to reduce the default buffer size to have low latency.
    # It is highly reccomended to use 22050 Hz as samplerate. Works fine also with 44.1K samples
    # but allowes a buffersize of 1 instead of 512 which means approx. 10ms instead of 50 ms latency!
    pygame.mixer.pre_init(22050,-16,1,1)
    pygame.init()
 #   pygame.display.quit()

    # load config
    config = Config.Config()
    config.loadSongConfig()

    songs = config.getSongs()
    pprint(songs)
    
    inputDriver = config.inputDriver

    # init status
    currentSong = 0
    chordsToPlay = [NO_BUTTON_CHORD]
    playOpen = True
    playing = False
    
    print "Initialization complete"

    while True:
        fist()

# The main loop. Listens to the eventqueue
def fist():
    global inputDriver, chordsOpen, chordsMuted
    
    # this keeps the application idle until an event is caught
    firstevent= pygame.event.wait()
    # put back the event taken out by wait()
    pygame.event.post(firstevent)
    #print "GotEvent  " + pygame.event.event_name(event.type)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
	inputEvent = inputDriver.handleInputEvent(event)
	if not inputEvent == None:
	    print "Eventcode: " + inputEvent.eventCode
	    handleEventCode(inputEvent)

	
	
def handleEventCode(inputEvent):
  
    eventCode = inputEvent.eventCode


    if inputEvent.eventType == InputEvent.CONST_TYPE_CHORD_DOWN:
	handleChordPressed(int(eventCode.replace("chord", "")))
    if inputEvent.eventType == InputEvent.CONST_TYPE_CHORD_UP:
	handleChordReleased(int(eventCode.replace("chord", "")))
    if eventCode == "up":
        #Trigger pulled up: play all chords in the activce chordlist from muted chords map
	playMutedChords()
    if eventCode == "down":
        #Trigger pushed down: play all chords in the activce chordlist from open chords map
	playOpenChords()
    if eventCode == "stop":
	#Trigger released: stop all chords
	stopAll()
    if eventCode == "nextSong":
	nextSong()
    if eventCode == "previousSong":
	previousSong()
    if eventCode == "exit":
	sys.exit()


def nextSong():
    global currentSong
    if currentSong == len(songs)-1:
        currentSong = 0
    else:
        currentSong = currentSong + 1
    songs[songs.keys()[currentSong]].getInitSound().play()
    
	

# Handler if a button has been pushed.
# Adds the selected chord to the list of actice chords.
# Removes the cord played when no button is pressed from the list and stops it.
# Immediately plays the chord when the trigger is active
def handleChordPressed(chord):
    global chordsToPlay
    
    print "Playing chord " + str(chord)
    
    if (chord > 5):
        return

    chordsToPlay.append(chord)

    if (NO_BUTTON_CHORD in chordsToPlay):
        chordsToPlay.remove(NO_BUTTON_CHORD)
        stopChord(NO_BUTTON_CHORD)
    playChord(chord)

# Handler if a button has been released
# Removes the selected chord to the list of actice chords
# Adds the cord played when no button is pressed to the list and plays it if the trigger is active.
# Immediately stops the chord when the trigger is active.
def handleChordReleased(chord):
    global chordsToPlay
    if (chord > 5):
        return

    chordsToPlay.remove(chord)
    
    
    #TODO what is this for? why check the guitar and not just the array length?
    #if (noButtonPresed()):
    if (len(chordsToPlay) == 0):
        chordsToPlay.append(NO_BUTTON_CHORD)
        playChord(NO_BUTTON_CHORD)
    
    
    
    stopChord(chord)

#stops all chords    
def stopAll():
    global playing
    pygame.mixer.stop()
    playing = False

# stops a single chord    
def stopChord(chord):
    if (chord > 5):
        return

    getCurrentSong().getChord(chord)["down"].stop()
    getCurrentSong().getChord(chord)["up"].stop()

def getCurrentSong():
    global songs, currentSong
    return songs[songs.keys()[currentSong]]

# plays a single chord when the trigger is active 
def playChord(chord):
    global playOpen, playing, chordsMuted, chordsOpen, songs, currentSong

    if (chord > 5):
        return

    # as soon as anyother chord than the NO_BUTTON_CHORD is played stop it, otherwise it may be heard chortly when changing a chord
    if (chord > NO_BUTTON_CHORD):
        stopChord(NO_BUTTON_CHORD)
        
    if (playing and playOpen):
        getCurrentSong().getChord(chord)["down"].play()
    if (playing and not playOpen):
        getCurrentSong().getChord(chord)["up"].play()
    
# plays chords from the active chords list using the open chords samples
def playOpenChords():
    global playing, playOpen, chordsToPlay
    playing = True
    playOpen = True
    for chord in chordsToPlay:
        playChord(chord)


# plays chords from the active chords list using the muted chords samples
def playMutedChords():
    global playing, playOpen, chordsToPlay
    playOpen = False
    playing = True
    for chord in chordsToPlay:
        playChord(chord)
    playing = True



# Helper that 
def noButtonPresed():
    global guitar
    status =  ( not guitar.get_button(0)\
            and not guitar.get_button(1)\
            and not guitar.get_button(2)\
            and not guitar.get_button(3)\
            and not guitar.get_button(4))
    return status

if __name__ == '__main__':
    main()
