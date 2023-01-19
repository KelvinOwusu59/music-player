from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import pygame
from tkinter import messagebox as msg
import time
from mutagen.mp3 import MP3

#gets the root of the screen
root=Tk()
root.title(" Kelvin's Music Player")
root.geometry("500x500+400+500")
root.resizable(0,0)


#initialize
pygame.mixer.init()

#functions
song_list=[]
def add_song():
    songs=filedialog.askopenfilenames(
       initialdir="/",title="Open File(s)",filetypes=(("MP3 Files","*.mp3"),)
    )#helps you to import a lot of filess
    print(songs)
    for song in songs:
        song_list.append(song)
        song=os.path.basename(song)
        songbox.insert(END,song)

#playing song
is_paused=False # the play function needs 
def play_song():
    #stop_music() #adding same to the play_song
    try:
        song_index=songbox.curselection()[0]
        song=song_list[song_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        #activate Slider movement
        move_slider()
    except Exception as e:
        pass



is_paused=False# we need to set 
def pause_and_unpause():
    try:
        global is_paused # so that when you declare a an is_paused variable, it wont mistake it.
        if is_paused is False:
            pygame.mixer.music.pause()
            is_paused=not is_paused#another way of setting True
        else:
            pygame.mixer.music.unpause()
            is_paused=False
    except Exception as e:
        pass

#stop_music
def stop_music():
    try:
        pygame.mixer.music.stop()
        music_slider.config(value=0)
        status_bar.configure(text=f"Press song to play!!")

    except Exception as e:
        pass

#previous music
def previous():
    stop_music() # we are adding the stop to the music so that before it goes to the previous , it would stop it first
    try:
        song_index=songbox.curselection()[0]
        previous_index=song_index-1
        song=song_list[previous_index]# only the line 56 changes and then we subtract -1
        #there is bug here becuase you manually have to get the prvious by selecting first which we dont like#

        #clear songbox selection
        songbox.select_clear(0,END) #clears all selected from first to the last

        #activate previous song
        songbox.activate(previous_index)

        #set the selection
        songbox.selection_set(previous_index,last=None)
        #load
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    except Exception as e:
        pass

def next_song():
    stop_music() #adding same to next as the previous
    try:
        song_index=songbox.curselection()[0]
        next_index=song_index+1
        song=song_list[next_index]# only the line 56 changes and then we subtract -1
        #there is bug here becuase you manually have to get the prvious by selecting first which we dont like#

        #clear songbox selection
        songbox.select_clear(0,END) #clears all selected from first to the last

        #activate previous song
        songbox.activate(next_index)

        #set the selection
        songbox.selection_set(next_index,last=None)
        #load
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    except Exception as e:
        pass

def remove_one_song():
    try:
        stop_music()
        current_song=songbox.curselection()[0]
        #remove from the Songbox
        songbox.delete(ANCHOR) #currently delte the selected item
        #remove from song list
        song_list.pop(current_song)# the pop remves it and returns it
    except Exception as e:
        pass


def remove_all_song():
    try:
        stop_music()
        current_song=songbox.curselection()[0]
        #remove from the Songbox
        songbox.delete(0,END) #currently delete the selected item
        #remove from song list
        song_list.clear()
        if current_song is play_btn:
            stop_music()
    except Exception as e:
        pass

def about():
    msg.showinfo("Developer Information",
    "This cool music player is made possible witht the help of Benz. It has a lot of functionalities that in real life can do alot of crazy stuffs.")

def move_slider():
    if not pygame.mixer.get_busy:
        return
    
    #Getting the current time, we use the current position
    current_play_time=pygame.mixer.music.get_pos()/1000
    converted_play_time=time.strftime("%H:%M:%S",time.gmtime(current_play_time)) # trying to give the format in the form of 00:33:22
    # gmt time converts it to a format that can be seen

    #we use mutagen to get the sec/of the total time of the music.

    #NB: Before we get the length we have to get the instance of it so that we can use the mutagen to get the length of the time.
    song_index=songbox.curselection()[0]
    song=song_list[song_index]
    song_mutagen=MP3(song)
    song_length=song_mutagen.info.length
    #convert song length to the standard format
    converted_song_time=time.strftime("%H:%M:%S",time.gmtime(song_length))
    #note that pygame can not manually add the time in seconds so we definitely have to hardcode it ourself.

    #increase time by second
    current_play_time+=1
    slider_pos=int(song_length) #converting the time to seconds
    #creating an exeption for the is_paused
    if is_paused:
        pass
    #trying to check if the integer of the curret length is equal to the current_pos
    elif int(music_slider.get())==int(current_play_time):
        music_slider.config(to=slider_pos,value=int(current_play_time))# changing the music of the song_length to the length ofnthe music.
        #setting the value to current_play_time to the value.
        status_bar.configure(text=f"Time elapsed: {converted_play_time} of {converted_song_time}")
    else:
        music_slider.config(to=slider_pos,value=int(music_slider.get()))
        #increase song by one second
        new_time=int(music_slider.get())+1
        music_slider.config(value=new_time) #setting the music_slider to the new time
        new_current=int(music_slider.get())
        converted_new_current=time.strftime("%H:%M:%S",time.gmtime(new_current))
        status_bar.configure(text=f"Time elapsed: {converted_new_current-1} of {converted_song_time}")
        # we are getting the play time of the song time to see how far the music has reached.


    #update status bar every one second
    #its in millisec so we are trying to get it to seconds thats why there's 1000 there
    status_bar.after(1000,move_slider)




def volume(r):# we need to pass in something inside to get the slider work
    #set the volume 
    pygame.mixer.music.set_volume(vol_slider.get())

    #get the current volume
    current_vol=pygame.mixer.music.get_volume()*100 # it comes in as a float so multipying it by 100 makes it reader friendly
    if current_vol<1:
        vol_meter.config(image=vol0)
    elif current_vol<=10:
        vol_meter.config(image=vol10)
    elif current_vol<=20:
        vol_meter.config(image=vol20)
    elif current_vol<=30:
        vol_meter.config(image=vol30)
    elif current_vol<=40:
        vol_meter.config(image=vol40)
    elif current_vol<=50:
        vol_meter.config(image=vol50)
    elif current_vol<=60:
        vol_meter.config(image=vol60)
    elif current_vol<=70:
        vol_meter.config(image=vol70)
    elif current_vol<=80:
        vol_meter.config(image=vol80)
    elif current_vol<=90:
        vol_meter.config(image=vol90)
    elif current_vol<=100:
        vol_meter.config(image=vol100)  

def slider(x):
    current_song_index=songbox.curselection()[0]
    current_song=song_list[current_song_index] 
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play(loops=0,start=int(music_slider.get()))   
#menu bar
appmenu=Menu(root)
root.config(menu=appmenu)#parameter to value
filemenu=Menu(appmenu)
appmenu.add_cascade(label="file",menu=filemenu)#cascade represents the title
#the commands aare what is under the title
filemenu.add_command(label="Add Songs",accelerator=["Ctrl+O"],command=add_song)
#accelerator helps to add shortcuts to the menu

#getting the volme images
vol0=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol0.png")
vol10=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol10.png")
vol20=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol20.png")
vol30=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol30.png")
vol40=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol40.png")
vol50=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol50.png")
vol60=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol60.png")
vol70=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol70.png")
vol80=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol80.png")
vol90=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol90.png")
vol100=PhotoImage(file=r"/Users/kelvinowusu/Desktop/tkayint/Vol/Vol100.png")

#Song Menu
songmenu=Menu(appmenu)
appmenu.add_cascade(label="Songs",menu=songmenu)#cascade represents the title
#the commands aare what is under the title
songmenu.add_command(label="Remove Selected Songs ",accelerator=["Ctrl+D"],command=remove_one_song)
songmenu.add_command(label="Remove All Songs " ,accelerator=["Ctrl+E"],command=remove_all_song)

aboutmenu=Menu(appmenu)
appmenu.add_cascade(label="About",menu=aboutmenu)#cascade represents the title
#the commands aare what is under the title
aboutmenu.add_command(label="About the Developers",command=about)



#creates the framing of the screen
mainframe=Frame(root)
mainframe.pack()

topframe=Frame(mainframe)
topframe.pack(fill=X)

btnframe=Frame(mainframe)
btnframe.pack(pady=40,fill=X)

music_control_frame=Frame(mainframe)

music_control_frame.pack(fill=X)

volframe=Frame(mainframe)
volframe.pack(fill=X)

#Songbox
songbox=Listbox(topframe,width=70,background="chocolate",font=("Open Sans",8))
songbox.pack(pady=20)

status_bar=Label(root,text="Status bar...",bd=1,relief=GROOVE,background="blue",anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=3)

#Photo Images
playPhoto=PhotoImage(file="play.png")
PausePhoto=PhotoImage(file="pause.png")
StopPhoto=PhotoImage(file="stop.png")
PreviousPhoto=PhotoImage(file="prev.png")
nextphoto=PhotoImage(file="next.png")



#Buttons
play_btn=Button(btnframe,image=playPhoto,borderwidth=0,command=play_song)
play_btn.pack(side="left")

pause_btn=Button(btnframe,image=PausePhoto,borderwidth=0,command=pause_and_unpause)
pause_btn.pack(side="left")

stop_btn=Button(btnframe,image=StopPhoto,borderwidth=0,command=stop_music)
stop_btn.pack(side="left",padx=5)

previous_btn=Button(btnframe,image=PreviousPhoto,borderwidth=0,command=previous)
previous_btn.pack(side="left")

next_play=Button(btnframe,image=nextphoto,borderwidth=0,command=next_song)
next_play.pack(side="left")

music_slider=ttk.Scale(music_control_frame,from_=0, to=100,orient=HORIZONTAL,value=0,length=400,command=slider)
music_slider.pack(pady=10)

#volume slider
vol_slider=ttk.Scale(volframe,from_=0,to=1,orient=HORIZONTAL,value=0.5,length=150,command=volume)
vol_slider.pack(side=LEFT)


#volume meter
vol_meter=Label(volframe,image=vol50) # its the one that includes the images
vol_meter.pack(padx=30)
root.mainloop()



















"""
1.get the currrent song playing and check if it is the song playing but in case it is playing,it should dle
"""