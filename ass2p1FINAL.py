'''
CSS 430 Assignment 2 Scheduling
Assumptions:
1. Input file is sorted by arrival time (does this matter???)
2. Input file is well formatted
'''
'''
Process class for Short Job First Algorithm
'''
class Process:
    #Constructor
    def __init__(self, num = 0 , aT = 0, bT = 0, priority = 0):
        self.num = num
        self.aT = aT
        self.bT = bT
        self.priority = priority

    #Overriding the '<' operator for sorting purposes
    def __lt__(self, other):
        if self.priority == other.priority:
            return self.bT < other.bT
        return self.priority < other.priority

    #Orverriding the '>' operator for osrting purposes
    def __gt__(self, other):
        if self.priority == other.priority:
            return self.bT > other.bT
        return self.priority > other.priority

    #String representation of the Processe class
    def __str__(self):
        return  'P' + str(self.num)

    #HTML representation of Process class, can be seen in ipython or jupyter notebook/lab
    def _repr_html_(self):
        return 'Process [' + str(self.aT) + ', ' + str(self.bT) + ', ' + str(self.priority) + ']'

    def runOne(self):
        self.bT -= 1

    def isCompleted(self):
        return self.bT is 0

def main():
    filename = input('Type in input file: (must be .txt file)\n')
    processes = readFile(filename)
    
    p_arrival = []
    for p in processes:
        p_arrival.append(p.aT)
    
    timeline = getTimeline(processes)
    
    tats = getAllTat(p_arrival, timeline)
    wt = getAllwt(p_arrival, timeline)

    printAll(timeline, tats, wt)

def readFile(filename):
    #get input from input file
    #filename = input('Type in input file: (must be .txt file) \n')
    f = open(filename, 'r')
    f_lines = f.readlines() #convert input into list 
    #size = len(f_lines)     #number of processes
    ans = []
    #storing to list
    for line in f_lines:
        l_arr = line.split()
        num = int(l_arr[0][1:]) - 1 #num starts at 0 so we can reuse functions from previous parts
        aT = int(l_arr[1])
        bT = int(l_arr[2])
        #priority = l_arr[3]
        ans.append(Process(num, aT, bT))

    f.close()

    return ans


def getTimeline(processes):
    currProcess = 0 #current working process (index)
    #counter = quantum
    timeline = []

    total_time = 0
    for p in processes:
        total_time += p.bT

    q = []
    
    currProcess = Process() #initilazation

    #running all processes
    sec = 0
    while not allCompleted(processes):
        #put arrived processes in queue
        for p in processes:
            if sec == p.aT:
                q.append(p)
        q.sort()


        if len(q) > 0: #there's at least one waiting process
            currProcess = q.pop(0)

            currProcess.runOne()
            timeline.append(currProcess.num)
        else:       #there's no process waiting in queue
            timeline.append(-1)
        
        
        if not currProcess.isCompleted(): #if process still has burst time left, put back in queue
            q.append(currProcess)
            q.sort()
        
        sec += 1
        print('second' + str(sec) + ': ', end = ' ')
        print(timeline)
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
            p = 'P'+str(timeline[sec]) #add plus one here
        else:
            p = 'NO'
        print(p.rjust(4), end = '')
    
    print()

    for sec in range(len(timeline)+1):
        print(str(sec).ljust(4), end = '')

    print('\n')

def printTat(tats):
    print('Turnaround Time(s):')
    for i in range(len(tats)):
        print('P' + str(i) + ': ' + str(tats[i]).ljust(3) + 's') #add plus one at str(i)
    print()

def printWt(wt):
    print('Waiting Time(s):')
    for i in range(len(wt)):
        print('P' + str(i) + ': ' + str(wt[i]).ljust(3) + 's') #add plus one at str(i)
    avg = sum(wt)/len(wt)
    print('Average wait time: ' + str(avg) + 's')
    print()


if __name__ == '__main__':
    main()