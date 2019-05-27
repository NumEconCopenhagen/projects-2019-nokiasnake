#import libraries
import numpy as np
import pandas as pd

class ASAD:
    """Class containing several key functions to solve the AS-AD problem"""
    def __init__(self, gamma, phi, h, b, alpha):
        """__init__ constructor for ASAD class

        Args:
            gamma (float): parameter for AS-AD
            phi (float): parameter for AS-AD
            h (float): parameter for AS-AD
            b (float): parameter for AS-AD
            alpha (float): parameter for AS-AD
        """
        self.gamma = gamma
        self.phi = phi
        self.h = h
        self.b = b
        self.alpha = alpha
        
    def sras(self, pi_t1, y_t, y_t1, s_t, s_t1):
        """SRAS function from the problem
        Args:
            pi_t1 (float): last periods inflation gap 
            y_t (float): current periods output gap
            y_t1 (float): last periods output gap
            s_t (float): current periods demand shock
            s_t1 (float): last periods demand shock

        Returns:
            pi_t (float): current periods inflation gap

        """
        #calculate inflation gap
        pi_t = pi_t1 + self.gamma * y_t + - self.phi * self.gamma * y_t1 + s_t - self.phi * s_t1
        
        return pi_t
    
    def ad(self, v_t, y_t):
        """AD function from the problem
        Args:
            v_t (float): current periods supply shock
            y_t (float): current periods output gap

        Returns:
            pi_t (float): current periods inflation gap

        """
        #calculate inflation gap
        pi_t = 1/(self.h*self.alpha)*(v_t-(1+self.b*self.alpha)*y_t)
        
        return pi_t
    
    def funcy(self,y_t1, s_t1, pi_t1, s_t, v_t, phi):
        """Calculates the equilibrium output gap for current period
        Args:
            y_t1 (float): last periods output gap
            s_t1 (float): last periods supply shock
            pi_t1 (float): last periods inflation gap
            s_t (float): current periods supply shock
            v_t (float): current periods demand shock
            phi (float): parameter for AS-AD curve

        Returns:
            y (float): current periods output gap
        """
        #calculate output gap
        y = ((self.alpha * self.gamma * self.h * phi * y_t1 
            + self.alpha * self.h * phi * s_t1 - self.alpha
            * self.h * pi_t1 - self.alpha * self.h * s_t + v_t)
            /(self.alpha * self.b + self.alpha * self.gamma 
            * self.h + 1))
        
        return y
        
    def funcpi(self, y_t1, s_t1, pi_t1, s_t, v_t, phi):
        """Calculates the equilibrium inflation gap for current period
        Args:
            y_t1 (float): last periods output gap
            s_t1 (float): last periods supply shock
            pi_t1 (float): last periods inflation gap
            s_t (float): current periods supply shock
            v_t (float): current periods demand shock
            phi (float): parameter for AS-AD curve

        Returns:
            pi (float): current periods inflation gap
        """
        #calculate inflation gap by calling funcy function
        pi = ((v_t - (self.alpha * self.b + 1) * self.funcy(y_t1, s_t1, pi_t1, s_t, v_t, phi=phi))
            /(self.alpha*self.h))
        
        return pi
        
    def ar_v(self, delta, v_t1, x_t):
        """Calculates autoregressive demand shock
        Args:
            delta (float): autoregressive parameter
            v_t1 (float): last periods demand shock
            x_t (float): random demand shock

        Returns:
            v_t (float): current periods demand shock
        """
        #calculate current period demand shock
        v_t = delta*v_t1 + x_t

        return v_t
    
    def ar_s(self, omega, s_t1, c_t):
        """Calculates autoregressive demand shock
        Args:
            omega (float): autoregressive parameter
            s_t1 (float): last periods supply shock
            c_t (float): random supply shock

        Returns:
            s_t (float): current periods demand shock
        """
        #calculate current period supply shock
        s_t = omega*s_t1 + c_t

        return s_t
    
    def ar_simulation(self, N, omega, delta, phi):
        """simulates the autoregressive AS-AD model
        Args:
            N (int):
            omega (float): autoregressive parameter
            delta (float): autoregressive parameter
            phi (float): parameter for AS-AD curve

        Returns:
            data (dataframe): dataframe containing simulation data
        """
        #save variable
        N = N

        #allocate space
        pi_vec = np.zeros(N)
        y_vec = np.zeros(N)
        s_vec = np.zeros(N)
        v_vec = np.zeros(N)
        c_vec = np.zeros(N)
        x_vec = np.zeros(N)
        i_vec = np.zeros(N)
        
        #setting start shock
        x_vec[1] = 0.1
        
        #for period i simulate AS-AD model
        for i in range(1, N):
            #save period number
            i_vec[i] = i

            #calculate demand/supply shock
            v_vec[i] = self.ar_v(delta, v_vec[i-1], x_vec[i])
            s_vec[i] = self.ar_s(omega, s_vec[i-1], c_vec[i])
            
            #calculate inflation/output gap
            y_vec[i] = self.funcy(y_t1 = y_vec[i-1], s_t1 = s_vec[i-1], pi_t1 = pi_vec[i-1], s_t = s_vec[i], v_t = v_vec[i], phi=phi)
            pi_vec[i] = self.funcpi(y_t1 = y_vec[i-1], s_t1 = s_vec[i-1], pi_t1 = pi_vec[i-1], s_t = s_vec[i], v_t = v_vec[i], phi=phi)
        

        #save arrays to dataframe
        data = pd.DataFrame()
        data["iteration"] = i_vec
        data["pi"] = pi_vec
        data["y"] = y_vec
        data["s"] = s_vec
        data["v"] = v_vec
        data["c"] = c_vec
        data["x"] = x_vec
        
        return data
    
    def stoch_simulation(self, N, omega, delta, sigmax, sigmac, seed, phi):
        """simulates the stochastic  AS-AD model
        Args:
            N (int):
            omega (float): autoregressive parameter
            delta (float): autoregressive parameter
            sigmax (float): demand variance
            sigmac (float): supply variance
            seed (int): seed for random draws
            phi (float): parameter for AS-AD curve

        Returns:
            data (dataframe): dataframe containing simulation data
        """
        
        #setting seed and sample
        np.random.seed(seed)
        N = N
        
        #allocate space
        pi_vec = np.zeros(N)
        y_vec = np.zeros(N)
        s_vec = np.zeros(N)
        v_vec = np.zeros(N)
        i_vec = np.zeros(N)
        
        #draw stochastic shocks
        c_vec = np.random.normal(0, sigmac, N)
        x_vec = np.random.normal(0, sigmax, N)

        #change initial value
        c_vec[0] = 0
        x_vec[0] = 0
        c_vec[1] = 0
        x_vec[1] = 0.1
        
        #for period i simulate AS-AD model
        for i in range(1, N):
            #save period number
            i_vec[i] = i

            #calculate demand/supply shock
            v_vec[i] = self.ar_v(delta, v_vec[i-1], x_vec[i])
            s_vec[i] = self.ar_s(omega, s_vec[i-1], c_vec[i])
            
            #calculate inflation/output gap
            yres =  self.funcy(y_t1 = y_vec[i-1], s_t1 = s_vec[i-1], pi_t1 = pi_vec[i-1], s_t = s_vec[i], v_t = v_vec[i], phi = phi)
            y_vec[i] = yres
            pires = self.funcpi(y_t1 = y_vec[i-1], s_t1 = s_vec[i-1], pi_t1 = pi_vec[i-1], s_t = s_vec[i], v_t = v_vec[i], phi = phi)
            pi_vec[i] = pires

        #save arrays to dataframe
        data = pd.DataFrame()
        data["iteration"] = i_vec
        data["pi"] = pi_vec
        data["y"] = y_vec
        data["s"] = s_vec
        data["v"] = v_vec
        data["c"] = c_vec
        data["x"] = x_vec
        
        return data