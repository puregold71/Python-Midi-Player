#!/usr/bin/env python
import csv
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile, askopenfile
import pygame
#from midiutil.MidiFile import MIDIFile
from midiutil import MIDIFile



class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry("1000x600+200+50")
        self.title("MIDI Music Maker")
        self.addInput()
        self.addOutput()



    def addInput(self):
        menubar = Menu(self, tearoff=0)
        self.config(menu=menubar)
        fileMenu=Menu(menubar)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command = self.clearMIDI)
        fileMenu.add_command(label="Open" , command = self.askopenfile)
        fileMenu.add_separator()
        fileMenu.add_command(label="Save As", command=self.asksaveasfile)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)

        fileMenu=Menu(menubar)
        menubar.add_cascade(label="Edit", menu=fileMenu)
        fileMenu.add_command(label="Undo", command=self.undo)
        fileMenu.add_separator()
    ##    fileMenu.add_command(label="Redo", command=self.redo)



        Label(self, height=50, width = 25, bg="black").grid(row=0, column = 0, rowspan = 30, columnspan = 1, sticky = "w")
        Label(self, text = "Let's Make Some Music", font = ("bold", "12"), bg="white").grid(row = 0, columnspan = 4, sticky="we")
        self["bg"] = "white"

        Label(self, text = "Pitch", bg="white").grid(row = 1, column = 1)
        scrollbar = Scrollbar(self)
        scrollbar.grid(row = 2, column = 2, sticky="nw")
        self.lstPitch = Listbox(self, height=3, width = 15, selectmode=SINGLE)
        self.lstPitch.grid(row=2, column = 1, sticky="n")
        self.lstPitch.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lstPitch.yview)
        self.lstPitch.insert(END, "C", "C#", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B")

        Label(self,text="",bg="white",padx=7).grid(row=1,column=3)
        Label(self,text="",bg="white",padx=10).grid(row=1,column=6)

        Label(self, text = "Duration", bg="white", padx=5).grid(row  = 1, column = 4)
        sb = Scrollbar(self)
        sb.grid(row = 2, column = 5, sticky = "nw")
        self.listDuration = Listbox(self, height=3, width=20,selectmode=SINGLE)
        self.listDuration.grid(row = 2, column = 4, sticky = "ne")
        self.listDuration.config(yscrollcommand=sb.set)
        sb.config(command=self.listDuration.yview)
        self.listDuration.insert(END, "Whole Note - 1", "Half Note - .5", "Quarter Note - .25", "Eighth Note - .125", "Sixteenth Note - .0625")


        Label(self, text = "Octave", bg="white",padx=5).grid(row = 1, column = 7, sticky="nwe")
        sbar=Scrollbar(self)
        sbar.grid(row = 2, column = 8, sticky = "nw")
        self.listOctave = Listbox(self, height=3, width = 10, selectmode=SINGLE)
        self.listOctave.grid(row=2, column=7, sticky = "nwe")
        self.listOctave.config(yscrollcommand=sbar.set)
        sbar.config(command=self.listOctave.yview)
        self.listOctave.insert(END, 1,2,3,4,5,6,7,8,9,10,11)










    def playMidi(self):
        list=self.listMyMIDI.get(0,END)
        length=len(list)
        MyMIDI = MIDIFile(length)
        listtrack=range(0,length)
        channel = 1
        listpitch = self.listPitchNum.get(0,END)
       # listtime = range(0,length)
        time = 0
        listduration = self.listDurOut.get(0,END)
        volume = 100

        for i in range (0,length):
            track = listtrack[i]
            channel = 1
            pitch = listpitch[i]
           # time = listtime[i]
            time = time + 1
            duration = listduration[i]
            volume = 100
            MyMIDI.addNote(track,channel,pitch,time,duration,volume)


   #     binfile = open("MyMIDI.mid",'wb')
    #    MyMIDI.writeFile(binfile)
     #   binfile.close()

        with open("MyMIDI.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)

        musicfile = open("MyMIDI.mid", 'rb')
        pygame.mixer.init()
        pygame.mixer.music.load(musicfile)
        pygame.mixer.music.play()


    def addPitch(self):
        selected=self.lstPitch.curselection()
        if selected == ():
            messagebox.showinfo ("Error", "Please select Pitch")
        if selected != ():
            selValue = self.lstPitch.get(selected[0])
            self.listPitchOut.insert(END,selValue)
            self.listPitchOut.get(0,END)


    def addOctave(self):
        note = ["C", "C#", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
        pitchlist = range(0,127)
        octave = list(range(1,13))
       # octave=range(1,13)
    ## Pitch value is an int between 1 and 127. This covers 11 octaves. Break down pitchlist by octaves
        octave[1] = pitchlist[0:12]
        octave[2] = pitchlist[12:24]
        octave[3] = pitchlist[24:36]
        octave[4] = pitchlist[36:48]
        octave[5] = pitchlist[48:60]
        octave[6] = pitchlist[60:72]
        octave[7] = pitchlist[72:84]
        octave[8] = pitchlist[84:96]
        octave[9] = pitchlist[96:108]
        octave[10] = pitchlist[108:120]
        octave[11] = pitchlist[120:127]


        selected=self.listOctave.curselection()
        if selected == ():
            messagebox.showinfo ("Error", "Please select Octave")

        if selected != ():
            selValue = self.listOctave.get(selected[0])
            self.listOctOut.insert(END,selValue)
            self.listOctOut.get(0,END)
            y=self.listPitchOut.get(END)
            z=note.index(y)

    ##Octave 11 only contains pitches 120 through 127 (C through F#) Show error message if octave 11 is chosen with these pitches
            if z in range(7,12):
                if selValue == 11:
                    messagebox.showinfo ("Error", "Octave 11 does not contain pitches G through B\nPlease choose a different pitch or octave")
                    self.undo()

            pitch = octave[selValue][z]
            self.listPitchNum.insert(END,pitch)
            p=self.listPitchNum.get(0,END)
            tracks = len(p)-1
            self.lblTracks["text"]= tracks+1
            self.addMidi()




    def addMidi(self):
        x=self.listPitchOut.get(END)
        y=self.listDurOut.get(END)
        z=self.listOctOut.get(END)
        self.listMyMIDI.insert(END,(x,y,z))
        midi=self.listMyMIDI.get(0,END)
        self.lblMyMIDI["text"] = midi


    def addDuration(self):
        selected=self.listDuration.curselection()
        if selected == ():
            messagebox.showinfo ("Error", "Please select Duration")
        if selected != ():
            selValue = self.listDuration.get(selected[0])
            if selValue == "Whole Note - 1":
                duration = 1
            elif selValue == "Half Note - .5":
                duration = .5
            elif selValue == "Quarter Note - .25":
                duration = .25
            elif selValue == "Eighth Note - .125":
                duration = .125
            elif selValue == "Sixteenth Note - .0625":
                duration = .0625
            else:
                print ("Something went wrong!")

            self.listDurOut.insert(END,duration)
            self.listDurOut.get(0,END)


    def asksaveasfile(self):
         return asksaveasfile(mode='wb')

    def askopenfile(self):
         return askopenfile(mode='r')

    def saveCSVfile(self):
          L=self.listMyMIDI.get(0,100)
          with asksaveasfile('wb') as f:
              wtr = csv.writer(f, delimiter= ' ')
              wtr.writerows(L)



    def clearMIDI(self):
        self.listPitchOut.delete(0,END)
        self.listDurOut.delete(0,END)
        self.listOctOut.delete(0,END)
        self.listMyMIDI.delete(0,END)
        self.listPitchNum.delete(0,END)
        c=self.listMyMIDI.get(0)
        self.lblMyMIDI["text"]= c
        self.lblTracks["text"] = 0



    def undo(self):
        self.listPitchOut.delete(END)
        self.listDurOut.delete(END)
        self.listOctOut.delete(END)
        self.listMyMIDI.delete(END)
        self.listPitchNum.delete(END)
        c=self.listMyMIDI.get(0,END)
        self.lblMyMIDI["text"] = c
        list = self.listMyMIDI.get(0, END)
        length = len(list)+1
        listtrack = range(0, length)
        for i in range (0,length):
            track = listtrack[i]
        self.lblTracks["text"] = track

    def open(self):
       pass



    def addOutput(self):
    #    self.btnCalc = Button(self, text = "Add to MyMIDI", bg="white", fg="black")
    #    self.btnCalc.grid(row = 2, column = 9, sticky="n", padx=10)
    #    self.btnCalc["command"] = self.addMidi

        self.btnCalc = Button(self, text = "Choose Pitch", bg="white", fg="black")
        self.btnCalc.grid(row = 3, column = 1, sticky="n")
        self.btnCalc["command"] = self.addPitch

        self.btnCalc = Button(self, text = "Choose Duration", bg="white", fg="black")
        self.btnCalc.grid(row = 3, column = 4, sticky="n")
        self.btnCalc["command"] = self.addDuration

        self.btnCalc = Button(self, text = "Choose Octave", bg="white", fg="black")
        self.btnCalc.grid(row = 3, column = 7, sticky="nwe")
        self.btnCalc["command"] = self.addOctave


        Label(self, text = "# Tracks", bg="black", fg="white").grid(row = 6, column = 0, sticky="e")
        self.lblTracks = Label(self, anchor = "w", relief = "groove")
        self.lblTracks.grid(row = 6, column = 1, sticky = "we", padx=10)

        self.btnCalc = Button(self, text = "Play MyMIDI", bg="white", fg="black")
        self.btnCalc.grid(row = 6, column = 2, columnspan=3)
        self.btnCalc["command"] = self.playMidi


    ##    Label(self, text = "MyMIDI List", fg="white", bg="white").grid(row = 10, column = 10)
        self.listMyMIDI = Listbox(self, relief = "groove", height=10)
    ##    self.listMyMIDI.grid(row = 11, column = 11, columnspan=3,  sticky = "we")

        Label(self, text = "Pitch Selected", fg="black", bg="white").grid(row=10, column=1, columnspan=2)
        self.listPitchOut = Listbox(self, relief="groove", height=10)
        self.listPitchOut.grid(row=11, column=1, columnspan=2)

        Label(self, text = "Duration Selected", fg="black", bg="white").grid(row=10, column=4)
        self.listDurOut = Listbox(self, relief="groove", height=10)
        self.listDurOut.grid(row=11, column=4, )

        Label(self, text = "Octave Selected", fg="black", bg="white").grid(row=10, column=7, sticky="we")
        self.listOctOut = Listbox(self, relief="groove", height=10)
        self.listOctOut.grid(row=11, column=7)

        Label(self,text = "Pitch Number", fg="black", bg="white").grid(row=10, column=8, columnspan=3)
        self.listPitchNum = Listbox(self, relief="groove", height = 10)
        self.listPitchNum.grid(row=11, column=8, columnspan=3)



        Label(self, text = "MyMIDI", bg="black", fg="white").grid(row = 7, column = 0, sticky="e")
        self.lblMyMIDI = Label(self, anchor="w", relief = "groove")
        self.lblMyMIDI.grid(row=7, column=1, columnspan = 12, sticky="we", padx=10)

        self.btnCalc = Button(self, text = "Clear MyMIDI", bg="white", fg="black")
        self.btnCalc.grid(row = 8, column = 1)
        self.btnCalc["command"] = self.clearMIDI

        self.btnCalc = Button(self, text = "Undo", bg="white", fg="black")
        self.btnCalc.grid(row = 2, column = 10, sticky="n")
        self.btnCalc["command"] = self.undo

        self.btnCalc = Button(self, text = "Save MyMIDI", bg="white", fg="black")
        self.btnCalc.grid(row = 9, column = 1)
        self.btnCalc["command"] = self.asksaveasfile

        self.btnCalc = Button(self, text="Open MIDI", bg="white", fg="black")
        self.btnCalc.grid(row = 9, column = 2, columnspan=3)
        self.btnCalc["command"] = self.openMyMidi

    def openMyMidi(self):
        musicfile = askopenfilename()
        pygame.mixer.init()
        pygame.mixer.music.load(musicfile)
        pygame.mixer.music.play()



def main():
    app=App()
    app.mainloop()

if __name__=="__main__":
  main()


