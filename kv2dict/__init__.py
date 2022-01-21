import io


def unescapeKeyValues(keyValuesString):
    return keyValuesString.replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\\', '\\').replace(r'\"', '"')


def loads(keyvaluesString):
    if not isinstance(keyvaluesString, str):
        raise ValueError('argument must be str')


    kvDict = {}
    focus = [ kvDict ]
    
    state = 0 # 0:NONE 1:IN_KEY 2:BEFORE_VALUE 3:IN_VALUE
    
    posBefore = -1
    posAfter = -1
    
    k = None
    v = None
    
    for index, value in enumerate(keyvaluesString):
        if value == '"':
            posBefore = posAfter
            posAfter = index
            if state == 1:
                k = unescapeKeyValues(keyvaluesString[posBefore + 1:posAfter])
            if state == 3:
                v = unescapeKeyValues(keyvaluesString[posBefore + 1:posAfter])
                focus[-1][k] = v
            state = (state + 1) % 4
        if value == '{':
            if state != 2:
                raise ValueError('keyvalues file is invalid')
            else:
                v = {}
                focus[-1][k] = v
                focus.append(v)
                state = 0
        if value == '}':
            if state != 0:
                raise ValueError('keyvalues file is invalid')
            else:
                focus.pop()

    if len(focus) != 1 or state != 0:
        raise ValueError('keyvalues file is invalid')
    
    return kvDict

def load(keyvaluesFile):
    if not isinstance(keyvaluesFile, io.TextIOBase):
        raise ValueError('argument must be like io.TextIOBase')

    kvDict = {}
    focus = [ kvDict ]
    
    state = 0 # 0:NONE 1:IN_KEY 2:BEFORE_VALUE 3:IN_VALUE
    
    k, v = None, None

    lineNum = 0

    while True:
        keyvaluesString = keyvaluesFile.readline()

        if len(keyvaluesString) == 0:
            break

        lineNum += 1
        
        indexBefore = None

        for index, value in enumerate(keyvaluesString):
            if value == ' ':
                continue

            elif value == '"':
                if state == 1:
                    k = unescapeKeyValues(keyvaluesString[indexBefore + 1:index])
                
                elif state == 3:
                    v = unescapeKeyValues(keyvaluesString[indexBefore + 1:index])
                    focus[-1][k] = v

                    k, v = None, None
                
                indexBefore = index
                state = (state + 1) % 4
            elif value == '{':
                if state != 2:
                    raise ValueError('keyvalues file is invalid at line', lineNum)
                else:
                    v = {}
                    focus[-1][k] = v
                    focus.append(v)

                    k, v = None, None

                    state = 0
            elif value == '}':
                if state != 0:
                    raise ValueError('keyvalues file is invalid at line', lineNum)
                else:
                    focus.pop()

    if len(focus) != 1 or state != 0:
        raise ValueError('keyvalues file is invalid')
    
    return kvDict
    
