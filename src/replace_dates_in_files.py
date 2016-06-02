#!/usr/bin/python3
import sys
import time
import logging
import re
import os
from array import array
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileCreatedEvent
from datetime import timedelta
from datetime import datetime

            
class FileHandler:
    DAY_MODIFIER_GROUP='dayModifier'
    DATE_FORMAT_GROUP='dateFormat'
    TMP_FILE_SUFFIX='.tmp'
    FILE_ENCODING='ISO-8859-15'
    
    def __init__(self):
        self.__dateRegex = re.compile('{DATE(?P<'+self.DAY_MODIFIER_GROUP+'>[+-][0-9]+)?(?P<'+self.DATE_FORMAT_GROUP+'>%[^}.]*)}')
    
    def handleFile(self, file):
        destinationFileName = self.dstFileName(file)
        tmpFileName = self.tmpFileName(destinationFileName)
        self.transformFile(file, tmpFileName)
        os.rename(tmpFileName, destinationFileName)
        if destinationFileName != file:
            logging.debug("Suppression du fichier d'origine %s", file)
            os.remove(file)
        
    def dstFileName(self, file):
        dstFileName=self.replaceDates(file)
        return dstFileName
        
    def tmpFileName(self, file):
        return file+self.TMP_FILE_SUFFIX
        
    def replaceDates(self, string):
        def datesrepl(matchobj):
            dayModifierGroup = matchobj.group(self.DAY_MODIFIER_GROUP)
            if (dayModifierGroup == None) :
                dayModifier = 0
            else:
                dayModifier = int(dayModifierGroup)
            dateFormat = matchobj.group(self.DATE_FORMAT_GROUP)
            return self.transformAndFormatDate(dayModifier, dateFormat)
        return self.__dateRegex.sub(datesrepl, string)
        
    def transformAndFormatDate(self, dayModifier, format):
        dayDelta=timedelta(days=dayModifier)
        modifiedDate = datetime.today() + dayDelta
        formattedDate = modifiedDate.strftime(format)
        return formattedDate

    def transformFile(self, originFilePath, destinationFilePath):
        logging.debug("Transformation du fichier %s vers le fichier %s", originFilePath, destinationFilePath)
        originFile = open(originFilePath, 'r', encoding=self.FILE_ENCODING)
        destinationFile = open(destinationFilePath, 'w+', encoding=self.FILE_ENCODING)
        
        lineNumber = 1
        for line in originFile:
            lineWithReplacedDates = self.replaceDates(line)
            if (line != lineWithReplacedDates):
                logging.debug("\tRemplace ligne %i :\n\t\t%s\t\t%s", lineNumber, line, lineWithReplacedDates)
            destinationFile.write(lineWithReplacedDates)
            lineNumber+=1
            
        
        originFile.close()
        destinationFile.close()
        
        
class RenameEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.__fileHandler=FileHandler()
        self.__filesToAccept = [re.compile('^.*\.xml$', re.IGNORECASE), re.compile('^.*\.csv$', re.IGNORECASE)]
        
    
    def on_created(self, event):
        try:
            if (isinstance(event, FileCreatedEvent)):
                filePath = event.src_path
                if self.shouldBeIgnored(filePath) == False:
                    logging.info("creation du fichier %s", event.src_path)
                    self.__fileHandler.handleFile(event.src_path)
                    logging.info("Fichier %s traite avec succes", event.src_path)
                else:
                    logging.debug("Ignore le fichier %s", event.src_path)
        except:
            import sys, traceback
            traceback.print_exc()
            
    def shouldBeIgnored(self, filePath):
        shouldBeIgnored = True
        for patternToAccept in self.__filesToAccept:
            logging.debug("trying pattern %s on file %s", patternToAccept, filePath)
            if re.match(patternToAccept, filePath) != None:
                logging.debug("pattern accepted")
                shouldBeIgnored = False
            else:
                logging.debug("pattern rejected")
        return shouldBeIgnored
            


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
                        
    if (len(sys.argv) != 2):
        logging.error("Usage\t: %s <path to watch>", sys.argv[0])
        logging.error("Exemple\t: %s /applis/ouisstiti/flux", sys.argv[0])
        logging.error("")
        logging.error("Replaces dates in files created in <in directory>. Accepts only *.xml and *.csv files")
        logging.error("Dates to replace have to be defined as '{DATE<numberOfDaySinceToday><dateFormat>}'")
        logging.error("\t<numberOfDaysSince>\t:\tinteger, number of days to add to current date (can be negative)")
        logging.error("\t<dateFormat>\t:\tstring, python date format expression")
        logging.error("")
        logging.error("Example 1:")
        logging.error("\t{DATE+2%Y%m%d}\t:\tdate in two days, with the format 20160123")
        logging.error("\t{DATE%Y%m}\t:\ttoday, with the format 201601")
        logging.error("\t{DATE-4%Y%m}\t:\tfour days ago, with the format 201601")
        exit(1)
    else:
        path = sys.argv[1]
        event_handler = RenameEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
