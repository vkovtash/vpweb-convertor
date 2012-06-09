__author__ = 'kovtash'


import subprocess, os, vpwebFileInfo, sys

if sys.platform == 'darwin':
    ATOMIC_PARSLEY = os.path.realpath("./bin/AtomicParsley")
elif sys.platform == 'linux2':
    ATOMIC_PARSLEY = os.path.realpath("/usr/bin/AtomicParsley")

class AtomicParsley(vpwebFileInfo.vpwebFileInfo):
    def __init__(self,filePath):

        self._filePath=filePath

        vpwebFileInfo.vpwebFileInfo.__init__(self,filePath)

    @property
    def stikType(self):
        if self.episode is None:
            return "Movie"
        else:
            return "TV Show"

    def setTags(self):
        cmd=[ATOMIC_PARSLEY,self._filePath,"-W","--stik",self.stikType]

        if self.poster is not None:
            cmd.extend(["--artwork",self.poster])

        if self.stikType=="TV Show":
            cmd.extend(["--TVShowName",self.name])

            if self.season is not None:
                cmd.extend(["--TVSeasonNum",self.season])

            if self.episode is not None:
                cmd.extend(["--TVEpisode",self.episode,"--TVEpisodeNum",self.episode])

        print cmd
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        resultcode=p.wait()
        result = not resultcode
        return result