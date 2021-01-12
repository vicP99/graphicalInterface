"""Premier exemple avec Tkinter.

On crée une fenêtre simple qui souhaite la bienvenue à l'utilisateur.

"""
# On importe Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from rocket_module import rocket
from rocket_module import read

import matplotlib.animation as animation
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from functools import partial


import rocket_module

# On crée une fenêtre, racine de notre interface
class Interface(Frame):

    def __init__(self,fenetre,**kwargs):
        Frame.__init__(self,fenetre,width=500,height=800,**kwargs) 
        self.pack(fill=BOTH)

        def check_error(self,name): #this fonction checks the potential errors, prints the errors if needed or prompts fusee if not
            nb_errors=0
            L_message=[]
            #classer les erreurs par ordre d'importance si possible (--> ligne 45 on print le premier element de la liste)
            #inserer les erreurs: if (erreur):---> L_message+=[message] nb_error+=1
            #bien verifier que le message d'erreur ne depasse pas en longueur

            try:
                if  var_pitch_angle.get()>1.57 or var_pitch_angle.get()<0 : # 2 potential erros: pitch angle out of range or wrong entry
                    L_message+=["Pitch angle outside ]0,pi/2["]
                    nb_errors+=1
            except TclError: #if the entry is not a float
                L_message+=["The pitch angle entry is empty or non-string"]
                nb_errors+=1


            if nb.get()==2 and name=="homemade rocket": #checks if there is a zero among the S2 entries
                try:  #also checks if there is a non float entry
                    check_values_own_rocket_S2=var_Height.get()*var_lift_off_mass.get()*var_payload_mass.get()*var_S1_length.get()*float(S1_diameter.get())*float(S1_thrust.get())*var_S1_Isp.get()*var_S1_m0.get()*var_S1_mp.get()*var_S2_length.get()*var_S2_diameter.get()*var_S2_thrust.get()*var_S2_Isp.get()*var_S2_m0.get()*var_S2_mp.get()
                except TclError:
                    L_message+=["You have an empty entry or a non-float one"]
                    nb_errors+=1
                    check_values_own_rocket_S2=1
                if check_values_own_rocket_S2==0:
                    L_message+=["your rocket has a characteristic equal to 0"]
                    nb_errors+=1

            if nb.get()==1 and name=="homemade rocket":# same thing for S1
                try:
                    check_values_own_rocket_S1=var_Height.get()*var_lift_off_mass.get()*var_payload_mass.get()*var_S1_length.get()*float(S1_diameter.get())*float(S1_thrust.get())*var_S1_Isp.get()*var_S1_m0.get()*var_S1_mp.get()
                except TclError:
                    L_message+=["You have an empty entry or a non-float one"]
                    nb_errors+=1
                    check_values_own_rocket_S1=1
                if check_values_own_rocket_S1==0:
                    L_message+=["your rocket has a characteristic equal to 0"]
                    nb_errors+=1

            if nb_errors==0:  #if there no errors, prompts fusee to start ploting
                fusee(self,name)
            else:
                print_errors(L_message,nb_errors)
            return()

        def print_errors(L_message,nb_errors):
            self.message=Label(self,text=" "*111).place(x=550,y=670)
            self.message=Label(self,text=L_message[0]+"  ("+str(nb_errors-1)+" others)",fg='red').place(x=550,y=670)
            return() #display the error message of the first error checked and the number of other errors

        def fusee(self,nom): # fonction that plots the trajectory
            newWindows = Toplevel(fenetre) #open a new window over the prededent
            newWindows.title(nom)    # the trajctory will be ploted in a new window
            newWindows.geometry("1000x1800+300+200")

                                        #ifthe user creates his own rocket:
            if nom=="homemade rocket": #here we gather the values in the entries for the created rocket
                if nb.get()==2:#we then define a rocket class object
                    homemade_rocket=rocket(var_name,var_year,var_country,var_mission_homemade_rocket,nb.get(),var_Height.get(),var_lift_off_mass.get(),var_payload_mass.get(),var_S1_length.get(),S1_diameter.get(),S1_thrust.get(),var_S1_Isp.get(),var_S1_m0.get(),var_S1_mp.get(),var_S2_length.get(),var_S2_diameter.get(),var_S2_thrust.get(),var_S2_Isp.get(),var_S2_m0.get(),var_S2_mp.get())
                else:
                    homemade_rocket=rocket(var_name,var_year,var_country,var_mission_homemade_rocket,nb.get(),var_Height.get(),var_lift_off_mass.get(),var_payload_mass.get(),var_S1_length.get(),S1_diameter.get(),S1_thrust.get(),var_S1_Isp.get(),var_S1_m0.get(),var_S1_mp.get(),0,0,0,0,0,0)

                myRocket=homemade_rocket
            else:
                myRocket = read(nom) #if the user chooses an already existing rocket

            Dt = 10

            X,Z,G,A,T,K = rocket.trajectory(myRocket,var_pitch_angle.get(),Dt) #call trajectory to get the lists of X and Z

            #plot the mission we want (Y for now)

            xL = []
            yL = [0]
            if(var_mission.get() == 1): #GEO
                yL = [36000000,36000000] 
            if(var_mission.get() == 2): #LE0
                yL = [2000000,2000000] 
            if(var_mission.get() == 3): #Moon
                yL = []
                for i in range(100):
                    yL.append(384000000 + 2000000*np.cos(2*np.pi*i/99))

            #------------------------------------------------------------------


            #contole the scale (we want a scale that show the mission and all the trajectory of the rocket)
            if varI.get()==1 and max(yL)< max(Z): #if we also want a scale factor
                dY = max(Z)
                dX = max(X)
            else:
                dX = max(max(X),max(Z),max(yL))
                dY = dX

            #----------------------------------------------

            #plot of the X of the mission (now we know the scale so it is easy)
            if(var_mission.get() == 1):
                xL = [0,1.3*dX]
            if(var_mission.get() == 2):
                xL = [0,1.3*dX]
            if(var_mission.get() == 3):
                for i in range(100):
                    xL.append(384000000 + 2000000*np.sin(2*np.pi*i/99))
            if (len(yL) == 1):
                yL = []

            #---------------------------------------------------------
            
            R = dX/dY #scale factor different of 1 only if varI.get() == 1

            #Change of the angle and the height with the scale factor
            for i in range(len(Z)):
                Z[i] = R* Z[i]



            for i in range(len(G)):
                G[i] = np.arctan(  np.tan(G[i])*R)

            #----------------------------------------------------

            #initialisation of the list of the trajectory there are 3 lists because we want 3 colour (green when we have 2 stages, blue when we have one and red when we have zero)
            trajX0 = []
            trajY0 = []

            trajX1 = []
            trajY1 = []

            trajX2 = []
            trajY2 = []

            #--------------------------------------------------


            counter = [] #to avoid plotting several times the same trajectory when we repeat the animation. It's a list to avoid local value problem when the animation repeat

            #image at instant i for i in range(frames = len(X)) 
            def animate(i):

                #count
                if i== 0:
                    counter.append(1)
                
                #------------------------
                

                axes.clear() #to clear the last frame i-1

                #legend and scale of the graphe

                axes.set_ylim(0, 1.3*dX, auto=False)
                axes.set_xlim(0, 1.3*dX, auto=False)

                if varI.get() == 1:
                    axes.set_ylabel('hauteur(m) *'+str(int(R))+','+str(int(10*R)%10), color='g')
                else:
                    axes.set_ylabel('hauteur(m) ', color='g')
                axes.set_xlabel('x(m)', color='g')

                #---------------------------------

                #plotting of the trajectory with a coulor for the nulber of stages given by K we add a counter to avoid plotting problem because we want a line between all consecutive point but when there is a repeat the last value and the first are adjacent
                if(K[i] == 0 and len(counter) == 2):
                    trajX0.append(X[i])
                    trajY0.append(Z[i])
                elif(K[i] == 1 and len(counter) == 2 ):
                    trajX1.append(X[i])
                    trajY1.append(Z[i])
                elif (K[i] == 2 and len(counter) == 2):
                    trajX2.append(X[i])
                    trajY2.append(Z[i])
                
                


                X0,Y0 =  rocket_module.plotRocket(myRocket,G[i]-np.pi/2,X[i],Z[i],2*dX,2*dX) #plot of the rocket 
                axes.plot(X0, Y0 , 'k ,')

                axes.plot(trajX0,trajY0, 'g-')
                axes.plot(trajX1,trajY1, 'b-,')
                axes.plot(trajX2,trajY2, 'r-,')

                axes.plot(xL,yL,'y-')

                #------------------------------------------------------
#----------------------------------------------------

            #initialisation
            fig = Figure(figsize=(8, 8), dpi=111)
            axes = fig.add_subplot(111)
            axes.set_ylim(0, 1.3*dX, auto=False)
            axes.set_xlim(0, 1.3*dX)
            axes.set_ylabel('hauteur(m) *'+str(int(R))+','+str(int(10*R)%10), color='g')
            axes.set_xlabel('x(m)', color='g')

            #--------------------------------------

            #plotting on tkinter interface
            graph = FigureCanvasTkAgg(fig, master=newWindows)
            canvas = graph.get_tk_widget().pack(expand=True)


            #animation
            ani = animation.FuncAnimation(fig, animate,  frames=len(X), interval=10, repeat=True) #plotting the animation
            
            newWindows.mainloop() #starting the program


        #plotting of the  bouton there are all more or less the samme so we comment one

        self.message=Label(self,text="choose your rocket:").place(x=450,y=20)
        self.bouton_Sputnik=Button(self,text="Sputnik",command=partial(check_error,self,"Sputnik")).place(x=50,y=290) #command= ... represent the fonction call when the buton is pressed
        self.bouton_Soyuz=Button(self,text="Soyuz",command=partial(check_error,self,"Soyuz")).place(x=210,y=290)
        self.bouton_Saturn=Button(self,text="Saturn V",command=partial(check_error,self,"Saturn V")).place(x=370,y=290)
        self.bouton_Ariane=Button(self,text="Ariane 5",command=partial(check_error,self,"Ariane 5")).place(x=530,y=290)
        self.bouton_Miura=Button(self,text="Miura 1",command=partial(check_error,self,"Miura 1")).place(x=690,y=290)
        self.bouton_falcon=Button(self,text="Falcon 9",command=partial(check_error,self,"Falcon 9")).place(x=850,y=290)

        var_mission=IntVar()

        self.message=Label(self,text="Choose your mission:").place(x=660,y=580)
        choix_gto = Radiobutton(self, text="GTO", variable=var_mission, value=1).place(x=650,y=630) #var_mission will get the valu=1 when this radiobuton is ckeked
        choix_leo = Radiobutton(self, text="LEO", variable=var_mission, value=2).place(x=750,y=630)
        choix_lune = Radiobutton(self, text="LUNE", variable=var_mission, value=3).place(x=850,y=630)
        choix_none = Radiobutton(self, text='NONE', variable=var_mission, value=4).place(x=550,y=630)

        var_mission_homemade_rocket=DoubleVar()
        var_year=DoubleVar()
        var_name=DoubleVar()
        var_country=0
        def select_stages(self,nb_stage,nb):
            if nb.get()==2:
                S2_length.config(state=NORMAL)
                S2_Isp.config(state=NORMAL)
                S2_diameter.config(state=NORMAL)
                S2_thrust.config(state=NORMAL)
                S2_m0.config(state=NORMAL)
                S2_mp.config(state=NORMAL)
            else:
                S2_length.config(state=DISABLED)
                S2_Isp.config(state=DISABLED)
                S2_diameter.config(state=DISABLED)
                S2_thrust.config(state=DISABLED)
                S2_m0.config(state=DISABLED)
                S2_mp.config(state=DISABLED)
            return()

        ######
        var_S2_length = DoubleVar()
        self.message=Label(self,text="S2 length").place(x=210,y=410)
        S2_length = Entry(self, textvariable=var_S2_length, width=5)
        S2_length.place(x=325,y=410)
        S2_length.config(state=DISABLED)


        var_S2_Isp = DoubleVar()
        self.message=Label(self,text="S2 Isp").place(x=210,y=440)
        S2_Isp = Entry(self, textvariable=var_S2_Isp, width=5)
        S2_Isp.place(x=325,y=440)
        S2_Isp.config(state=DISABLED)

        var_S2_diameter = DoubleVar()
        self.message=Label(self,text="S2 diameter").place(x=210,y=470)
        S2_diameter = Entry(self, textvariable=var_S2_diameter, width=5)
        S2_diameter.place(x=325,y=470)
        S2_diameter.config(state=DISABLED)

        var_S2_thrust = DoubleVar()
        self.message=Label(self,text="S2 thrust").place(x=210,y=500)
        S2_thrust = Entry(self, textvariable=var_S2_thrust, width=5)
        S2_thrust.place(x=325,y=500)
        S2_thrust.config(state=DISABLED)

        var_S2_m0 = DoubleVar()
        self.message=Label(self,text="S2 m0").place(x=210,y=530)
        S2_m0 = Entry(self, textvariable=var_S2_m0, width=5)
        S2_m0.place(x=325,y=530)
        S2_m0.config(state=DISABLED)

        var_S2_mp = DoubleVar()
        self.message=Label(self,text="S2 mp").place(x=210,y=560)
        S2_mp = Entry(self, textvariable=var_S2_mp, width=5)
        S2_mp.place(x=325,y=560)
        S2_mp.config(state=DISABLED)
        ##########

        self.message=Label(self,text="build your own rocket ! ").place(x=120,y=325)

        nb=IntVar(self)
        self.message=Label(self,text="nb étages").place(x=40,y=350)
        nb_stage = Spinbox(self,textvariable=nb,from_=1, to=2, increment=1,width=4)
        nb_stage.place(x=150,y=350)
        nb_stage.config(command=partial(select_stages,self,nb_stage,nb))


        var_Height = DoubleVar()
        self.message=Label(self,text="Height").place(x=40,y=380)
        Height = Entry(self, textvariable=var_Height, width=5)
        Height.place(x=150,y=380)

        var_lift_off_mass = DoubleVar()
        self.message=Label(self,text="lift off mass").place(x=40,y=410)
        lift_off_mass = Entry(self, textvariable=var_lift_off_mass, width=5)
        lift_off_mass.place(x=150,y=410)

        var_payload_mass = DoubleVar()
        self.message=Label(self,text="payload mass").place(x=40,y=440)
        payload_mass = Entry(self, textvariable=var_payload_mass, width=5)
        payload_mass.place(x=150,y=440)

        var_S1_length = DoubleVar()
        self.message=Label(self,text="S1 length").place(x=40,y=470)
        S1_length = Entry(self, textvariable=var_S1_length, width=5)
        S1_length.place(x=150,y=470)

        var_S1_diameter = DoubleVar()
        self.message=Label(self,text="S1 diameter").place(x=40,y=500)
        S1_diameter = Entry(self, textvariable=var_S1_diameter, width=5)
        S1_diameter.place(x=150,y=500)

        var_S1_thrust = DoubleVar()
        self.message=Label(self,text="S1 thrust").place(x=40,y=530)
        S1_thrust = Entry(self, textvariable=var_S1_thrust, width=5)
        S1_thrust.place(x=150,y=530)

        var_S1_Isp = DoubleVar()
        self.message=Label(self,text="S1 Isp").place(x=40,y=560)
        S1_Isp = Entry(self, textvariable=var_S1_Isp, width=5)
        S1_Isp.place(x=150,y=560)

        var_S1_m0 = DoubleVar()
        self.message=Label(self,text="S1 m0").place(x=210,y=350)
        S1_m0 = Entry(self, textvariable=var_S1_m0, width=5)
        S1_m0.place(x=325,y=350)

        var_S1_mp = DoubleVar()
        self.message=Label(self,text="S1 mp").place(x=210,y=380)
        S1_mp = Entry(self, textvariable=var_S1_mp, width=5)
        S1_mp.place(x=325,y=380)



        self.homemade_rocket_button=Button(self,text="Launch !",command=partial(check_error,self,"homemade rocket")).place(x=150,y=595)

        self.message=Label(self,text="Here is our rocket simulator, this world may be a bit different").place(x=560,y=350)
        self.message=Label(self,text="(The eart is flat, with a constant gravitationnal field, without )").place(x=560,y=370)
        self.message=Label(self,text="air pressure) but we're sure you can have fun with it. ").place(x=560,y=390)
        self.message=Label(self,text="To launch a rocket you can choose either amoung some of the").place(x=560,y=420)
        self.message=Label(self,text="most famous rockets or create a new one by yourself. Then ").place(x=560,y=440)
        self.message=Label(self,text="you'll have to choose a mission (GTO,LEO or the moon) and the ").place(x=560,y=460)
        self.message=Label(self,text="pitch angle.").place(x=560,y=480)
        self.message=Label(self,text="You can also choose if you want the same axes scale for x and z ").place(x=560,y=500)
        self.message=Label(self,text="or an adapted one. ").place(x=560,y=520)

        varI = IntVar()
        self.check=Checkbutton(self,text="axis scale factor",variable=varI).place(x=50,y=650)

        var_pitch_angle = DoubleVar()
        self.message=Label(self,text="pitch angle").place(x=220,y=650)
        pitch_angle = Entry(self, textvariable=var_pitch_angle, width=5)
        pitch_angle.place(x=310,y=650)
        var_pitch_angle.set(1.4)







fenetre=Tk()
fenetre.title("Choose your rocket")
fenetre.geometry("1000x1800+300+200")
interface=Interface(fenetre)



picture_falcon=PhotoImage(file="falcon.png")
label_falcon=Label(fenetre,image=picture_falcon).place(x=820,y=50)

picture_miura=PhotoImage(file="Miura.png")
label_falcon=Label(fenetre,image=picture_miura).place(x=660,y=50)

picture_ariane=PhotoImage(file="ariane.png")
label_ariane=Label(fenetre,image=picture_ariane).place(x=500,y=50)

picture_saturn=PhotoImage(file="saturn.png")
label_saturn=Label(fenetre,image=picture_saturn).place(x=340,y=50)

picture_soyuz=PhotoImage(file="soyuz.png")
label_soyuz=Label(fenetre,image=picture_soyuz).place(x=180,y=50)

picture_sputnik=PhotoImage(file="sputnik.png")
label_sputnik=Label(fenetre,image=picture_sputnik).place(x=20,y=50)




fenetre.mainloop()
