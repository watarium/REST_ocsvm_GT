import csv
import io
import pandas as pd
import InputLog

class SignatureDetector:

    EVENT_TGT = "4769"
    EVENT_ST="4769"

    df=pd.DataFrame(data=None, index=None, columns=["datetime","eventid","accountname","clientaddr","servicename","processname","objectname"], dtype=None, copy=False)

    def __init__(self):
        print("constructor called")

    def is_attack(self):
        print("is_attack called")

    @staticmethod
    def signature_detect(datetime, eventid, accountname, clientaddr, servicename, processname, objectname):
        """ Detect attack using signature based detection.
        :param datetime: Datetime of the event
        :param eventid: EventID
        :param accountname: Accountname
        :param clientaddr: Source IP address
        :param servicename: Service name
        :param processname: Process name(command name)
        :param objectname: Object name
        :return : True(1) if attack, False(0) if normal
        """

        inputLog = InputLog.InputLog(datetime, eventid, accountname, clientaddr, servicename, processname, objectname)
        return SignatureDetector.signature_detect(inputLog)

    @staticmethod
    def signature_detect(inputLog):
        """ Detect attack using signature based detection.
        :param inputLog: InputLog object of the event
        :return : True(1) if attack, False(0) if normal
        """
        is_attack=False

        if (inputLog.get_eventid()==SignatureDetector.EVENT_ST) :
            SignatureDetector.hasNoTGT(inputLog)

        series = pd.Series([inputLog.get_datetime(),inputLog.get_eventid(),inputLog.get_accountname(),inputLog.get_clientaddr(),
                      inputLog.get_servicename(),inputLog.get_processname(),inputLog.get_objectname()], index=SignatureDetector.df.columns)
        SignatureDetector.df=SignatureDetector.df.append(series, ignore_index = True)

        inputLog.set_clientaddr("192.168.1.9");


        return is_attack

    @staticmethod
    def hasNoTGT(inputLog):
        logs=SignatureDetector.df[(SignatureDetector.df.accountname == inputLog.get_accountname())&(SignatureDetector.df.clientaddr==inputLog.get_clientaddr())]
        print(logs)
        print(logs.loc[:,['eventid']])


