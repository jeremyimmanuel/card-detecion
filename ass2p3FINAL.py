'''
CSS 430 Assignment 2 Scheduling
Assumptions:
1. Input file is sorted by arrival time (does this matter???)
2. Input file is well formatted
'''
import sys

class Process:
    def __init__(self, num = 0, aT = 0, bT = 0, priority = 0):
        self.num = num
        self.aT = aT
        self.bT = bT
        self.priority = priority

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.aT < other.aT #tiebreaker
        return self.priority < other.priority

    def __gt__(self, other):
        if self.priority == other.priority:
            return self.aT > other.aT #tiebreaker
        return self.priority > other.priority
    
    def __str__(self):
        return  'P' + str(self.num)

    def _repr_html_(self):
        return 'Process [' + str(self.aT) + ', ' + str(self.bT) + ', ' + str(self.priority) + ']'

    def run(self, n = 1):
        self.bT -= n

    def isCompleted(self):
        return self.bT <= 0

def main():
    
    filename = input('Type in input file: (must be .txt file)\n') #get filname
    #filename = sys.argv[1] #input from command line
    processes = readFile(filename)
    
    quantum = int(input('Enter value for quantum size (ms): ')) #get quantum size
    # quantum = int(sys.argv[2]) #input from command line
    
    p_arrival = []
    for p in processes:
        p_arrival.append(p.aT)

    timeline = getTimeline(processes, quantum)
    tats = getAllTat(p_arrival, timeline)
    wt = getAllwt(p_arrival, timeline)

    printAll(timeline, tats, wt)

def readFile(filename):
    #get input from input file
    f = open(filename, 'r')
    f_lines = f.readlines() #convert input into list 
    
    ans = []
    
    #storing to list
    for line in f_lines:
        l_arr = line.split()
        num = int(l_arr[0][1:]) - 1 #num starts at 0 so we can reuse functions from previous parts
        aT = int(l_arr[1])
        bT = int(l_arr[2])
        priority = l_arr[3]
        ans.append(Process(num, aT, bT, priority))

    f.close()

    return ans


def getTimeline(processes, quantum = 3):
    timeline = [] #initialize timeline as list
    q = [] #implement a queue with list
    currProcess = Process() 
    
    sec = 0
    while not allCompleted(processes):
        #put arrived processes in queue
        for p in processes:
            if sec >= p.aT and not p.isCompleted() and p not in q: 
                q.append(p)
                print(len(q))
        q.sort()

        if len(q) > 0:  #there's at least one waiting process
            currProcess = q.pop(0)
            runTime = quantum if currProcess.bT >= quantum else currProcess.bT
            #print('runTime: ' + str(runTime) )
            currProcess.run(runTime)
            
            for _ in range(runTime):
                timeline.append(currProcess.num)
        else:           #if there's no process waiting to be run
            timeline.append(-1)
            
        if not currProcess.isCompleted(): #if process still has burst time left, put back in queue
            q.append(currProcess)
            q.sort()
            sec += runTime
        else:
            sec += 1
        
        
    return timeline

def allCompleted(processes):
    for p in processes:
        if not p.isCompleted():
            return False
    return True

def rindex(arr, val):
    rarr = arr[::-1] #reverse array
    return len(arr) - 1 - rarr.index(val)

def getTat(p_arrival, timeline, pid):
    #last instance - arrival time
    return rindex(timeline, pid) - p_arrival[pid] + 1

def getAllTat(p_arrival, timeline):
    tats = []
    numP = len(p_arrival)
    for pid in range(numP):
        tats.append(getTat(p_arrival, timeline, pid))
    return tats

def getWaitTime(p_arrival, timeline, pid):
    start = p_arrival[pid]
    end = rindex(timeline, pid) + 1
    tl_subset = timeline[start:end]
    return len(tl_subset) - tl_subset.count(pid)

def getAllwt(p_arrival, timeline):
    wt = []
    numP = len(p_arrival)
    for pid in range(numP):
        wt.append(getWaitTime(p_arrival, timeline, pid))
    return wt

def printAll(timeline, tats, wt):
    printTimeline(timeline)
    printTat(tats)
    printWt(wt)

def printTimeline(timeline):
    print('TIMELINE:')
    for sec in range(len(timeline)):
        if timeline[sec] >= 0:
            p = 'P'+str(timeline[sec] + 1) #add plus one here
        else:
            p = 'NO'    #no process was running at this time
        print(p.rjust(4), end = '')
    
    print()

    for sec in range(len(timeline)+1):
        print(str(sec).ljust(4), end = '')

    print('\n')

def printTat(tats):
    print('Turnaround Time(s):')
    for i in range(len(tats)):
        print('P' + str(i + 1) + ': ' + str(tats[i]).ljust(3) + 'ms') #add plus one at str(i)
    print()

def printWt(wt):
    print('Waiting Time(s):')
    for i in range(len(wt)):
        print('P' + str(i + 1) + ': ' + str(wt[i]).ljust(3) + 'ms') #add plus one at str(i)
    avg = sum(wt)/len(wt)
    print('Average wait time: ' + str(avg) + 's')
    print()

if __name__ == '__main__':
    main()