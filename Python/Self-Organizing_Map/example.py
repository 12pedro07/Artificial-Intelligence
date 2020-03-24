from som import SOM

inputs  = [[1,4],
           [6,2],
           [1,3],
           [5,1],
           [4,0],
           [0,4]]

weights = [[5,0],
           [-1,4]]

sigma   = 1

learning_rate = 1

sigma_decrease_rate = 0

som = SOM(inputs, weights, sigma=sigma, learning_rate=learning_rate, sigma_decrease_rate=sigma_decrease_rate)
som.train()
