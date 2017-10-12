#!/usr/bin/python3
#coding=utf-8

import subprocess

#author: cg错过
#time: 2017-09-30

class ProcessCL:

    def getResultAndProcess(self, strCL):

        dictResult = {}
        strOut = ''
        strErr = ''
        subObj = subprocess.Popen(strCL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                  universal_newlines=True)
        returnCode = subObj.poll()
        while returnCode is None:
            stdout, stderr = subObj.communicate()
            returnCode = subObj.poll()
            strOut += stdout
            strErr += stderr
        dictResult['stdout'] = stdout
        dictResult['stderr'] = stderr
        
        return dictResult


    def getContinueResultAndProcess(self, strCL):
        
        strOut = ''
        strErr = ''
        dictResult = {}
        subObj = subprocess.Popen(strCL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                  universal_newlines=True)
        returnCode = subObj.poll()
        while returnCode is None:
            lineOut = subObj.stdout.readline()
            lineErr = subObj.stdout.readline()
            returnCode = subObj.poll()
            lineOut = lineOut.strip()
            lineErr = lineErr.strip()

            strOut += lineOut
            strErr += lineErr
            if((lineOut == '') | (lineErr == '')):
                break
            
        dictResult['stdout'] = strOut
        dictResult['stderr'] = strErr

        return dictResult
