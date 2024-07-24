import numpy as np

def bullseye(k):
    L=[]
    Points=[]
    while(len(L) < k):
        x = np.random.uniform(-1,1)
        y = np.random.uniform(-1,1)
        if x**2 + y**2 <= 1:
            L.append(np.sqrt(x**2 + y**2))
            Points.append((x,y))
    L.sort()
    return L,Points

def bullseye_experiment(darts,trials):
    L = []
    for i in range(trials):
        L.append(min(bullseye(darts)[0]))
    return (np.mean(L))

print(bullseye_experiment(100,100000))