import json
import unicodedata
from text_ui import textInterface

#한글 정렬
def fill_str_with_space(input_s="", max_size=30, fill_char=" "):
    """
    - 길이가 긴 문자는 2칸으로 체크하고, 짧으면 1칸으로 체크함. 
    - 최대 길이(max_size)는 40이며, input_s의 실제 길이가 이보다 짧으면 
    남은 문자를 fill_char로 채운다.
    """
    l = 0 
    for c in input_s:
        if unicodedata.east_asian_width(c) in ['F', 'W']:
            l+=2
        else: 
            l+=1
    return input_s+fill_char*(max_size-l)

#일 클래스
class task():
    def __init__(self, title, deadLine = "없음", progress = 0, children = list()):
        
        self.title = title
        self.deadLine = deadLine
        self.children = children
        self.progress = progress
        self.add = '\n'
        
        self.isComplete = False
        
        if len(self.children) > 0:
            self.reflectProgress()

    def setComplete(self, progress: int):
        self.progress = progress

        if self.progress == 100:
            self.isComplete = True
        pass

    def reflectProgress(self):
        completeNum = 1
        
        for arg in self.children:
            if arg.isComplete == True:
                completeNum += 1
        #zero division error 방지
        if len(self.children) != 0:
            self.progress = int(completeNum/(len(self.children)) * 100)
        
        if self.progress == 100:
            self.isComplete = True
        pass

    def setChildrenProgress(self, index: int, progress: int):
        self.children[index].setProgress(progress)
        self.reflectProgress()

    def setDeadLine(self, deadLine):
        self.deadLine = deadLine

    def print(self, Id):
        text = self.add + fill_str_with_space(str(Id + 1) + "." + self.title)
        text += fill_str_with_space(" 기한: " + self.deadLine)
        text += " 진행률:" + str(self.progress) + "%"


        for i in range(0, len(self.children)):
                self.children[i].add = self.add + '    '
                text += (self.children[i].print(i))
        return text

class taskDirectory(list):
    def __init__(self, directory: str, root_task = task("main"), current_directory = str()):
        super().__init__()
        self.root_task = root_task
        self.directory = directory
        self.current_directory = current_directory + '/'

        self.clear()
        self += self.directory.split('/')
        self.task_name = self[-1]
        self.type = self.get_type()

    def set_current_dir(self, current_dir: str):
        self.current_directory = current_dir + '/'
        self.to_absolute_path()

    def set_root_task(self, root_task):
        self.root_task = root_task

    def get_task(self):
        print(self)
        task = self.root_task
        for i in range(1, len(self)):
            task = self.find_tesk(task, self[i])
        return task
    
    def to_text(self):
        return self.directory


    def get_type(self):
        if self.directory[0] == '/':
            return "absolute"
        elif self.directory == '../':
            return "parent"
        else: 
            return "relative"

    def to_absolute_path(self):
        if self.type == "parent":
            self.directory = self.current_directory.strip(self.current_directory.split('/')[-1])
        if self.type == "relative":
            self.directory = self.current_directory + self.directory
        self.to_list()

    def to_list(self):
        self.clear()
        self += self.directory.split("/")
        self.remove('')
    
    def change_directory(self):
        pass            

    def find_tesk(self, task:task, title:str):
        for i in range(0, len(task.children)):
            if task.children[i].title == title:
                return task.children[i]

        
# 일 경로, 경로로 일을 찾아주고, 경로로 변환해서 보여줄 수 있음   
# 사용법: 디렉토리를 넣어 초기화, set_root_task, set_current_dir를 마치고 get_task등으로 사용     

#--------------------------------------------------------
class taskManeger(textInterface):

    task_list = dict()
    path = "save.json"
    
    def __init__(self):
        super().__init__()
        self.name = "TaskM"
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                task_list = json.load(file)
            self.root_task = self.DictToTask(task_list)
            self.main_task = self.root_task
        except:
            self.main_task = task("main", children=list())
            self.save()

        self.directory = taskDirectory('/' + self.main_task.title, self.root_task, '')

        self.list_print() 

        self.bindFunc('print', self.list_print)
        self.bindFunc('add', self.add_task)
        self.setParmType((str, str, str))

        self.bindFunc('deadline', self.alter_dead_line)
        self.setParmType((int, str))
        
        self.bindFunc('progress', self.set_progress)
        self.setParmType((int, int))

        self.bindFunc('remove', self.remove)
        self.setParmType((int))

        self.bindFunc('move', self.move)
        self.setParmType((str))

        self.setHead(self.directory.to_text(), '>')
    
    def taskToDict(self, task: task):
        children = list()
        arg = dict()
        arg["title"] = task.title
        arg["deadLine"] = task.deadLine
        arg["progress"] = task.progress

        if task.children != None:
            for i in range(0, len(task.children)):
                children.append(self.taskToDict(task.children[i]))

        arg["children"] = children
        return arg


    def DictToTask(self, _dict: dict):
        children = list()
        # arg = dict()
        # arg["title"] = task.title
        # arg["deadLine"] = task.deadLine
        
        _task = task(_dict["title"], _dict["deadLine"], _dict["progress"])
        if _dict["children"] != None:
            for i in range(0, len(_dict["children"])):
                children.append(self.DictToTask(_dict["children"][i]))

        _task.children = children
        return _task

    def save(self):
        with open(self.path, "w", encoding="utf-8") as file:
                
            json.dump(self.taskToDict(self.root_task), file, indent="\t")
            print("저장됨")

    def list_print(self):
        print('\n')
        for i in range(0, len(self.main_task.children)):
                self.main_task.children[i].add = '\n'
                print(self.main_task.children[i].print(i), end='')
        print('\n')

    def add_task(self, *arg):    
        #자식, 기한을 받음 인덱스로 구분, 0은 기한, 1은 자식
        if len(arg) == 0:
            print("인자 없음")
            return
        if len(arg) == 1:
            result = task(arg[0])
        if len(arg) == 2:
            result = task(arg[0], arg[1])
        if len(arg) == 3:
            arg[2] = arg[2].split('.')

            for j in range(0, len(arg[2])):
                arg[2][j] = self.main_task.children[int(arg[2][j]) - 1]

            for k in range(0, len(arg[2])):  
                self.main_task.children.remove(arg[2][k])

            result = task(arg[0], arg[1], children=arg[2])
        
        self.main_task.children.append(result)
        
        #list요소를 arg로 설정
        self.save()

    def alter_dead_line(self, *arg):
        #인덱스, 기한
        #?뒤 세부사항 deadLine:
        index:int
        DLine:str
        index, DLine = arg

        index -= 1
        self.main_task.children[index].deadLine = DLine
        self.save()

    def set_progress(self, *arg):
        index:int
        progress:int
        index, progress = arg

        index -= 1
        self.main_task.children[index].progress = progress
        self.save()
        
    def set_parent(self, *arg):
        index:int
        parent_index:int
        pass

    def remove(self, *arg):
        index:int
        index = arg[0]
        index -= 1
        self.main_task.children.pop(index)
        self.save()

    def move(self, *arg):
        directory = arg[0]
        self.directory = taskDirectory(directory, self.root_task, self.directory.to_text())
        self.directory.to_absolute_path()

        self.main_task = self.directory.get_task()
        self.setHead(self.directory.to_text(), '>')

     

if __name__ == "__main__":
    app = taskManeger()
    app.execute("exit")

# while True:
#     mode = input("모드(t: 할 일, p: 프린트):")

#     if mode == 't':
#         add = input("할 일 추가:").split(",")
#         for i in range(0, len(add)):
#             info = add[i].split(";")
            
#             #자식, 기한을 받음 인덱스로 구분, 0은 기한, 1은 자식
#             if len(info) == 1:
#                 arg = task(info[0])
#             if len(info) == 2:
#                 arg = task(info[0], info[1])
#             if len(info) == 3:
#                 info[2] = info[2].split('.')

#                 for j in range(0, len(info[2])):
#                     info[2][j] = main_task.children[int(info[2][j]) - 1]

#                 for k in range(0, len(info[2])):  
#                     main_task.children.remove(info[2][k])

#                 arg = task(info[0], info[1], children=info[2])
            
#             #list요소를 arg로 설정
#             add[i] = arg
#         main_task.children += add
#         save()

#     if mode == 'p':
#         list_print()

#     if mode == 'd':
#         #인덱스, 기한
#         #?뒤 세부사항 deadLine:
#         index, DLine = input("인덱스 기한:").split(' ')
#         index = int(index) - 1
#         main_task.children[index].deadLine = DLine
#         save()

#     if mode == 'r':
#         #인덱스, 기한
#         #?뒤 세부사항 deadLine:
#         index, progress = input("인덱스 기한:").split(' ')
#         index = int(index) - 1
#         main_task.setChildrenProgress(index, progress)
#         print(main_task.progress)
#         save()

#     if mode == 'exit':
#         break






