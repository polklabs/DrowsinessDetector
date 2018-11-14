from multiprocessing import Process
import main

# not sure if multiprocessing is supported on iOs
class ButtonProcess(Process):
   def __init__(self, webcamSource):
      super(ButtonProcess, self).__init__()
      self.webcamSource = webcamSource
   def run(self):
        main.main(self.webcamSource)
   def kill(self):
        main.changeLiveState()
   def join(self, timeout=None):
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)

