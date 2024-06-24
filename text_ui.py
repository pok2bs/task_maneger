class textInterface():
    def __init__(self, commend_info = dict()):
        self.commend_list = list()
        
        self.commend_func = commend_info
        self.pram = list()
        self.separator = dict()
        self.pram_type = dict()

        self.var_proces_func = None
        self.head = str()
        self.binded_commend = None
        self.setVarProcessFunc(self.VarProcessFunc)
        self.separator["var"] = ' '
        self.separator["commend"] = ';'

        self.name = 'program'

    def addCommend(self, commend: str):
        self.commend_list.append(commend)

    def bindFunc(self, commend:str, function):
        self.commend_func[commend] = function
        self.binded_commend = commend
        self.addCommend(commend)

    def setParmType(self, types: tuple):
        self.pram_type[self.binded_commend] = types

    def setVarProcessFunc(self, function):
        self.var_proces_func = function

    def setHead(self, head: str, separator: str):
        self.head = self.name + ' ' + head + separator + ' '

    def VarProcessFunc(self, input:str, separator):
        arg = input.strip(' ').split(separator)
        commend = arg[0]
        if len(arg) >= 2:
            var = arg 
            var.pop(0)

            if type(self.pram_type[commend]) == type:
                _type = self.pram_type[commend]
                var[0] = _type(var[0])
                self.pram.append(tuple(var))
                return commend
            
            for i in range(0, len(var)):
                _type = self.pram_type[commend][i]
                var[i] = _type(var[i])

            self.pram.append(tuple(var))
            return commend

        if len(arg) == 1:
            self.pram.append(None)
            return commend


    def execute(self, exit_commend):
        while True:
            self.pram.clear()
            #입력 받음
            
            #구분자로 나눔
            _input = input(self.head)
            input_commend = _input.split(self.separator["commend"])
            for i in range(0, len(input_commend)):
                input_commend[i] = self.var_proces_func(input_commend[i], self.separator["var"])
                
                if input_commend[i] == exit_commend:
                    return

            #존재하는 명령어인지 검사
            commend = list()
            for comm in input_commend:
                for e_comm in self.commend_list:
                    if comm == e_comm:
                        commend.append(comm)
                        break

            if len(commend) == 0:
                print("입력된 명령어가 존재하지 않습니다.")
                

            #나눈 명령어들을 순차적으로 실행
            for i in range(0, len(commend)):
                if self.pram[i] == None:
                    self.commend_func[commend[i]]()
                else:
                    self.commend_func[commend[i]](*self.pram[i])
                
        

# def hello():
#     print("hello")

# def bye():
#     print("bye")

# def say(*arg):
#     text = arg[0]
#     num = arg[1]

#     while num != 0:
#         print(text)
#         num -= 1

# data = [1, 2, 3, 4]
# myTerminal = taskTerminal()
# myTerminal.head = "명령어:"
# myTerminal.separator["commend"] = ";"
# myTerminal.separator["var"] = " "

# myTerminal.bindFunc('hello', hello)

# myTerminal.bindFunc('b', bye)

# myTerminal.bindFunc('s', say)
# myTerminal.setParmType((str, int))
# myTerminal.setVar('s', ('hello!', 6))


# if __name__ == "__main__":
#     myTerminal.execute("exit")

    
