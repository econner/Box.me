import os
import jpype
from box import constants

def extract_text():
    '''
    jpype.startJVM(constants.JVM_PATH, "-ea", constants.JPYPE_CLASSPATH)
    TextExtract = jpype.JClass("TextExtract")
    text = TextExtract.extractTextFromFile('box/suggestion_engine/test_files/wordfile.doc')
    jpype.shutdownJVM()
    '''
    
    os.system('java -classpath ' + constants.JAVA_CLASSPATH + ' TextExtract suggestion_engine/test_files/wordfile.doc')
    
    return os.getcwd()