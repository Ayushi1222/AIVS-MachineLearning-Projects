import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load the data (replace with actual data loading)
# Assuming data is a pandas DataFrame with columns representing test scores
data = pd.read_csv(r'D:\AIVS-Projects\7. Data Compression\DataCompression1.csv')

# Normalize the data
data_normalized = (data - data.mean()) / data.std()

# Perform PCA
pca = PCA()
pca.fit(data_normalized)

# Explained variance
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

# Plot cumulative variance
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='--')
plt.title('Cumulative Variance Explained by Principal Components')
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative Variance Explained')
plt.grid(True)
plt.show()

# Determine the number of components that explain 95% of the variance
threshold = 0.95
num_components = np.argmax(cumulative_variance >= threshold) + 1

print(f'Number of tests that can be dropped: {data.shape[1] - num_components}')
print(data.shape[1])
# covariance banao then eigen values nikalni jitni eigen values 0 utne columns drop kr skte h 
