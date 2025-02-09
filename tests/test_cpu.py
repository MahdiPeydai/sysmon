import re
import psutil
import time
import signal

from bddcli import Given, when, stdout, status, stderr, Application, given


INTERVAL_EXPECTED_USAGE = '''\
usage: sysmon cpu [-h] [-i INTERVAL] [-pc]
sysmon cpu: error: argument -i/--interval: expected one argument
'''


# sysmon cpu usage command test
def test_cpu():
    app = Application('sysmon', 'sysmon:Sysmon.quickstart')

    with Given(app, 'cpu') as s:
        
        # test command : sysmon cpu
        assert status == 0 # check process status
        assert stderr == '' # check for error
        assert re.match(r'CPU Usage : \d+\.\d+%',str(stdout)) # validate output

       
        # test command : sysmon cpu -i
        when(['cpu', '-i'])
        assert status == 2
        assert stderr == INTERVAL_EXPECTED_USAGE


        # test command : sysmon cpu -pc
        # show cpu usage for each core
        when(['cpu', '-pc'])
        assert status == 0
        assert stderr == ''

        lines = str(stdout).strip().split('\n') # get output lines
        num_cores = psutil.cpu_count(logical=True)  # get system cpu cores

        assert len(lines) == num_cores  # ensure outpu lines and cpu cores are same

        for i, line in enumerate(lines):
            assert re.match(rf'Core {i + 1} usage : \d+\.\d+%', line)  # validate output
        


    #testing intervals

    # test command : sysmon cpu -i 1
    # show cpu usage in intervals
    with Given(app, 'cpu -i 1', nowait=True) as s:
        # estimated time for third print
        time.sleep(2.5)
        
        s.kill(signal.SIGINT)
        s.wait()

        lines = str(stdout).strip().split('\n')
        intervals = 3

        stdout_pattern = r''
        for l in range(intervals) :
            stdout_pattern += r'CPU Usage : \d+\.\d+%\n'
        stdout_pattern += "\n"
        assert re.match(stdout_pattern,str(stdout))

    # test command : sysmon cpu -pc -i 1
    # show cpu usage in intervals
    with Given(app, 'cpu -pc -i 1', nowait=True) as s:
        # estimated time for second print
        time.sleep(1.5)
        s.kill(signal.SIGINT)
        s.wait()
        
        lines = str(stdout).strip().split('\n')
        num_cores = psutil.cpu_count(logical=True)

        assert len(lines) % num_cores == 0  # ensure outpu lines and cpu cores number are

        intervals = 2

        stdout_pattern = r''
        for l in range(intervals) :
            for i in range(num_cores):
                stdout_pattern += rf'Core {i + 1} usage : \d+\.\d+%\n'
        stdout_pattern += "\n"
        assert re.match(stdout_pattern,str(stdout))
