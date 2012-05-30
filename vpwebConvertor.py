__author__ = 'kovtash'

SOURCE_DIR = '/Users/kovtash/vpweb/complete'
ENCODED_DIR = '/Users/kovtash/vpweb/encoded'
TAGGED_DIR = '/Users/kovtash/vpweb/tagged'

import ffmpegConvertor,glob,os,AtomicParsley


class vpwebConvertor():
    def __init__(self,sourceDir,encodedDir,taggedDir):
        self._sourceDir=sourceDir
        self._encodedDir=encodedDir
        self._taggedDir=taggedDir

        #init working directories
        if not os.path.exists(self._encodedDir):
            os.makedirs(self._encodedDir)

        if not os.path.exists(self._taggedDir):
            os.makedirs(self._taggedDir)

    @property
    def filesForConvert(self):
        return glob.glob(os.path.join(self._sourceDir,'*'))

    @property
    def filesForSetTags(self):
        return glob.glob(os.path.join(self._encodedDir,'*'))

    def convertVideo(self,sourcePath):

        filename=os.path.splitext(os.path.basename(sourcePath))[0]+"."+ffmpegConvertor.ITUNES_MEDIA_PRESET.format
        destinationPath=os.path.join(self._encodedDir,filename)

        result = ffmpegConvertor.videoConvert(sourcePath,ffmpegConvertor.ITUNES_MEDIA_PRESET,destination=destinationPath)
        if result:
            os.remove(sourcePath)

    def setVideoTags(self,sourcePath):

        destinationPath=os.path.join(self._taggedDir,os.path.basename(sourcePath))
        tags=AtomicParsley.AtomicParsley(sourcePath)
        result = tags.setTags()

        if result:
            os.rename(sourcePath,destinationPath)


    def process(self):
        for file in self.filesForConvert:
            self.convertVideo(file)

        for file in self.filesForSetTags:
            self.setVideoTags(file)


if __name__ == "__main__":
    test = vpwebConvertor(SOURCE_DIR,ENCODED_DIR,TAGGED_DIR)
    test.process()
