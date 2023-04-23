from tkinter import *
from tkinter import messagebox
from argparse import FileType
from tkinter.filedialog import *
from PIL import ImageTk,Image
from stegano import lsb
from tkinter import font as tkFont
from stegano import exifHeader as aaa
import os
from subprocess import Popen

def encode():
	main.destroy()
	enc=Tk()
	enc.attributes("-fullscreen", True)
	enc.wm_attributes('-transparentcolor')
	img=ImageTk.PhotoImage(Image.open("bg_image.jpg"))
	fontl = tkFont.Font(family='Bahnschrift', size=32)
	label1=Label(enc,image=img)
	label1.pack()

	LabelTitle=Label(text="Encode Image",bg="#F57F17",fg="white",width=20)
	LabelTitle['font']=fontl
	LabelTitle.place(relx=0.6, rely=0.1)

	def openfile():
		global fileopen
		global imagee
		
		fileopen=StringVar()
		fileopen=askopenfilename(initialdir="/Pictures",title="Select file",filetypes=(("jpeg,png files","*jpg *png"),("all files","*.*"))) 
		imagee=ImageTk.PhotoImage(Image.open(fileopen))
		
		Labelpath=Label(text=fileopen)
		Labelpath.place(relx=0.6, rely=0.25, height=21, width=450)

		Labelimg=Label(image=imagee)
		Labelimg.place(relx=0.7, rely=0.3, height=200, width=200)



	Button2 = Button(text="Openfile",command=openfile)
	Button2.place(relx=0.7, rely=0.2, height=31, width=94)

	secimg=StringVar()
	radio1=Radiobutton(text='jpeg',value='jpeg',variable=secimg)
	radio1.place(relx=0.7, rely=0.57)
	

	radio2=Radiobutton(text='png',value='png',variable=secimg)
	radio2.place(relx=0.8, rely=0.57)
			


	Label1 =Label(text="Enter message")
	Label1.place(relx=0.6, rely=0.6, height=21, width=104)
	entrysecmes=Entry()
	entrysecmes.place(relx=0.7, rely=0.6, relheight=0.05, relwidth=0.200)

	Label2 =Label(text="File Name")
	Label2.place(relx=0.6, rely=0.70, height=21, width=104)

	entrysave=Entry()
	entrysave.place(relx=0.7, rely=0.70, relheight=0.05, relwidth=0.200)

	def encode():
		if secimg.get()=="jpeg":
			inimage=fileopen
			response=messagebox.askyesno("popup","Do you want to encode?")
			if response==1: 
				aaa.hide(inimage,entrysave.get()+'.jpg',entrysecmes.get())
				messagebox.showinfo("popup","Successfully encoded"+entrysave.get()+".jpeg")

			else:
				messagebox.showwarning("popup","Unsuccessful!")

		if secimg.get()=="png":
			inimage=fileopen
			response=messagebox.askyesno("popup","Do you want to encode?")
			if response==1: 
				lsb.hide(inimage,message=entrysecmes.get()).save(entrysave.get()+'.png')
				messagebox.showinfo("popup","Successfully encoded to "+entrysave.get()+".png")

			else:
				messagebox.showwarning("popup","Unsuccessful!")
		


	def back():
		enc.destroy()
		Popen('python image.py')

	Button2 = Button(text="Encode",command=encode)
	Button2.place(relx=0.7, rely=0.8, height=31, width=94)

	Buttonback = Button(text="Back",command=back)
	Buttonback.place(relx=0.7, rely=0.85, height=31, width=94)

	enc.mainloop()



def decode():
	main.destroy()
	dec=Tk()
	dec.attributes("-fullscreen", True)
	dec.wm_attributes('-transparentcolor')
	img=ImageTk.PhotoImage(Image.open("bg_image.jpg"))
	fontl = tkFont.Font(family='Bahnschrift', size=32)
	label1=Label(dec,image=img)
	label1.pack()

	LabelTitle=Label(text="Decode Image",bg="#311B92",fg="white",width=20)
	LabelTitle['font']=fontl
	LabelTitle.place(relx=0.6, rely=0.1)

	secimg=StringVar()
	radio1=Radiobutton(text='jpeg',value='jpeg',variable=secimg)
	radio1.place(relx=0.7, rely=0.57)
	

	radio2=Radiobutton(text='png',value='png',variable=secimg)
	radio2.place(relx=0.8, rely=0.57)
		
	
	
	def openfile():
		global fileopen
		global imagee
		fileopen=StringVar()
		fileopen=askopenfilename(initialdir="/Pictures",title="Select file",filetypes=(("jpeg files, png file","*jpg *png"),("all files","*.*"))) 
		
		imagee=ImageTk.PhotoImage(Image.open(fileopen))
		Labelpath=Label(text=fileopen)
		Labelpath.place(relx=0.6, rely=0.25, height=21, width=450)

		Labelimg=Label(image=imagee)
		Labelimg.place(relx=0.7, rely=0.3, height=200, width=200)

		
	def deimg():
		if secimg.get()=="png":
			messag=lsb.reveal(fileopen)

		if secimg.get()=="jpeg":
			messag=aaa.reveal(fileopen)	
		
		Label2=Label(text=messag)
		Label2.place(relx=0.7, rely=0.7, height=21, width=204)
		

	Button2 = Button(text="Openfile",command=openfile)
	Button2.place(relx=0.7, rely=0.2, height=31, width=94)

	Button2 = Button(text="Decode",command=deimg)
	Button2.place(relx=0.7, rely=0.8, height=31, width=94)
	


	def back():
		dec.destroy()
		Popen('python image.py')

	Buttonback = Button(text="Back",command=back)
	Buttonback.place(relx=0.7, rely=0.85, height=31, width=94)

	dec.mainloop()

#main program
main=Tk()
main.title('Steganography')
main.attributes("-fullscreen", True)
fontl = tkFont.Font(family='Bahnschrift', size=32)

global image1
image1=ImageTk.PhotoImage(Image.open("bg_image.jpg"))
label=Label(main,text="image",image=image1)
label.pack()

encbutton=Button(text='Encode',fg="Black",bg="#fff",width=20,command=encode)
encbutton['font'] =fontl 
encbutton.place(relx=0.6,rely=0.3)
encbutton.config(borderwidth=0, bd=0)


decbutton=Button(text='Decode',fg="Black",bg="#fff",width=20,command=decode)
decbutton['font'] =fontl 
decbutton.place(relx=0.6,rely=0.5)
decbutton.config(borderwidth=0, bd=0)

def exit():
	main.destroy()

closebutton=Button(text='Exit',fg="black",bg="#F44336",width=20,command=exit)
closebutton['font'] =fontl 
closebutton.place(relx=0.6,rely=0.7)
closebutton.config(borderwidth=0, bd=0)
main.mainloop()