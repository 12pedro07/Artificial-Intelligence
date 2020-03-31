import matplotlib.pyplot as plt
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

som = SOM(inputs, weights, sigma=sigma, learning_rate=learning_rate, sigma_decrease_rate=sigma_decrease_rate, epochs=10)
som.train(ignore_hk=True, display=True)
points = [[1,4],
          [6,2],
          [1,3],
          [5,1],
          [4,0],
          [0,4],
          [3,4]]

predictions = som.predict(points, ignore_hk=True, display=True)

p, m = som.prediction_line(display=True)

def med(points, p, m):
    y=[]
    for point in points:
        y.append(m*(point - p[0]) + p[1])
    return y

plt.grid()
for point, prediction in zip(points, predictions):
    x, y = point
    color, label = ("blue", "cluster 1") if prediction[0] == 1 else ("red", "cluster 2")
    plt.scatter(x,y,c=color,label=label,s=30)
plt.plot(range(6), med(range(6), p, m))
plt.show()
