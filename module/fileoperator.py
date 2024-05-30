import os
import re
import inspect

class BaseOperator:
    
    @classmethod
    def set_path(cls, work_directory: str, target_path: str):
        """
        원하는 디렉토리 경로를 설정하는 함수
        
        > work_direcotory : 최상위 작업 디렉토리(명령어 실행 기준)
        > target_path : 최상위 작업 디렉토리를 제외한 나머지 하위 경로
        """
        try:
            work_dir_index = os.getcwd().index(work_directory)
            return os.getcwd()[:work_dir_index] + work_directory + target_path
        
        except Exception as e:
            func_name = inspect.currentframe().f_code.co_name
            return print(e, f"{func_name} is not working ")
        
    @classmethod
    def get_file_list(cls, target_directory: str, file_format: tuple):
        """
        목표 디렉토리로부터 xlsx, xlsm 형식의 파일 이름을 가져와 리스트 생성하는 함수
        
        > target_dircetory : 가져올 파일이 담긴 디렉토리
        > file_format : 가져올 파일의 형식(튜플 형태로 나열)
        """
        try:
            all_file_list = os.listdir(target_directory)
            return sorted([file for file in all_file_list if file.endswith(file_format)])        
            
        except Exception as e:
            func_name = inspect.currentframe().f_code.co_name
            return print(e, f"{func_name} is not working ")
        
    @classmethod
    def selecting_list(cls, target_list: list, keywords: list):
        """ 
        리스트에서 키워드 선택 후 정렬해서 반환하는 함수
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            return sorted(
                [
                    target_name for target_name in target_list 
                    if any(keyword in target_name for keyword in keywords)
                ]
            )
        except Exception as e:
            return print(e, f"{func_name} is not working ")
        
    @classmethod
    def clearing_list(cls, target_list: list, except_keyword: list):
        """ 
        리스트에서 키워드 제외 후 정렬해서 반환하는 함수
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            return sorted(
                [
                    target_name for target_name in target_list 
                    if not any(keyword in target_name for keyword in except_keyword)
                ]
            )
        except Exception as e:
            return print(e, f"{func_name} is not working ")
    
    def find_variable(text: str):
        """
        인스턴스 변수에서 원하는 문자열이 포함된 변수를 딕셔너리로 저장
        
        > text: 인스턴스 변수 중 찾고싶은 문자열
        """
        try:
            variable_dict = dict()
            for var_name, var_value in self.__dict__.items():
                if text in var_name:
                    variable_dict[var_name] = var_value             
            return variable_dict
        
        except Exception as e:
            func_name = inspect.currentframe().f_code.co_name
            return print(e, f"{func_name} is not working ")
        
    def execute_for(iteration: list, *methods: callable):
        """
        여러개의 함수를 가변인자로 받아 리스트의 반복만큼 실행하는 함수
        
        > iteration : for문을 반복할 리스트
        > method : for문 내부에서 반복 실행될 함수(갯수 조절 가능)
        
        >>> instance.execute_for(
            iteration_list,
            (method_1, (params)),
            (method_2, (params)),
            )
        """
        func_name = inspect.currentframe().f_code.co_name
        
        try:
            for idx, _ in enumerate(iteration):
                idx = idx
                self.iter_value = _
                print(f"============ {_} ===============")
                
                for method, params in methods:
                    method(*params)
                
        except Exception as e:
            return print(e, f"{func_name} is not working ")
    
    @staticmethod        
    def replace_keywords_in_files(directory, keyword, replacement):
        
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".sql"):
                    filepath = os.path.join(root, filename)
                    
                    with open(filepath, "r") as file:
                        file_content = file.read()
                        
                    updated_content = file_content.replace(keyword, replacement)

                    with open(filepath, "w") as file:
                        file.write(updated_content)
    
    @staticmethod
    def find_directory(start_path: str, target_directory_name: str, visited=None, founded=False):
        
        if os.path.isdir(start_path):
            curr_dir = start_path
        else:
            curr_dir = os.path.dirname(start_path)
        
        if visited == None:
            visited = list()
            try_num = 1
            visited.append(try_num)
        
        while founded == False:
            
            tried_num = visited[0]
            print(f"{tried_num}th try to find {target_directory_name}")
            
            if tried_num > 4:
                print("Can not find target directory in short time")
                break
            
            for root, dirs, files in os.walk(curr_dir):
                
                if root in visited:
                    continue
                else:
                    visited.append(root)
                
                    if os.path.basename(root) == target_directory_name:
                        founded = True
                        print(f"{target_directory_name} founded")
                        return root
            
            visited[0] = tried_num + 1
            
            upper_dir = os.path.dirname(curr_dir)
            return BaseOperator.find_directory(upper_dir, target_directory_name, visited)
        
if __name__ == "__main__":
    
    curr_path = os.path.abspath(__file__)
    dir = BaseOperator.find_directory(
        start_path=curr_path,
        target_directory_name='lotto_data'
    )
    
    # visited = set()
    
    # visited.add(0)
    # visited.add(1)
    # print(visited[0])
    