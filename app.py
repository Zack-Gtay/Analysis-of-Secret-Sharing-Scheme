import os
import tss
from tss import Hash
import base64
import time

secret = "Hello, I am here for you. Do your best to get closer. There is no reason to live outside the horizon of help."
iterations = 10  # Number of iterations for averaging

# Define the values of s and t to test
s_values = [3, 4, 5]
t_values = [2, 3]

# Function to store shares in folders based on s and t
def store_shares(s, t, shares):
    folder_name = f"shares_s{s}_t{t}"
    os.makedirs(folder_name, exist_ok=True)
    for i, share in enumerate(shares):
        with open(f"{folder_name}/share_{i+1}.txt", "wb") as f:
            f.write(base64.b64encode(share))

# Function to reconstruct secret from stored shares
def retrieve_shares(s, t):
    folder_name = f"shares_s{s}_t{t}"
    shares = []
    for filename in os.listdir(folder_name):
        with open(os.path.join(folder_name, filename), "rb") as f:
            shares.append(base64.b64decode(f.read()))
    return shares

# Iterate through each combination of s and t
for s in s_values:
    for t in t_values:
        total_share_time = 0
        total_recover_time = 0

        for _ in range(iterations):
            # Measure time to share
            start_share = time.time()
            shares = tss.share_secret(t, s, secret, Hash.NONE)
            end_share = time.time()
            share_time = end_share - start_share
            total_share_time += share_time

            # Store shares in folders
            store_shares(s, t, shares)

            # Measure time to recover
            start_recover = time.time()
            retrieved_shares = retrieve_shares(s, t)
            reconstructed_secret = tss.reconstruct_secret(retrieved_shares[0:t])
            end_recover = time.time()
            recover_time = end_recover - start_recover
            total_recover_time += recover_time

        # Calculate average times
        avg_share_time = total_share_time / iterations
        avg_recover_time = total_recover_time / iterations

        # Print Avg Time to Share and Avg Time to Recover
        print(f"Avg Time to Share (s={s}, t={t}): {avg_share_time} seconds")
        print(f"Avg Time to Recover (s={s}, t={t}): {avg_recover_time} seconds")
