#import libraries
import numpy as np
import pandas as pd

class ExchangeEconomy:
    """Class containing several key functions to solve the exchange economy problem"""

    def __init__(self,betas, elist, N, p1, p2, gamma=None):
        """__init__ constructor for ExchangeEconomy class

        Args:
            betas (np.array): beta values
            elist (list of np.arrays): endowements list
            N (int): number of consumers
            p1 (float): price of good 1
            p2 (float): price of good 2 
            gamma (float): gamma in utility function
        """
        self.betas = betas
        self.elist = elist
        self.N = N
        self.p1 = p1
        self.p2 = p2
        self.gamma=gamma
        
    def budget(self):
        """budget function in the economy
        Args:
            none
        Returns:
            I (float): budget constraint
        """
        #allocate space
        I = np.empty(self.N)

        #calculate budgetconstraint
        I = self.p1 * self.elist[0] + self.p2 * self.elist[1] + self.elist[2]
            
        return I
    
    def demand_func(self):
        """demand function of the three goods
        Args:
            none
        Returns:
            x (array): consumer j's demand functions
        """

        #allocate space
        x = np.empty((3, self.N))
        #call budget function
        I = self.budget()
        
        #calculate demand function and save in array
        x[0] = self.betas[:,0] * I / self.p1
        x[1] = self.betas[:,1] * I / self.p2
        x[2] = self.betas[:,2] * I
        
        return x
    
    def excess_demand(self):
        """excess demand function for the economy
        Args:
            none
        Returns:
            z (array): excess demand of every good
        """
        #allocate space
        z = np.empty(3)

        #call demand function
        x = self.demand_func()
        
        #for good i, calculate excess demand
        for i in range(3):
            z[i] = np.sum(x[i])-np.sum(self.elist[i])
            
        return z        
    
    def walras(self, kappa, epsilon):
        """Solves the walras equilibrium for the economy
        Args:
            kappa (float): adjustment parameter
            epsilon (float): tolerance
        Returns:
            p1 (float): equilibrium price of good 1
            p2 (float): equilibrium price of good 2
        """

        #perform max N iterations
        for i in range(self.N):
            
            #call excess demand function
            z = self.excess_demand()
            
            #if excess demand is under threshold, break
            if abs(z[0])<epsilon and abs(z[1])<epsilon:
                break

            #else adjust prices
            else:
                self.p1 = self.p1+kappa*z[0]/self.N
                self.p2 = self.p2+kappa*z[1]/self.N

        return self.p1, self.p2
            
            
    def utility(self):
        """utility function for the economy
        Args:
            none
        Returns:
            util (array): utility for each consumer
        """
        #call demand function
        x = self.demand_func()

        #allocate space
        util = np.empty(self.N)
        
        #for consumer i calculate utility
        for i in range(self.N):
            util[i] = (x[0,i]**self.betas[i,0]*x[1,i]**self.betas[i,1]*x[2,i]**self.betas[i,2])**self.gamma
        
        return util