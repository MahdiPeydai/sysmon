import sys
import time
import psutil

class Monitoring():

    def __init__(self, data_fetcher, response_handler):
        self.data_fetcher = data_fetcher
        self.response_handler = response_handler


    def monitor(self, args):
        interval = args.interval

        if interval and interval<0: # validating interval argument
            message = "Error: Interval must be a positive integer!"
            self.esponse_handler.error(message=message, code=2)

        try:
            while True:
                data = self.data_fetcher.fetch(args)
                self.response_handler.success(data)
            
                if not interval:
                    sys.exit(0)
                else:
                    time.sleep(interval)
        
        
        # handling user privileges error
        except psutil.AccessDenied:
            message = "Root privileges required"
            self.response_handler.error(message=message)

        except KeyboardInterrupt: # kill signal (ctrl+C) handling
            message = ''
            self.response_handler.error(message=message, code=0) # calling response class error method

        #except Exception as e:
            #self.response_handler.error(message=e)
