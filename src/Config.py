#!/usr/bin/python
import pygame
import sys
import xml.etree.ElementTree as ET
from pygame.locals import *
from os import listdir

class Song:

    def __init__(self,tree):
        chords = {}
        root = tree.getroot()
        self.setId(root.attrib["id"])
        self.setName(root.attrib["name"])
        self.setInitSound(pygame.mixer.Sound(root.attrib["initSound"]))
        for chordEl in root.iter('chord'):
            sounds = {}
            for soundEl in chordEl.iter('sound'):
                sounds[soundEl.attrib["id"]] = pygame.mixer.Sound(soundEl.attrib["file"])
            
            chords[int(chordEl.attrib["id"])] = sounds
        
        self.setChords(chords)

    def getInitSound(self):
        return self.initSound

    def setInitSound(self,initSound):
        self.initSound = initSound

    def getChord(self, chord):
        return self.chords[chord]

    def setChords(self,chords):
        self.chords = chords
        
    def getId(self):
        return self.anId

    def setId(self,anId):
        self.anId = anId

    def getName(self,name):
        return self.name

    def setName(self,name):
        self.name = name

class Config:

    def __init__(self):
        self.songs = {}

    def loadSongConfig(self):
        filelist = listdir("../songs");
        for songfile in filelist:
            if songfile.endswith("song"):
                tree = ET.parse("../songs/" + songfile)
                song = Song(tree)
                self.songs[song.getId()] = song
        
        #load input driver config
        mainConfigTree = ET.parse('../config.sys')
        mainConfigRoot = mainConfigTree.getroot()
        
        useInputEl = mainConfigRoot.find('useInput')
        self.inputId = useInputEl.attrib['inputId']
        
        
        for inputEl in mainConfigRoot.findall('input'):
	    if inputEl.attrib['id'] == self.inputId:
	      
	        inputDriverId = inputEl.attrib['driver']
	        inputName = inputEl.attrib['name']
	        
	        if (inputDriverId == "keyboard"):
		    self.inputDriver = InputDriverKeyboard(inputEl, inputName)
	        if (inputDriverId == "joystick"):
		    self.inputDriver = InputDriverJoystick(inputEl, inputName, useInputEl.attrib['deviceNumber'])
	if hasattr (self, "inputDriver"):
	    print "Using input " + inputName + " (" + self.inputId + ") with driver " + inputDriverId
	else:
	    print "Could not find input with id '" + self.inputId + "'"
	    sys.exit()
        
    def getSongs(self):
        return self.songs
        


class InputEvent:
  
    CONST_TYPE_CHORD_UP = 0
    CONST_TYPE_CHORD_DOWN = 1
    CONST_TYPE_TRIGGER = 2
  
    def __init__(self, eventCode, eventType):
	self.eventCode = eventCode
	self.eventType = eventType
      
      
    
class InputDriverKeyboard:

    def __init__(self, inputEl, inputName):
	self.buttons = {}
        buttonsEl = inputEl.find('buttons')
        
        for buttonEl in buttonsEl.findall('button'):
	    self.buttons[int(buttonEl.attrib['hardwareId'])] = (buttonEl.attrib['eventIdDown'], buttonEl.attrib['eventIdUp'])
	
	#we actually have to open a display, otherwise we do not get any input
	#sdl driver set to dummy does not work!
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('GuitarPyPi')
	#pygame.event.set_grab(True)
	#pygame.mouse.set_visible(0)

	pygame.event.set_blocked(MOUSEMOTION)
	pygame.event.set_blocked(ACTIVEEVENT)
        
    def handleInputEvent (self, event):
	if event.type == KEYDOWN or event.type == KEYUP:
	    scancode = event.scancode
	    if not scancode in self.buttons:
		return None
		
	    if event.type == KEYDOWN:
		eventCode = self.buttons[scancode][0]
	    if event.type == KEYUP:
		eventCode = self.buttons[scancode][1]

	    if   event.type == KEYDOWN and eventCode.startswith("chord"):
		return InputEvent(eventCode, InputEvent.CONST_TYPE_CHORD_DOWN)
	    elif event.type == KEYUP and eventCode.startswith("chord"):
		return InputEvent(eventCode, InputEvent.CONST_TYPE_CHORD_UP)
	    else:
		return InputEvent(eventCode, InputEvent.CONST_TYPE_TRIGGER)
        
        debugTxt = "Unsupported event with type '" + str(event.type) + "'"
        if hasattr (event, "scancode"):
	  debugTxt = debugTxt + ", scancode '" + str(event.scancode)
	if hasattr (event, "value"):
	  debugTxt = debugTxt + "', axis '" + str(event.value) + "'"
        print  debugTxt
        return None;
        


class InputDriverJoystick:

    def __init__(self, inputEl, inputName, deviceNumber):
      
	self.buttons = {}
	self.triggers = {}
      
        buttonsEl = inputEl.find('buttons')
        triggersEl = inputEl.find('triggers')
        
        for buttonEl in buttonsEl.findall('button'):
	    self.buttons[int(buttonEl.attrib['hardwareId'])] = (buttonEl.attrib['eventIdDown'], buttonEl.attrib['eventIdUp'])
        
        for triggerEl in triggersEl.findall('axis'):
	    self.triggers[str(triggerEl.attrib['x']) + str(triggerEl.attrib['y'])] = triggerEl.attrib['eventId']
        
        
	pygame.joystick.init()

	# we do not need this event which is thrown permanently by the guitar
	pygame.event.set_blocked(JOYAXISMOTION)

	print "Using joystick device " + deviceNumber
	self.pygameJoystick = pygame.joystick.Joystick(int(deviceNumber))
	self.pygameJoystick.init()

    #returns InputEvent
    def handleInputEvent (self, event):
	if event.type == JOYHATMOTION:
	    triggerKey = str(event.value[0]) + str(event.value[1]);
	    if triggerKey in self.triggers:
		return InputEvent(self.triggers[triggerKey], InputEvent.CONST_TYPE_TRIGGER)
	
	elif event.type == JOYBUTTONDOWN:
	    if event.button in self.buttons:
	      return InputEvent(self.buttons[event.button][0], InputEvent.CONST_TYPE_CHORD_DOWN)
        
        elif event.type == JOYBUTTONUP:
	    if event.button in self.buttons:
	      return InputEvent(self.buttons[event.button][1], InputEvent.CONST_TYPE_CHORD_UP)
        
        debugTxt = "Unsupported event with type '" + str(event.type) + "'"
        if hasattr (event, "button"):
	  debugTxt = debugTxt + ", button '" + str(event.button)
	if hasattr (event, "value"):
	  debugTxt = debugTxt + "', axis '" + str(event.value) + "'"
        print  debugTxt
        return None;
        
