import os
import hashlib
import shutil
from datetime import datetime

class VersionControlSystem:
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.repo_path = os.path.join(os.getcwd(), repo_name)
        self.objects_path = os.path.join(self.repo_path, 'objects')
        self.logs_path = os.path.join(self.repo_path, 'logs')

    def init_repo(self):
        if os.path.exists(self.repo_path):
            print(f"Repository {self.repo_name} already exists.")
            return
        os.makedirs(self.objects_path)
        os.makedirs(self.logs_path)
        print(f"Repository {self.repo_name} initialized.")

    def add(self, filename):
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            return
        file_hash = self.hash_file(filename)
        file_version = os.path.join(self.objects_path, file_hash)
        shutil.copy(filename, file_version)
        print(f"File {filename} added to the repository.")

    def commit(self, message):
        commit_id = hashlib.sha1(message.encode() + str(datetime.now()).encode()).hexdigest()
        commit_log = os.path.join(self.logs_path, commit_id + '.log')
        with open(commit_log, 'w') as log_file:
            log_file.write(f"Commit message: {message}\n")
            log_file.write(f"Timestamp: {datetime.now()}\n")
        print(f"Commit {commit_id} created.")

    def log(self):
        logs = [f for f in os.listdir(self.logs_path) if f.endswith('.log')]
        logs.sort()
        for log_file in logs:
            with open(os.path.join(self.logs_path, log_file)) as log:
                print(log.read())

    def checkout(self, commit_id):
        commit_log = os.path.join(self.logs_path, commit_id + '.log')
        if not os.path.exists(commit_log):
            print(f"Commit {commit_id} does not exist.")
            return
        with open(commit_log) as log_file:
            print(f"Checking out commit {commit_id}:")
            print(log_file.read())

    def hash_file(self, filename):
        sha1 = hashlib.sha1()
        with open(filename, 'rb') as file:
            while chunk := file.read(4096):
                sha1.update(chunk)
        return sha1.hexdigest()

# Example usage:
if __name__ == "__main__":
    v = VersionControlSystem("my_repo")
    v.init_repo()  # Initialize the repo
    v.add("file1.txt")  # Add a file
    v.commit("Initial commit")  # Commit the changes
    v.log()  # Show the commit logs

