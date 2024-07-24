import numpy as np
import pandas as pd

# Load dataset
data = pd.read_csv(r"D:\AIVS-Projects\3. Recommender System\data.csv")

# Inspect the dataset
print(data.columns)
print(data.head())

# Assuming the first column is the person and the rest are the people they found impressive
person_column = data.columns[0]
other_columns = data.columns[1:]
# Create a list of all unique students

students = list(set(data[person_column]).union(*[set(data[col].dropna()) for col in other_columns]))

n = len(students)
student_index = {name: idx for idx, name in enumerate(students)}

# Create an adjacency matrix
adj_matrix = np.zeros((n, n))

for _, row in data.iterrows():
    person_a = row[person_column]
    if pd.isna(person_a):
        continue
    for person_b in row[other_columns].dropna():
        if person_b in student_index:
            adj_matrix[student_index[person_a], student_index[person_b]] = 1         

# Matrix factorization parameters
k = 10  # Number of latent features
alpha = 0.002  # Learning rate
beta = 0.02  # Regularization parameter
iterations = 1000  # Number of iterations

# Initialize U and V matrices
U = np.random.rand(n, k)
V = np.random.rand(k, n)

# Training using gradient descent
for iter in range(iterations):
    for i in range(n):
        for j in range(n):
            if adj_matrix[i, j] > 0:
                error = adj_matrix[i, j] - np.dot(U[i, :], V[:, j])
                for r in range(k):
                    U[i, r] += alpha * (2 * error * V[r, j] - beta * U[i, r])
                    V[r, j] += alpha * (2 * error * U[i, r] - beta * V[r, j])

# Predicted adjacency matrix
predicted_matrix = np.dot(U, V)

# Apply threshold to determine impressions
threshold = 0.8
predicted_impressions = (predicted_matrix > threshold).astype(int)
print(predicted_impressions)
print(predicted_matrix)

# Output predictions
predicted_links = []
for i in range(n):
    for j in range(n):
        if i!=j and adj_matrix[i, j] == 0 and predicted_impressions[i, j] > 0:
            predicted_links.append((students[i], students[j], predicted_matrix[i, j]))

# Save predictions to CSV
output_path = r'D:\AIVS-Projects\3. Recommender System\predicted_links.csv'
predictions_df = pd.DataFrame(predicted_links, columns=['Person A', 'Person B', 'Predicted Strength'])
predictions_df.to_csv(output_path, index=False)

print(f"Predictions saved to {output_path}")
