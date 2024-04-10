import os
import subprocess

branches = ['main', 'dev', 'SIT']

def update_file_content(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    updated_lines = []
    for line in lines:
        if "webserver-module" in line:
            updated_lines.append(line.replace('ref=v1.1', 'ref=v1.2'))
        else:
            updated_lines.append(line)
    
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

def git_diff(branch):
    subprocess.run(['git', 'diff'], check=True)

def git_add_commit(branch):
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Updated the webserver module version from v1.1 to v1.2'], check=True)

def main():
    global branches
    if not branches:
        branches_input = input("Enter branch names separated by commas: ")
        branches = branches_input.split(',')
    
    for branch in branches:
        subprocess.run(['git', 'checkout', branch.strip()], check=True)

        directory = os.getcwd()
        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.tf'):
                    file_path = os.path.join(root, file_name)
                    update_file_content(file_path)
        print(f"Git diff for branch {branch.strip()}:")
        git_diff(branch.strip())
        git_add_commit(branch.strip())

if __name__ == "__main__":
    main()
