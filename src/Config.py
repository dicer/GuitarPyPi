#!/usr/bin/python
import pygame
import xml.etree.ElementTree as ET
from pygame.locals import *

class Song:

    def getInitSound(self):
        return self.initSound

    def setInitSound(self,initSound):
        self.initSound = initSound

    def getChord(self, chord):
        return self.chords[chord]

    def setChords(self,chords):
        self.chords = chords
        
    def getId(self):
        return self.id

    def setId(self,id):
        self.id = id

    def getName(name):
        return self.name

    def setName(self,name):
        self.name = name

class Config:

    def __init__(self):
        self.songs = {}

    def loadSongConfig(self):
        tree = ET.parse('../songs/test1.song')
        chords = {}
        song = Song()
        root = tree.getroot()
        song.setId(root.attrib["id"])
        song.setName(root.attrib["name"])
        song.setInitSound(pygame.mixer.Sound(root.attrib["initSound"]))
        for chordEl in root.iter('chord'):
            sounds = {}
            for soundEl in chordEl.iter('sound'):
                sounds[soundEl.attrib["id"]] =  pygame.mixer.Sound(soundEl.attrib["file"])

            chords[int(chordEl.attrib["id"])] = sounds 
        song.setChords(chords)
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
	        
        print "Using input " + inputName + " (" + self.inputId + ") with driver " + inputDriverId
        
    def getSongs(self):
        return self.songs
        

        
    
class InputDriverKeyboard:

    def __init__(self, inputEl, inputName):
	self.buttons = {}
        


class InputDriverJoystick:

    def __init__(self, inputEl, inputName, deviceNumber):
      
	self.buttons = {}
	self.triggers = {}
      
        buttonsEl = inputEl.find('buttons')
        triggersEl = inputEl.find('triggers')
        
        for buttonEl in buttonsEl.findall('button'):
	    self.buttons[int(buttonEl.attrib['hardwareId'])] = buttonEl.attrib['eventId']
        
        for triggerEl in triggersEl.findall('axis'):
	    self.triggers[str(triggerEl.attrib['x']) + str(triggerEl.attrib['y'])] = triggerEl.attrib['eventId']
        
        
	pygame.joystick.init()

	# we do not need this event which is thrown permanently by the guitar
	pygame.event.set_blocked(JOYAXISMOTION)

	print "Using joystick device " + deviceNumber
	self.pygameJoystick = pygame.joystick.Joystick(int(deviceNumber))
	self.pygameJoystick.init()

    def handleInputEvent (self, event):
	if event.type == JOYHATMOTION:
	    triggerKey = str(event.value[0]) + str(event.value[1]);
	    if triggerKey in self.triggers:
		return self.triggers[triggerKey]
	
	elif event.type == JOYBUTTONDOWN:
	    if event.button in self.buttons:
	      return "pressed" + self.buttons[event.button]
        
        elif event.type == JOYBUTTONUP:
	    if event.button in self.buttons:
	      return "released" + self.buttons[event.button]
        
        debugTxt = "Unsupported event with type '" + str(event.type) + "'"
        if hasattr (event, "button"):
	  debugTxt = debugTxt + ", button '" + str(event.button)
	if hasattr (event, "value"):
	  debugTxt = debugTxt + "', axis '" + str(event.value) + "'"
        print  debugTxt
        return "";
        
