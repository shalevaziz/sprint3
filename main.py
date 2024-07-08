import os

TOP_SECRET_FOLDER_PATH = 'C:\Users\Public\Documents\top_secret'

top_secret_files = os.listdir(TOP_SECRET_FOLDER_PATH)

for file in top_secret_files:
    with open(os.path.join(TOP_SECRET_FOLDER_PATH, file), 'r') as f:
        print(f.read())

