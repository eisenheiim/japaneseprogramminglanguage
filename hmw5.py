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
resss=[] #list to store results.

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
    if "," in word:
        if len(word) >5:
            
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
            
        
    elif word.isdigit():
        return 1
ifstring=0
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
                if word in resss:
                    pass
                else:
                    raise Exception(f"Compile error {line_no=}")
                
            
            
        
        elif word.isdigit():
            pass
        else:
            if word in resss:
                    pass
            else:
                raise Exception(f"Compile error {line_no=}")
            

    elif word in resss:
        pass
    else:
        raise Exception(f"Compile error {line_no=}")

    return word
def expressionsolver(tokens):
    global ifstring
    
    if len(tokens)==1:
        if japanesechecker(tokens[0]):
            pass
        else:tokens[0]=str(variablecheck(tokens[0]))
        return tokens[0]
    while len(tokens) != 1:
        while "kaikakko" in tokens: #solving expressions inside paranthesis at first.

            if "kaikakko" in tokens:
                if tokens.count("kaikakko") != tokens.count("tojikakko"):
                    raise Exception(f"Compile error {line_no=}")
                while "kaikakko" in tokens:
                    kaikakko_index = len(tokens) - 1 - tokens[::-1].index("kaikakko")
                    tojikakko_index = len(tokens) - 1 - tokens[::-1].index("tojikakko")
                    if "kaikakko" in tokens[kaikakko_index+1:tojikakko_index] or "tojikakko" in tokens[kaikakko_index+1:tojikakko_index]:#Checking if there is another open parenthesis inside a pair of parenthesis
                        raise Exception(f"Compile error {line_no=}")
                    listcopy=tokens.copy()
                    poplen=len(listcopy[kaikakko_index+1:tojikakko_index])
                    res=expressionsolver(listcopy[kaikakko_index+1:tojikakko_index])
                    resss.append(res)
                    tokens[tojikakko_index]=res
                    for i in range(poplen+1):
                        tokens.pop(kaikakko_index)
        while "kakeru" in tokens:
            kakeru_index = len(tokens)-1-tokens[::-1].index("kakeru")
            if not japanesechecker(tokens[kakeru_index - 1]):

                if tokens[kakeru_index-1].lower() in intvariable:
                    number=turkishconverter(intvariable[tokens[kakeru_index-1].lower()])
                else:
                    raise Exception(f"Compile error {line_no=}")
            else:
                number = turkishconverter(tokens[kakeru_index - 1])
            if japanesechecker(tokens[kakeru_index + 1]):
                factor2 = turkishconverter(tokens[kakeru_index + 1])
            else:
                if tokens[kakeru_index + 1].lower() in intvariable:
                    factor2=turkishconverter(variablecheck(tokens[kakeru_index + 1].lower()))
                else:factor2=variablecheck(tokens[kakeru_index + 1])
            
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
                resss.append(str(result))
            tokens.pop(kakeru_index - 1)
            tokens.pop(kakeru_index - 1)
        while "tasu" in tokens:
            tasu_index = len(tokens) - 1 - tokens[::-1].index("tasu")
            
            if japanesechecker(tokens[tasu_index - 1]) and japanesechecker(tokens[tasu_index + 1]):
                mult1 = turkishconverter(tokens[tasu_index - 1])
                mult2 = turkishconverter(tokens[tasu_index + 1])
                result = mult1 + mult2
                if len(str(result))>10:
                    if sys.argv[1]=="-execute":
                        raise Exception(f"Runtime error {line_no=}")

                tokens[tasu_index + 1] = japanconverter(str(result))
            elif tokens[tasu_index-1].lower() in intvariable:
                    mult1=turkishconverter(intvariable[tokens[tasu_index-1].lower()])
                    mult2 = turkishconverter(tokens[tasu_index + 1])
                    result = mult1 + mult2
                    if len(str(result))>10:
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")
            elif tokens[tasu_index+1].lower() in intvariable:
                    mult2=turkishconverter(intvariable[tokens[tasu_index+1].lower()])
                    mult1 = turkishconverter(tokens[tasu_index - 1])
                    result = mult1 + mult2
                    if len(str(result))>10:
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")
            else:

                if type(variablecheck(tokens[tasu_index - 1])) != type(variablecheck(tokens[tasu_index + 1])):
                    raise Exception(f"Compile error {line_no=}")
                else:
                    mult1 = variablecheck(tokens[tasu_index - 1])
                    mult2 = variablecheck(tokens[tasu_index + 1])
                    result = mult1 + mult2
                    if len(result)>10000:
                        if sys.argv[1]=="-execute":
                            raise Exception(f"Runtime error {line_no=}")

                
                    tokens[tasu_index + 1] = str(result)
                    resss.append(str(result))
            tokens.pop(tasu_index - 1)
            tokens.pop(tasu_index - 1)
    return tokens[0]

if sys.argv[1]=="-compile":
    with open(sys.argv[2],"r") as inputfile:
       
        
        line=inputfile.readline()
        while line!="Puroguramu o oware .":
            
            line=line.strip("\n")
            listoftokens=line.split()
            testword=" ".join(listoftokens)
            #space control
            if line!=testword:
                raise Exception(f"Compile error {line_no=}")
            if "print" in listoftokens:
                pass

            #assignment
            elif "atai" in listoftokens:
                expressionss=listoftokens[4:-3]
                res=expressionsolver(expressionss)
                variable=listoftokens[0]
                if ifstring==1:

                    if variable.lower() in strvariables:
                        strvariables[variable.lower()]=res
                    else:
                        raise Exception(f"Compile error {line_no=}")
                else:

                    if variable.lower() in intvariable:
                        intvariable[variable.lower()]=japanconverter(turkishconverter(res))
                    else:
                        raise Exception(f"Compile error {line_no=}")
                
                #constucting the expression
    

            #declaration
            elif "wa" in listoftokens:
                variablename=listoftokens[0].lower()
                if variablename in keywords:
                    raise Exception(f"Compile error {line_no=}")

                for ch in variablename:
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
                pass   

            for e in listoftokens:
                if japanesechecker(e):
                    x=e.replace(",","")
                    if len(x)>10:
                        raise Exception(f"Compile error {line_no=}")
                else:
                    if "-" in e:
                        x=e.strip("-")
                        if len(x)>10000:
                            raise Exception(f"Compile error {line_no=}")

            line=inputfile.readline()
            line_no+=1
            ifstring=0
        inputfile.seek(0)
        content=inputfile.read()
       
        with open(sys.argv[3],"wb") as objfile:
            pickle.dump(content,objfile)
            pickle.dump(strvariables,objfile)
            pickle.dump(intvariable,objfile)
            pickle.dump(resss,objfile)
            
        


if sys.argv[1]=="-execute":
    if os.path.exists(sys.argv[2]):
        with open(sys.argv[2],"rb") as objfile:
            data=pickle.load(objfile)
            strvariables=pickle.load(objfile)
            intvariable=pickle.load(objfile)
            resss=pickle.load(objfile)
        with open(sys.argv[3],"w") as outxt:
            line_no=1
            for line in data.split("\n"):
                if "atai wa" in line:
                    l=line.split()[4:-3]
                    res=expressionsolver(l)
                    if japanesechecker(res):
                        if len(str(turkishconverter(res)))>10:
                            raise Exception(f"Runtime error {line_no=}")
                        
                    else:
                        if len(res)>10000:
                            raise Exception(f"Runtime error {line_no=}")
                if "print" in line:
                    l=line.split()[:-4]
                    res=expressionsolver(l)
                    if japanesechecker(res):
                        if len(str(turkishconverter(res)))>10:
                            raise Exception(f"Runtime error {line_no=}")
                       
                    else:
                        if len(res)>10000:
                            raise Exception(f"Runtime error {line_no=}")
                        res="-"+res+"-"
                    outxt.write(res+"\n")
                line_no+=1
    else:
        pass
