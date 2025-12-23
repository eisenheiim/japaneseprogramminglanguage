import sys
import os
import pickle
keywords= [
    "wa", "o", "no", "atai", "de", "aru", "print", "suru",
    "tasu", "seisu", "moji-retsu", "kakeru", "kaikakko",
    "tojikakko", "puroguramu", "hajimeyo", "oware"
]
strvariables={}
intvariable={}
line_no=1
english_letters = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z'
]
results=[] #list to store results.
def japanconverter(number): #to convert numbers to japanese type integers
    count=0
    x=[]
    if type(number)==type(4):
        number=str(number)
    number=number[::-1]
    for ch in number:
        x.append(ch)
        count+=1
        if count%4==0 and len(number)>4 : #putting commas.
            x.append(",")
    if x[-1]==",":
        x.pop(-1)
    if x[0]==",":
        x.pop(0)
    x.reverse()
    res="".join(x)
    return res
def turkishconverter(number): #converting japanese type of numbers to normal numbers to make calculations.
    number=number.replace(",","")
    if number.isdigit()!=1:
        raise Exception(f"Compile error {line_no=}")
    return int(number)
def japanesechecker(word): #checking if the number is in true form.
    if word.replace(",","").isdigit():
        if word.isdigit() and len(word) > 1 and word[0] == "0":
            raise Exception(f"Compile error {line_no=}")
        if len(word.replace(",",""))>=5:
            if "," in word:
                if len(word) >=5:
                    reversedword = word[::-1]
                    count = 1
                    for char in reversedword:
                        if char == ",":
                            if count != 5:
                                return 0
                            count = 1
                        else:
                            count += 1
                    wordy = word.replace(",", "")
                    if wordy.isdigit()!=1:
                        return 0
                    return 1
            else:raise Exception(f"Compile error {line_no=}")
        elif word.isdigit():
            return 1
ifstring=0
def check_product(a, b): #checking if product of numbers is bigger than 10 digits
    num1 = len(str(a).replace(",",""))
    num2=len(str(b).replace(",",""))
    if num1+num2-1>10:
        return 0
    return 1
def check_string(s, n):
    if len(str(s).replace(",","")) * n > 10000:
        return 0
    return 1
def variablecheck(word): #function to check variables.
    global ifstring
    if word.lower() in strvariables:
        ifstring=1
        word =strvariables[word.lower()]
    elif word.lower() in intvariable:
        word =(intvariable[word.lower()])
    elif "-" in word:
        ifstring=1
        word =word.strip("-")
    #japanese number control
    elif "," in word:
        if len(word) >5:
            reversedword = word[::-1]
            count = 1
            for char in reversedword:
                if char == ",":
                    if count % 5!=0:
                        raise Exception(f"Compile error {line_no=}")
                    else:
                        pass
                    count = 1
                else:
                    count += 1
            wordy = word.replace(",", "")
            if wordy.isdigit()!=1:
                if word in results:
                    pass
                else:
                    raise Exception(f"Compile error {line_no=}")
        elif word.isdigit():
            pass
        else:
            if word in results:
                    pass
            else:
                raise Exception(f"Compile error {line_no=}")
    elif word in results:
        pass
    else:
        raise Exception(f"Compile error {line_no=}")
    return word
def expressionsolver(tokens): #function to solve expressions
    global ifstring
    if len(tokens)==1:
        if japanesechecker(tokens[0]):
            pass
        else:tokens[0]=str(variablecheck(tokens[0]))
        return tokens[0]
    while len(tokens) != 1:
        if len(tokens) > 1 and "kakeru" not in tokens and "tasu" not in tokens and "kaikakko" not in tokens:
                #if there is no operator in expressions
                raise Exception(f"Compile error {line_no=}")
        while "kaikakko" in tokens: #solving expressions inside paranthesis at first.
            if "kaikakko" or "tojikakko" in tokens:
                if tokens.count("kaikakko") != tokens.count("tojikakko"): #if kaikakko numbers and tojikakko numbers do not match
                    raise Exception(f"Compile error {line_no=}")
                while "kaikakko" in tokens:
                    kaikakko_index = len(tokens) - 1 - tokens[::-1].index("kaikakko")
                    tojikakko_index = len(tokens) - 1 - tokens[::-1].index("tojikakko")
                    if "kaikakko" in tokens[kaikakko_index+1:tojikakko_index] or "tojikakko" in tokens[kaikakko_index+1:tojikakko_index]:#Checking if there is another open parenthesis inside a pair of parenthesis
                        raise Exception(f"Compile error {line_no=}")
                    listcopy=tokens.copy()
                    poplen=len(listcopy[kaikakko_index+1:tojikakko_index])
                    res=expressionsolver(listcopy[kaikakko_index+1:tojikakko_index])
                    results.append(res)
                    tokens[tojikakko_index]=res
                    for i in range(poplen+1):
                        tokens.pop(kaikakko_index)
        while "kakeru" in tokens:
            kakeru_index = len(tokens)-1-tokens[::-1].index("kakeru")
            if kakeru_index==0 or kakeru_index==len(tokens)-1:#if operator are at the beginning or at the end of the expression boundries.
                if sys.argv[1]=="-execute":
                    raise Exception(f"Runtime error {line_no=}")
                else:
                    raise Exception(f"Compile error {line_no=}")
            if not japanesechecker(tokens[kakeru_index - 1]): #if it s not a number but int variable
                if tokens[kakeru_index-1].lower() in intvariable:
                    number=turkishconverter(intvariable[tokens[kakeru_index-1].lower()])
                else:
                    raise Exception(f"Compile error {line_no=}")
            else:
                number = turkishconverter(tokens[kakeru_index - 1])
            if japanesechecker(tokens[kakeru_index + 1]):
                factor2 = turkishconverter(tokens[kakeru_index + 1])
                if check_product(number,factor2)==0: #if their products are more than limit.
                    if sys.argv[1]=="-execute":
                        raise Exception(f"Runtime error {line_no=}")
                    elif sys.argv[1]=="-compile":
                        number=0
            else:
                if tokens[kakeru_index + 1].lower() in intvariable:
                    factor2=turkishconverter(variablecheck(tokens[kakeru_index + 1].lower()))
                else:factor2=variablecheck(tokens[kakeru_index + 1])
                if tokens[kakeru_index + 1].lower() not in intvariable:
                    if check_string(factor2,number)==0: #checking if the prodcut is longer than limit.
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")
                        elif sys.argv[1]=="-compile":
                            number=0
            result = number * factor2
            if type(result)==type(5):
                if len(str(result))>10:
                    if sys.argv[1]=="-execute":
                        raise Exception(f"Runtime error {line_no=}")
                tokens[kakeru_index + 1] = japanconverter(str(result))
            else:
                if len(str(result))>10000:
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")
                tokens[kakeru_index + 1] = (str(result))
                results.append(str(result))
            tokens.pop(kakeru_index - 1)
            tokens.pop(kakeru_index - 1)
        while "tasu" in tokens:
            tasu_index = len(tokens) - 1 - tokens[::-1].index("tasu")
            if tasu_index==0 or tasu_index==len(tokens)-1: #checkin if the operator is at the beginninh or a the end of the expression.
                if sys.argv[1]=="-execute":
                    raise Exception(f"Runtime error {line_no=}")
                else:
                    raise Exception(f"Compile error {line_no=}")
            if japanesechecker(tokens[tasu_index - 1]) and japanesechecker(tokens[tasu_index + 1]):
                mult1 = turkishconverter(tokens[tasu_index - 1])
                mult2 = turkishconverter(tokens[tasu_index + 1])
                result = mult1 + mult2
                tokens[tasu_index + 1] = str(japanconverter(result))
                results.append(str(japanconverter(result)))
                if len(str(result))>10:
                    if sys.argv[1]=="-execute":
                        raise Exception(f"Runtime error {line_no=}")
            elif tokens[tasu_index-1].lower() in intvariable and tokens[tasu_index+1].lower() in intvariable:
                    mult1=turkishconverter(intvariable[tokens[tasu_index-1].lower()])
                    mult2=turkishconverter(intvariable[tokens[tasu_index+1].lower()])
                    result = mult1 + mult2
                    if len(str(result))>10:
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")
                    tokens[tasu_index + 1] = str(japanconverter(result))
                    results.append(str(japanconverter(result)))
            elif tokens[tasu_index-1].lower() in intvariable and japanesechecker(tokens[tasu_index + 1]):
                    mult1=turkishconverter(intvariable[tokens[tasu_index-1].lower()])
                    mult2 = turkishconverter(tokens[tasu_index + 1])
                    result = mult1 + mult2
                    if len(str(result))>10:
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")
                    tokens[tasu_index + 1] = str(japanconverter(result))
                    results.append(str(japanconverter(result)))
            elif tokens[tasu_index+1].lower() in intvariable and japanesechecker(tokens[tasu_index -1]):
                    mult2=turkishconverter(intvariable[tokens[tasu_index+1].lower()])
                    mult1 = turkishconverter(tokens[tasu_index - 1])
                    result = mult1 + mult2
                    if len(str(result))>10:
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")
                    tokens[tasu_index + 1] = str(japanconverter(result))
                    results.append(str(japanconverter(result)))
            else: #so we are going to concatenate. they must be strings
                if tokens[tasu_index - 1].lower() in intvariable or tokens[tasu_index + 1].lower() in intvariable :
                    raise Exception(f"Compile error {line_no=}")
                else:
                    mult1 = variablecheck(tokens[tasu_index - 1])
                    mult2 = variablecheck(tokens[tasu_index + 1])
                    result = mult1 + mult2
                    if len(result)>10000:
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")
                    tokens[tasu_index + 1] = str(result)
                    results.append(str(result))  
            tokens.pop(tasu_index - 1)
            tokens.pop(tasu_index - 1)
    return tokens[0]
if sys.argv[1]=="-compile":
    
    with open(sys.argv[2],"r") as inputfile:
        line=inputfile.readline()
        while line.strip()!="Puroguramu o oware .":
            line=line.strip("\n")
            listoftokens = []
            current = ""
            instrcnst = False #if we are in string constant
            i = 0
            #hyphen control
            while i < len(line):
                ch = line[i]
                if ch == "-" and line[i:i+7]!="-retsu ": # possible single - input.
                    if instrcnst:
                        current += "-"
                        #constant finishes
                        listoftokens.append(current)
                        current = ""
                        instrcnst = False
                    else:
                        #constant starts
                        if current:
                            listoftokens.append(current)
                            current = ""
                        instrcnst = True
                        current += "-"
                elif ch == " " and not instrcnst:
                    if current:
                        listoftokens.append(current)
                        current = ""
                else:
                    current += ch
                i += 1
            if current:
                listoftokens.append(current)
            testword=" ".join(listoftokens)
            if (line.count("-")-line.count("moji-retsu"))%2!=0: #hypen control
                raise Exception(f"Compile error {line_no=}")
            #space control
            if line!=testword:
                raise Exception(f"Compile error {line_no=}")
            if listoftokens[-3]=="print" and listoftokens[-4]=="o" and listoftokens[-2]=="suru":
                res=expressionsolver(listoftokens[:-4])
            #assignment
            elif listoftokens[2]=="atai" and listoftokens[1]=="no":
                expressionss=listoftokens[4:-3]
                res=expressionsolver(expressionss)
                variable=listoftokens[0]
                if len(expressionss)==1: #wrong type assignment checking.
                    if variable.lower() in strvariables and expressionss[0].lower() in intvariable:
                        raise Exception(f"Compile error {line_no=}")
                    if variable.lower() in intvariable and expressionss[0].lower() in strvariables:
                        raise Exception(f"Compile error {line_no=}")
                if ifstring==1: #if the result is string
                    if variable.lower() in strvariables:
                        strvariables[variable.lower()]=res
                    else:
                        raise Exception(f"Compile error {line_no=}")
                else:
                    if variable.lower() in intvariable:
                        if japanesechecker(res):
                            intvariable[variable.lower()]=japanconverter(turkishconverter(res))
                        else:raise Exception(f"Compile error {line_no=}")
                    else:
                        raise Exception(f"Compile error {line_no=}")
                #constucting the expression
            #declaration
            elif listoftokens[1]=="wa":
                variablename=listoftokens[0].lower()
                if variablename in keywords:
                    raise Exception(f"Compile error {line_no=}")
                for ch in variablename:#checking the variables name
                    if ch in english_letters:
                        continue
                    else:
                        raise Exception(f"Compile error {line_no=}")
                if len(variablename)>10:
                    raise Exception(f"Compile error {line_no=}")
                else:
                    if listoftokens[2]=="seisu":
                        if variablename in intvariable or variablename in strvariables:
                            raise Exception(f"Compile error {line_no=}")
                        else:
                            intvariable[variablename]=0
                    else:
                        if variablename in strvariables or variablename in intvariable:
                            raise Exception(f"Compile error {line_no=}")
                        else:
                            strvariables[variablename]=""
            else:
                if line!="Puroguramu o hajimeyo .":
                    raise Exception(f"Compile error {line_no=}")

                #checking the line.
            for e in listoftokens:
                if japanesechecker(e):
                    x=e.replace(",","")
                    if len(x)>10:
                        raise Exception(f"Compile error {line_no=}")
                elif "-" in e and e!="moji-retsu":
                    if e[0]=="-" and e[-1]=="-":
                        x=e.strip("-")
                    if len(x)>10000:
                        raise Exception(f"Compile error {line_no=}")
                    if "-" in x:
                        raise Exception(f"Compile error {line_no=}")
                elif e.lower() in strvariables or e.lower() in intvariable:
                    pass
                elif e.lower() in keywords or e==".":
                    pass
                else: raise Exception(f"Compile error {line_no=}")
            line=inputfile.readline()
            line_no+=1
            ifstring=0
            if line.strip()=="":
                raise Exception(f"Compile error {line_no=}")
        inputfile.seek(0)
        lines = inputfile.readlines()
        last_line = lines[-1]
        if last_line!="Puroguramu o oware .":
            raise Exception(f"Compile error {line_no=}")
        inputfile.seek(0)
        content=inputfile.read()
        with open(sys.argv[3],"wb") as objfile:
            pickle.dump(content,objfile)
if sys.argv[1]=="-execute":
    if os.path.exists(sys.argv[2]):
        with open(sys.argv[2],"rb") as objfile:
            strvariables={}
            intvariable={}
            line_no=1
            english_letters = [
                'a','b','c','d','e','f','g','h','i','j','k','l','m',
                'n','o','p','q','r','s','t','u','v','w','x','y','z'
            ]
            results=[]
            data=pickle.load(objfile)
            with open(sys.argv[3],"w") as outxt:
                for line in data.split("\n"):
                    line=line.strip("\n")
                    listoftokens = []
                    current = ""
                    instrcnst = False
                    i = 0
                    while i < len(line):
                        ch = line[i]
                        if ch == "-" and line[i:i+7]!="-retsu ":
                            if instrcnst:
                                current += "-"
                                # hyphen bloğu bitiyor
                                listoftokens.append(current)
                                current = ""
                                instrcnst = False
                            else:
                                # hyphen bloğu başlıyor
                                if current:
                                    listoftokens.append(current)
                                    current = ""
                                instrcnst = True
                                current += "-"
                        elif ch == " " and not instrcnst:
                            if current:
                                listoftokens.append(current)
                                current = ""
                        else:
                            current += ch
                        i += 1
                    if current:
                        listoftokens.append(current)

                    #printing
                    if "print" in listoftokens:
                        l=listoftokens[:-4]
                        res=expressionsolver(l)
                        #if products are bigger than limits.
                        if japanesechecker(res):
                            if len(str(turkishconverter(res)))>10:
                                raise Exception(f"Runtime error {line_no=}")
                        else:
                            if len(res)>10000:
                                raise Exception(f"Runtime error {line_no=}")
                            res="-"+res+"-"
                        outxt.write(res+"\n")#writing to output file
                    #assignment
                    elif "atai" in listoftokens:
                        expressionss=listoftokens[4:-3]
                        res=expressionsolver(expressionss)
                        variable=listoftokens[0]
                        if ifstring==1:
                            if variable.lower() in strvariables:
                                strvariables[variable.lower()]=res
                           
                        else:
                            if variable.lower() in intvariable:
                                if japanesechecker(res):
                                    intvariable[variable.lower()]=japanconverter(turkishconverter(res))
                                
                        #constructing the expression

                    #declaration
                    elif "wa" in listoftokens:
                        variablename=listoftokens[0].lower()
                        for ch in variablename:
                            if ch in english_letters:
                                continue
                        
                        
                        if listoftokens[2]=="seisu":
                            intvariable[variablename]=0
                        else:                    
                            strvariables[variablename]=""
                    else:
                        pass   
                    
                    line_no+=1
                    ifstring=0
    else:
        pass
