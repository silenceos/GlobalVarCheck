'''
Created on 2016-10-25

@author: xinli3
'''

import os
import sys
import re

def GVCheck(inputFile):
    command = 'readelf -s ' + inputFile
    print 'Execute command: %s\n'%command
    try:
        fp_in = os.popen(command)
    except IOError:
        print 'Execute command failed: %s\n'%command
        return
    lines = fp_in.readlines()
    fp_in.close()
    
    #find dynamic table index
    symtableIndex = 0
    haveSymTable = False
    table = ''
    #look for '.symtab' table
    for i in range(0, len(lines)):
        if lines[i].find('.symtab') != -1:
            symtableIndex = i + 2
            haveSymTable = True
            table = '\'.symtab\''
            break
    if not haveSymTable:
        #look for '.dynsym' table
        for i in range(0, len(lines)):
            if lines[i].find('.dynsym') != -1:
                symtableIndex = i + 2
                haveSymTable = True
                table = '\'.dynsym\''
                break
    #not found symbol table
    if not haveSymTable:
        print 'Not found symbol table, please check input file.\n'
        return
      
    #find global variable
    sizeIndex = 2
    typeIndex = 3
    bindindex = 4
    ndxIndex = 6
    nameIndex = 7
    j = symtableIndex
    try:
        fp_out = open('global_var_check.log', 'a')
    except:
        print 'Open log file error: global_var_check.log'
        return
    fp_out.write('-------------------------------\n')
    fp_out.write('library file: '+inputFile+'\n')
    fp_out.write('data from '+table+' table\n')
    fp_out.write('\nGlobal Variable Information:\n')
    fp_out.write('ID\tSize\tVarName\n')
    count = 0
    while j < len(lines):
        if lines[j] != '\n' or lines[j] != ' ':
            line = lines[j]
            line = line.strip()
            line = re.sub(r'\s{2,}', ' ', line)
            contents = line.split(' ')
            if 'OBJECT' == contents[typeIndex].upper() and 'GLOBAL' == contents[bindindex].upper() and 'UND' != contents[ndxIndex]:
                count += 1
                tmp = str(count) +'\t' + contents[sizeIndex] + '\t' + contents[nameIndex] + '\n'
                fp_out.write(tmp)
        j += 1
    fp_out.write('\ntotal: '+str(count)+'\n')
    fp_out.write('-------------------------------\n\n\n')
    fp_out.close()
    print '~~~All done~~~'
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: GlobalVarCheck.py inputFile\n'
        exit()
    GVCheck(sys.argv[1])