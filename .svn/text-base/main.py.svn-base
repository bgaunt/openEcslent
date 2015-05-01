#starting point for ecslent
import random
import os
import engine
import yaml
import traceback

class Options(object):
    def update(self, rhs):
        self.__dict__.update(rhs.__dict__)

class NetworkingOptions(Options):
    def __init__(self):
        self.enableNetworking               = False
        self.vShipNet                       = False
        self.ip                             = '192.168.1.2'
        self.server                         = False

class EngineeringOptions(Options):
    def __init__(self):
        self.doProfiling                    = False
        self.alwaysBuildExt                 = True
        self.abortIfCompilingExtensionsFail = True
        self.loadPsyco                      = False #load psyco - disabled for now because it has a few weird stability quirks, and performance is not an issue thus far
        self.configPath                     = 'config'
        self.compileCEntForMingW            = False
        self.releaseMode                         = False

class GfxOptions(Options):
    def __init__(self):
        self.drawGrid                       = False
        self.hydrax                         = False
        self.drawGrid                       = False
        self.renderWater                    = True
        self.renderSkybox                   = True

class GameOptions(Options):
    def __init__(self):
        self.testToRun                      = 8
        self.toLoad                         = []

class Player(Options):
    def __init__(self):
        self.playerId                       = -1
        self.side                           = 0

class LocalOptions(Options):
    def __init__(self):
        self.networkingOptions = NetworkingOptions()
        self.engineeringOptions = EngineeringOptions()
        self.gfxOptions = GfxOptions()
        self.gameOptions = GameOptions()
        self.playerOptions = Player()

    def update(self, rhs):
        Options.update(self, rhs)
        self.networkingOptions.update(rhs.networkingOptions)
        self.engineeringOptions.update(rhs.engineeringOptions)
        self.gfxOptions.update(rhs.gfxOptions)
        self.gameOptions.update(rhs.gameOptions)

def RunGame(localOptions):
    try:
        engine.misc.erasePycFiles()
        parseCommandLineOptions(localOptions)
        e = engine.Engine(localOptions)
        e.transition(e.State.MINIMAL)
        e.transition(e.State.MAINMENU)
        e.levelSystem.levelToLoad = 'openwater'
        e.transition(e.State.GAMEPLAY)
        e.mainLoop()
    finally:
        engine.misc.erasePycFiles()

def LoadLocalOptions():
    localOptionsFilename = 'localOptions.yaml'
    localOptions = LocalOptions()
    try:
        savedlocalOptions = yaml.load(open(localOptionsFilename, 'r'))
        localOptions.update(savedlocalOptions)
    except:
        print 'Failed to load local options - create defaults'
        localOptions = LocalOptions()
        traceback.print_exc()
    yaml.dump(localOptions, open(localOptionsFilename, 'w'), default_flow_style=False)
    return localOptions

def parseCommandLineOptions(localOptions):
    #import pdb; pdb.set_trace()
    import sys
    s = 'load='
    for arg in sys.argv:
        if s in arg:
            opt = arg[arg.find(s) + len(s):].strip()
            print 'Load:', opt
            append = True
            for lo in localOptions.gameOptions.toLoad:
                if opt.lower() == lo.lower():
                    append = False
                    break
            if append:
                localOptions.gameOptions.toLoad.append(opt)

def BuildCExtensions(localOptions):
    command = 'python setup.py build_ext --inplace'
    if localOptions.engineeringOptions.alwaysBuildExt:
        command += ' --force'
    if localOptions.engineeringOptions.compileCEntForMingW:
        command += ' -c mingw32'        
    output = os.system(command)
    if output != 0:
        if localOptions.engineeringOptions.abortIfCompilingExtensionsFail:
            raise Exception( 'Failed to compile cent.pyd - aborting' )
        else:
            print 'Failed to compile cent.pyd'
    return True

localOptions = None # for the cProfiler
def main():
    random.seed(12345)
    global localOptions
    localOptions = LoadLocalOptions()
    if localOptions.engineeringOptions.releaseMode:
        import os
        if not os.path.exists(os.path.join(os.getcwd(), 'cent.pyd')):
            output = BuildCExtensions(localOptions)
    else:
        output = BuildCExtensions(localOptions)

    #run main
    if localOptions.engineeringOptions.doProfiling:
        import cProfile
        cProfile.run('RunGame(localOptions)', 'profileData')
    else:
        RunGame(localOptions)

if __name__ == '__main__':
    main()
