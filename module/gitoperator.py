import subprocess
import os

from fileoperator import BaseOperator

class GitOperator(BaseOperator):
    
    def __init__(
        self,
        git_repo_url:str = None,
        pulling_dir_path:str = None
    ):
        
        self.git_repo_url = git_repo_url
        self.pulling_dir_path = pulling_dir_path
        
    def git_running(self, bash:str):
        
        splited_bash = bash.split()
        
        try:
            result = subprocess.run(
                splited_bash,
                check=True,
                text=True,
                capture_output=True
            )  
            if 'Already up to date.' in result.stdout:
                pass
            else:
                print("Output:\n", result.stdout)
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            print("Error:\n", e.stderr)
            return e.stderr
            
    def git_remote_check(self):
        bash = f'git remote -v'
        out = self.git_running(bash)
        return out
            
    def git_clone(self):
        bash = f'git clone {self.git_repo_url}'
        self.git_running(bash)
    
    def git_pull(self, repo_name:str, branch_name:str):
        
        original_dir = os.getcwd()
        os.chdir(self.pulling_dir_path)
        
        remote_check_result = self.git_remote_check()
        
        if self.git_repo_url in remote_check_result:
            bash = f'git pull {repo_name} {branch_name}'
            self.git_running(bash)
            os.chdir(original_dir)
        else:
            return print(f"Can't pull because git don't remoted to {self.git_repo_url}")
        

if __name__ == "__main__":
    
    
    git_repo = 'https://github.com/happylie/lotto_data.git'
    clone_dir = BaseOperator.set_path(
        work_directory='sampling',
        target_path='/lotto_data'
    )
    
    lotto_git = GitOperator(
        git_repo_url=git_repo,
        pulling_dir_path=clone_dir        
    )
    # lotto_git.git_clone()
    lotto_git.git_pull('origin', 'main')
    
    