__author__ = 'kovtash'

import subprocess,os,re

FFMPEG=os.path.realpath("./bin/ffmpeg")

class MediaStream():
    def __init__(self):
        self.id = None
        self.codec = None

class VideoStream(MediaStream):
    def __init__(self):
        MediaStream.__init__(self)
        self.width=None
        self.height=None

class MediaPreset():
    def __init__(self):
        self.video=VideoStream()
        self.audio=MediaStream()
        self.format=None

ITUNES_MEDIA_PRESET = MediaPreset()
ITUNES_MEDIA_PRESET.video.codec='h264'
ITUNES_MEDIA_PRESET.audio.codec='aac'
ITUNES_MEDIA_PRESET.format='mp4'


class MediaInfo():
    def __init__(self,sourceFile=None):
        self._streamInfoPattern = re.compile('.*Stream #(?P<streamId>\d+\.\d+)[^:]*: (?P<streamType>[^:]+):(?P<streamData>[^\n]+)')
        self._videoSizePattern = re.compile('\d+x\d+')
        self.videoStreams = []
        self.audioStreams = []

        if sourceFile is not None:
            self.getInfoFromFile(sourceFile)


    def getInfoFromFile(self,sourceFile):
        cmd = [FFMPEG,"-i",sourceFile]

        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        std=p.communicate()

        processSTDOUT=std[1]
        print processSTDOUT


        streamInfo=self._streamInfoPattern.findall(processSTDOUT)
        print streamInfo

        for stream in streamInfo:
            streamData=stream[2].split(',')

            if stream[1] == 'Video':
                currentStream = VideoStream()
                currentStream.id=stream[0]
                currentStream.codec=streamData[0].strip(' ')

                videoSizes=self._videoSizePattern.search(streamData[2]).group(0).strip(' ').split('x')
                currentStream.width=videoSizes[0]
                currentStream.height=videoSizes[1]
                self.videoStreams.append(currentStream)

            elif stream[1] == 'Audio':
                currentStream = MediaStream()
                currentStream.id=stream[0]
                currentStream.codec=streamData[0].strip(' ')
                self.audioStreams.append(currentStream)



def videoConvert(source,preset,destination=None,fast=True):

    result=False

    if destination is None:
        sourceFilename,sourceExtension=os.path.splitext(source)
        currentDestination="".join([sourceFilename,'_converted.',preset.format])
    else:
        currentDestination=destination

    if not os.path.exists(source):
        return result

    if fast:
        currentPreset=MediaPreset()
        currentPreset.video.codec='copy'
        currentPreset.audio.codec='copy'
        currentPreset.format=preset.format
        sourceInfo=MediaInfo(source)



        if len(sourceInfo.videoStreams)==0 or len(sourceInfo.audioStreams)==0:
            return result

        for stream in sourceInfo.videoStreams:
            if preset.video.codec != stream.codec:
                currentPreset.video.codec = preset.video.codec

        for stream in sourceInfo.audioStreams:
            if preset.audio.codec != stream.codec:
                currentPreset.audio.codec = preset.audio.codec

    else:
        currentPreset=preset

    cmd = [FFMPEG,"-threads","4","-y","-i",source,"-vcodec",currentPreset.video.codec,"-acodec",currentPreset.audio.codec,"-f",preset.format,currentDestination]
    print cmd

    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    resultcode=p.wait()
    result = not resultcode
    return result

if __name__=='__main__':
    pass