from scrapy.conf import settings
import jpype, os

# java classpath
JAVA_CLASSPATH = [
    os.path.join(os.path.dirname(__file__), 'boilerpipe-1.2.0.jar'),
    os.path.join(os.path.dirname(__file__), 'nekohtml-1.9.13.jar'),
    os.path.join(os.path.dirname(__file__), 'xerces-2.9.1.jar')
]

class JavaInterface(object):
    def __init__(self):
        self.initialized = False

    def __getattribute__(self, name):
        if not jpype.isJVMStarted():
            object.__getattribute__(self, 'init_JVM')()

        if not jpype.isThreadAttachedToJVM():
            jpype.attachThreadToJVM()
        
        if not object.__getattribute__(self, 'initialized'):
            object.__getattribute__(self, 'initialize')()

        return object.__getattribute__(self, name)

    def init_JVM(self):
        jpype.startJVM(
            jpype.getDefaultJVMPath(), '-Djava.class.path=%s' % ':'.join(JAVA_CLASSPATH),
            '-DsuppressSwingDropSupport=true', '-Xms32M', '-Xmx64M'
        )
    
    def initialize(self):
        self.initialized = True            
        self.ArticleExtractor = jpype.JClass('de.l3s.boilerpipe.extractors.ArticleExtractor')
        self.ArticleSentencesExtractor = jpype.JClass('de.l3s.boilerpipe.extractors.ArticleSentencesExtractor')
