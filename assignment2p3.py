'''
CSS 430 Assignment 2 Scheduling
Assumptions:
1. Input file is sorted by arrival time (does this matter???)
2. Input file is well formatted
'''
import queue

class Process:
    def __init__(self, num, aT, bT, priority):
        self.num = num
        self.aT = aT
        self.bT = bT
        self.priority = priority

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.bT < other.bT

        return self.priority < other.priority

    def __gt__(self, other):
        if self.priority == other.priority:
            return self.bT > other.bT
        return self.priority > other.priority
    
    def __str__(self):
        return  'P' + str(self.num)

    def _repr_html_(self):
        return 'Process [' + str(self.aT) + ', ' + str(self.bT) + ', ' + str(self.priority) + ']'

    def runOne(self):
        self.bT -= 1

def main():
    filename = input('Type in input file: (must be .txt file)\n')
    processes = readFile(filename)
    
    #quantum = input('Enter value for quantum size (ms): ')
    #print('p_arrival: ', end = '')
    #print(p_arrival)
    #print('p_cpu: ', end = '')
    #print(p_cpu)
    p_arrival = []
    for p in processes:
        p_arrival.append(p.aT)
    timeline = getTimeline(processes, quantum = 3)
    
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
        priority = l_arr[3]
        ans.append(Process(num, aT, bT, priority))

    return ans

def printQueue(q):
    if q.qsize() is not 0:
        val = q.get()
        arr = [val]
        print('[' + str(val) + '', end = '')
        q.put(val)
        
        for _ in range(1, q.qsize()):
            val = q.get()
            arr.append(val)
            print(', ' + str(val), end = '')
            q.put(val)
        print(']')
    else:
        print('[]')

def getTimeline(processes, quantum = 3):
    currProcess = 0 #current working process (index)
    counter = quantum
    timeline = []

    total_time = 0
    for p in processes:
        total_time += p.bT

    q = []
    isNewQuantum = True

    arrived = []
    #running all processes
    for sec in range(total_time):
        #put arrived processes in queue
        for p in processes:
            if sec == p.aT:
                q.append(p)
        q.sort()

        currProcess = q.pop(0)        
        currProcess.runOne()
        if currProcess.bT is not 0:
            q.append(currProcess)

        timeline.append(currProcess.num)

    return timeline

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
        p = 'P'+str(timeline[sec] + 1)
        print(p.rjust(4), end = '')
    
    print()

    for sec in range(len(timeline)+1):
        print(str(sec).ljust(4), end = '')

    print('\n')

def printTat(tats):
    print('Turnaround Time(s):')
    for i in range(len(tats)):
        print('P' + str(i+1) + ': ' + str(tats[i]).ljust(3) + 's')
    print()

def printWt(wt):
    print('Waiting Time(s):')
    for i in range(len(wt)):
        print('P' + str(i+1) + ': ' + str(wt[i]).ljust(3) + 's')
    avg = sum(wt)/len(wt)
    print('Average wait time: ' + str(avg) + 's')
    print()


        

if __name__ == '__main__':
    main()