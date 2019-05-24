import numpy as np
import pandas as pd


def gm_simulation(distribution=(0,1), decision="v_h", ratio=0.2, uninformed=0.5, 
                  startvalue=0.5, iterations = 500, seed=5000, epsilon=10**-5, 
                  shockperiod = None, shock={}):
    """Simulates a simple Glosten-Milgrom model with binary distributed security.
    Repeats simulation until either the threshold parameter is reached or the maximum
    number of simulations is reached.
    
    Args:
        distribution (tuple): upper and lower value for the security. Default (0,1)
        decision (string): selecting the true value of the security. Default "v_h". options = ("v_h", "v_l")
        
        ratio (float): Ratio of informed traders on the market. Default 0.2
        uninformed (float): Chance to receieve buy order from uninformed trader. Default 0.5
        startvalue (float): Dealer's start belief about the value of the security. Default 0.5
        
        iterations (int): Maximum number of iterations run by the simulation. Default 500
        seed (int): Seed used to generate random numbers. Default 5000
        epsilon (float): Threshold parameter. Default 10**-5
        
        shockperiod (int): Selects which iteration the shock is introduced. Default None
        shock (dict): Type of shock introduced. Default {}
        
    Returns:
        dataframe (pandas dataframe): dataframe containing the simulation data for all iterations
        values (dictionary): dictionary containing parameter values from the final iteration.
    """
    
    #setting values
    v_l, v_h = distribution
    pi = ratio
    beta_b = uninformed
    beta_s = 1-beta_b
    shock = shock
    
    #determine realized value of v
    v = decision
    
    #allocate space to save simulation data
    values={}
    ratiovalues = []
    iteration = []
    thetavalues = np.empty(iterations)
    muvalues = np.empty(iterations)
    askvalues = np.empty(iterations)
    bidvalues = np.empty(iterations)
    gapvalues = np.empty(iterations)
    pivalues = np.empty(iterations)
    decisionvalues = np.empty(iterations)
    
    #saving startvalue of dealer beliefs
    thetavalues[0]=startvalue
    
    #setting simulation settings
    theta_t1 = startvalue
    N = iterations
    np.random.seed(seed)
    
    #setting break index
    break_index = 0
    
    #simulation loop
    for i in range(N):
        
        #check if in shockperiod
        if i==shockperiod:
            if shock != {}:
                
                #apply changes if shock is private only
                if "Public" not in shock:
                    if shock["Private"]==1:
                        v="v_h"
                    if shock["Private"]==0:
                        v="v_l"
                
                #apply changes if shock is public only
                elif "Private" not in shock:
                    v_l, v_h = shock["Public"] 
                    v = decision
                
                #apply changes if shock is public and private
                else:
                    v_l, v_h = shock["Public"]
                    if shock["Private"]==1:
                        v="v_h"
                    if shock["Private"]==0:
                        v="v_l"
        
        #get v value from v_h or v_l
        if v=="v_h":
            v=v_h
        elif v=="v_l":
            v=v_l
            
        #calculate expected value of security
        mu_t1 = theta_t1*v_h+(1-theta_t1)*v_l
        muvalues[i] = mu_t1
        
        #calculate markup/discount
        s_a = (pi*theta_t1*(1-theta_t1))/(pi*theta_t1+(1-pi)*beta_b)*(v_h-v_l)
        s_b = (pi*theta_t1*(1-theta_t1))/(pi*(1-theta_t1)+(1-pi)*beta_s)*(v_h-v_l)
        
        #calculate ask/bid price
        askvalues[i] = a_t = mu_t1 + s_a
        bidvalues[i] = b_t = mu_t1 - s_b 
        
        #calculate gap
        gapvalues[i] = gap_t = a_t - b_t
        
        #determine trader type
        trader = np.random.binomial(1,pi)
        pivalues[i] = trader
        
        #Determine order type if trader is informed
        if trader == 1:

            if v == v_h:
                if v_h>a_t:
                    d_t=1
                    
            elif v == v_l:
                if v_l<b_t:
                    d_t=-1
                    
            else:
                d_t=0
                    
        #determine order type if trader is uninformed
        if trader == 0:
            
            #random draw of ordertype
            buysell = np.random.binomial(1,beta_b)
            if buysell == 1:
                d_t = 1
            else:
                d_t = -1
        
        decisionvalues[i] = d_t
        
        #update beliefs depending on order type
        if d_t == 1:
            theta_t = ((1+pi)*beta_b)/(pi*theta_t1+(1-pi)*beta_b)*theta_t1
            theta_t1 = theta_t
            
        elif d_t == -1:
            theta_t = ((1-pi)*beta_b)/(pi*(1-theta_t1)+(1-pi)*beta_b)*theta_t1
            theta_t1 = theta_t
        
        #saving theta values with lag of 1
        if i<iterations-1:
            thetavalues[i+1] = theta_t
        
        #saving ratio and iteration values
        ratiovalues.append(str(ratio))
        iteration.append(int(i))
        
        #off by one error
        break_index=i+1
        
        #save values and break loop if threshold or maximum iteration is reached
        if gap_t<epsilon or i == N-1:
            values.update({"Theta": theta_t,"Bid": b_t, "Ask": (a_t), "Mu": mu_t1, "Equilibrium period": break_index-1})
            break
            
    #adding all simulation data to single dataframe
    dataframe = pd.DataFrame()
    dataframe["Iteration"] = iteration
    dataframe["ratio"] = ratiovalues
    dataframe["theta"] = thetavalues[0:break_index]
    dataframe["mu"] = muvalues[0:break_index]
    dataframe["ask"] = askvalues[0:break_index]
    dataframe["bid"] = bidvalues[0:break_index]
    dataframe["spread"] = gapvalues[0:break_index]
    dataframe["trader"] = pivalues[0:break_index]
    dataframe["order"] = decisionvalues[0:break_index]
    
    return dataframe, values