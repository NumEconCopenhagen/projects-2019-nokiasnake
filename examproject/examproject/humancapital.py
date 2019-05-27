import numpy as np
import pandas as pd

class HumanCapitalAccumulation:
    """Class containing several key functions to solve the Human Capital problem"""
    def __init__(self, rho, beta, gamma, w, b, delta, h_vec):
        """__init__ constructor for HumanCapitalAccumulation class

        Args:
            rho (float): utility preference
            beta (float): discount factor
            gamma (float): disutility of work
            w (float): wage
            b (float): unemployment benefits
            delta: random extra human capital
            h_vec: human capital vector
        """        
        
        self.rho = rho
        self.beta = beta
        self.gamma = gamma
        self.w = w
        self.b = b
        self.delta = delta
        self.h_vec = h_vec
        
    def consumption(self,l_t, h_t):
        """consumption function
        
        Args:
            l_t (int): indicator of work
            h_t (float): human capital

        Returns:
            c_t (float): consumption level
        """

        #calculate consumption gained from work
        if l_t==1:
            c_t = self.w*h_t*l_t
        
        #calculate consumption from unemployment
        if l_t==0:
            c_t = self.b
            
        return c_t
            
    def utility(self,l_t,h_t):
        """Utility function

        Args:
            l_t (int): indicator of work
            h_t (float): human capital

        Returns:
            u_t (float): utility level

        """
        #calculate utility from consumption function
        u_t = self.consumption(l_t, h_t)**(1-self.rho)/(1-self.rho) - self.gamma*l_t
        
        return u_t
    
    def humancapital(self, l_t, h_t, prob):
        """Human capital accumulation function

        Args:
            l_t (int): indicator of work
            h_t (float): human capital
            prob (float): chance of gaining extra human capital


        Returns:
            h_2 (float): human capital in period 2

        """
        #calculate human capital in period 2
        h_2 = h_t + l_t + prob*self.delta
        
        return h_2

    def period1(self,l_t,h_t):
        """utility maximation faced in period 1

        Args:
            l_t (int): indicator of work
            h_t (float): human capital

        Returns:
            v1 (float): expected quality of living for both periods
        
        """
        #calculate humancapital acculumation
        h2 = self.humancapital(h_t, l_t, 0.5)
        
        #calculate utility
        v1 = self.utility(l_t, h_t) + self.beta * self.utility(l_t,h2)
        
        return v1
    
    def period2(self, l_t, h_t):
        """utility maximation faced in period 2

        Args:
            l_t (int): indicator of work
            h_t (float): human capital

        Returns:
            v2 (float): expected quality of living in period 2
        
        """
        #calculate utility
        v2 = self.utility(l_t, h_t)
        
        return v2
    
    def solution(self, period):
        """solves the model with regard to utility maximizing behaviour

        Args:
            period (function): period utility maximation function

        Returns:
            data (dataframe): dataframe containing utility for all scenarios
        """
        #allocate space
        humancap = []
        optimallabour = []
        optimalutil = []
        workutil = []
        unemputil = []
        
        #for human capital level 
        for h in self.h_vec:
            #create list containing work and unemp utility maximation
            list = [period(0, h), period(1, h)]
            
            #if work utility if higher, saves work as optimal
            if list[1]>list[0]:
                optimallabour.append(1)

            #else save unemployment as optimal
            else:
                optimallabour.append(0)
            
            #append data to lists 
            optimalutil.append(max(list))
            workutil.append(list[1])
            unemputil.append(list[0])
            humancap.append(h)
        
        #save lists to dataframe
        data = pd.DataFrame()
        data["h"]=humancap
        data["best l"]=optimallabour
        data["best u"]=optimalutil
        data["work u"]=workutil
        data["unemp u"]=unemputil
        
        return data