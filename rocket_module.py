import numpy as np
import matplotlib as plt
import pandas as pd

class rocket():
    def __init__(self, Name, Year, Country, Mission, Stage_Number, Height, Lift_off_mass,Payload_mass,S1_length,S1_diameter,S1_thrust,S1_Isp,S1_m0,S1_mp,S2_length,S2_diameter,S2_thrust,S2_Isp,S2_m0,S2_mp):
        self.Name = Name
        self.Year = Year
        self.Country = Country
        self.Mission = Mission
        self.Stage_Number = int(Stage_Number)
        self.Height = float(Height)
        self.Lift_off_mass = float(Lift_off_mass)
        self.Payload_mass = float(Payload_mass)
        self.S1_length = float(S1_length)
        self.S1_diameter = float(S1_diameter)
        self.S1_thrust = float(S1_thrust)
        self.S1_Isp = float(S1_Isp)
        self.S1_m0 = float(S1_m0)
        self.S1_mp = float(S1_mp)
        self.S2_length = float(S2_length)
        self.S2_diameter = float(S2_diameter)
        self.S2_thrust = float(S2_thrust)
        self.S2_Isp = float(S2_Isp)
        self.S2_m0 = float(S2_m0)
        self.S2_mp = float(S2_mp)

    def trajectory(self,theta,Dt):
        R=6371000 #earth radius
        G_constant=6.674e-11
        m_earth=5.972e24
        t_tot=100000
        t=Dt
        g=9.81
        L_m0=[self.Lift_off_mass,self.Lift_off_mass-self.S1_m0]
        L_mp=[self.S1_mp]
        if self.Stage_Number==1: #speciale case for 1 stage rockets
            L_m0[-1]=self.Payload_mass
        L_sp=[self.S1_Isp]
        L_T=[self.S1_thrust]
        Z,X,G,A,T,K=[0.1],[0],[np.arctan(np.tan(theta)-L_m0[0]*g/L_T[0]/np.cos(theta))],[0],[0],[0] #initilaisation qui respectent le while pour le 1er instant
        if self.Stage_Number==2: #end of initialisation for two stage rockets
            L_m0+=[L_m0[-1]-self.S2_m0]
            L_mp+=[self.S2_mp]
            L_sp+=[self.S2_Isp]
            L_T+=[self.S2_thrust]
        L_mp+=[L_m0[-1]]#to ensure that m>L_m0[k]-L_mp[k] always true during the free fall
        Vx_extinction=0 #initilisation of engines cut-off speeds
        Vz_extinction=0
        m=self.Lift_off_mass
        k=0
        X0,Z0=0,0
        T_separation=0
        for k in range(self.Stage_Number+1): #iterates k as the different phase of the flight (nb_stage + free fall)
            altitude=Z[-1]
            g=G_constant*m_earth/(R+altitude)/(R+altitude)#gravitationnal acceleration
            while m>L_m0[k]-L_mp[k] and altitude>0 :
                if k<self.Stage_Number: #propulsion phase
                    m=L_m0[k]-L_T[k]*(t-T_separation)/L_sp[k]/g #mass
                    C=L_m0[k]*L_sp[k]*L_sp[k]*g*g/L_T[k]*(1-m/L_m0[k]*(np.log(L_m0[k]/m)+1)) #a constant that appears in z(t) and y(t)
                    v_z=Vz_extinction+L_sp[k]*g*np.log(L_m0[k]/m)*np.sin(theta)-g*(t-T_separation)
                    v_x=Vx_extinction+L_sp[k]*g*np.log(L_m0[k]/m)*np.cos(theta)
                    G+=[np.arctan(v_z/v_x)] #pitch angle
                else:
                    DX=Vx_extinction*(t-T_separation)# ballistic fall
                    C=0
                    G+=[np.arctan((Vz_extinction-g*(t-T_separation))/Vx_extinction)]
                tb_prec=int(T_separation/Dt)
                DX=Vx_extinction*(t-T_separation)
                DZ=Vz_extinction*(t-T_separation)-g/2*(t-T_separation)*(t-T_separation)
                X+=[X0+ C*np.cos(theta)+DX]
                Z+=[Z0+ C*np.sin(theta)+DZ]
                A+=[theta-G[-1]]
                t+=Dt
                T+=[t]
                K+=[k]
                altitude=Z[-1]

            if k<=self.Stage_Number: #cas où la fusée est dejà en chute libre
                Vx_extinction=v_x
                Vz_extinction=v_z
            X0=X[-1]
            Z0=Z[-1]
            T_separation=t
        return(X,Z,G,A,T,K)



def plotAndSaveFig(myRocket):

    axes = plt.gca()  #define the environment


    axes.set_frame_on(False)
    axes.xaxis.set_visible(False)
    axes.yaxis.set_visible(False)

    #we want the lenght < 1 because our plot is from 0 to 1
    H = myRocket.Height

    h = myRocket.Height/H           
    l1 = myRocket.S1_length/H
    l2 = myRocket.S2_length/H
    d1 = myRocket.S1_diameter/H
    d2 = myRocket.S2_diameter/H

    #-------------------------------------

    #controle the case where there is only one stafe because then d2 = l2 = nan
    if(myRocket.Stage_Number == 1):
        d2 = d1
        l2 = 0

    #base of the rocket
    x = 0.5
    y = 0

    #define point of the rocket
    A = [x - d1/2, y]
    B = [x + d1/2, y]
    C = [x - d1/2, y + l1]
    D = [x + d1/2, y + l1]
    E = [x - d2/2, y + l1]
    F = [x + d2/2, y + l1]
    G = [x + d2/2, y + l1 + l2]
    H = [x - d2/2, y + l1 + l2]
    I = [x, y + h]
    #----------------------



    #plot a line between each point we want
    axes.add_artist(mat.lines.Line2D((A[0], C[0]), (A[1], C[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((A[0], B[0]), (A[1], B[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((D[0], B[0]), (D[1], B[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((C[0], D[0]), (C[1], D[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((E[0], F[0]), (E[1], F[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((E[0], H[0]), (E[1], H[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((G[0], F[0]), (G[1], F[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((G[0], H[0]), (G[1], H[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((I[0], G[0]), (I[1], G[1]), color = 'red'))
    axes.add_artist(mat.lines.Line2D((H[0], I[0]), (H[1], I[1]), color = 'red'))

    plt.savefig(myRocket.Name + ".png")
    plt.show()


def rot(theta,M,O): #rotation of theta(radiant) around O becausse we want to turn the rocket when plotting the animation
    x = M[0] - O[0]
    y = M[1] - O[1]
    M[0] = x*np.cos(theta) - y*np.sin(theta) + O[0]
    M[1] = x*np.sin(theta) + y*np.cos(theta) + O[1]


def newLine(A,B,plotX,plotY):  #an expensive way to plot a line but the precednt way don't work (or i don't know how) with animation af tkinter
    i = 0
    for i in range (101):
        plotX.append(A[0] + i*(B[0]-A[0])/100)
        plotY.append(A[1] + i*(B[1]-A[1])/100)


def plotRocket(myRocket,theta,x,y,dX,dY): #same method as plotAndSaveFig but this time there is a rotation and an origine

    plotX = []
    plotY = []


    H = myRocket.Height
    L1 = myRocket.S1_length
    L2 = myRocket.S2_length
    D1 = myRocket.S1_diameter
    D2 = myRocket.S2_diameter

    dilatationX = 3*H/dX
    dilatationY = 3*H/dY

    h = H/dilatationY
    l1 = L1/dilatationY
    l2 = L2/dilatationY
    d2 = D2/dilatationX
    d1 = D1/dilatationX

    if(myRocket.Stage_Number == 1):
        d2 = d1
        l2 = 0

    A = [x - d1/2, y]
    B = [x + d1/2, y]
    C = [x - d1/2, y + l1]
    D = [x + d1/2, y + l1]
    E = [x - d2/2, y + l1]
    F = [x + d2/2, y + l1]
    G = [x + d2/2, y + l1 + l2]
    H = [x - d2/2, y + l1 + l2]
    I = [x, y + h]

    rot(theta,A,[x,y])
    rot(theta,B,[x,y])
    rot(theta,C,[x,y])
    rot(theta,D,[x,y])
    rot(theta,E,[x,y])
    rot(theta,F,[x,y])
    rot(theta,G,[x,y])
    rot(theta,H,[x,y])
    rot(theta,I,[x,y])

    newLine(A,B,plotX,plotY)
    newLine(A,C,plotX,plotY)
    newLine(B,D,plotX,plotY)
    newLine(B,D,plotX,plotY)
    newLine(C,D,plotX,plotY)
    newLine(E,F,plotX,plotY)
    newLine(E,H,plotX,plotY)
    newLine(G,F,plotX,plotY)
    newLine(G,H,plotX,plotY)
    newLine(G,I,plotX,plotY)
    newLine(H,I,plotX,plotY)

    return plotX,plotY


class notARocket(ValueError):
    pass


def read(Name):
    ListRocket = ["Miura 1","Sputnik","Soyuz","Saturn V","Ariane 5","Falcon 9"]
    if not (Name in ListRocket):
        raise notARocket('The name is not in the list of rockets')
    else:
        df = pd.read_csv('rocket_database.csv')
        ListName = df['Name']
        i = 0
        while(ListName[i] != Name):
            i += 1
        myRocket = rocket
        myRocket.Name = df['Name'][i]
        myRocket.Year = df['Year'][i]
        myRocket.Country = df['Country'][i]
        myRocket.Mission = df['Mission'][i]
        myRocket.Stage_Number = df['Stages number'][i]
        myRocket.Height = df['Height [m]'][i]
        myRocket.Lift_off_mass = df['Lift-off mass [tons]'][i]
        myRocket.Payload_mass = df['Payload mass [kg]'][i]
        myRocket.S1_length = df['S1 length [m]'][i]
        myRocket.S1_diameter = df['S1 diameter [m]'][i]
        myRocket.S1_thrust = df['S1 thrust [kN]'][i]
        myRocket.S1_Isp = df['S1 Isp [s]'][i]
        myRocket.S1_m0 = df['S1 m0 [tons]'][i]
        myRocket.S1_mp = df['S1 mp [tons]'][i]
        myRocket.S2_length = df['S2 length [m]'][i]
        myRocket.S2_diameter = df['S2 diameter [m]'][i]
        myRocket.S2_thrust = df['S2 thrust [kN]'][i]
        myRocket.S2_Isp = df['S2 Isp [s]'][i]
        myRocket.S2_m0 = df['S2 m0 [tons]'][i]
        myRocket.S2_mp = df['S2 mp [tons]'][i]
    return myRocket
