'''
CSS 430 Assignment 2 Scheduling
Assumptions:
1. Input file is sorted by arrival time (does this matter???)
2. Input file is well formatted
'''
import queue

def main():
    filename = input('Type in input file: (must be .txt file)\n')
    p_arrival, p_cpu = readFile(filename)
    quantum = int(input('Enter value for quantum size (ms): '))
    #print('p_arrival: ', end = '')
    #print(p_arrival)
    #print('p_cpu: ', end = '')
    #print(p_cpu)
    timeline = getTimeline(p_arrival, p_cpu, quantum)
    tats = getAllTat(p_arrival, timeline)
    wt = getAllwt(p_arrival, timeline)

    printAll(timeline, tats, wt)

def readFile(filename):
    #get input from input file
    #filename = input('Type in input file: (must be .txt file) \n')
    f = open(filename, 'r')
    f_lines = f.readlines() #convert input into list 
    size = len(f_lines)     #number of processes
    p_arrival = [None] * size
    p_cpu = [None] * size
    
    #storing to list
    for i in range(size):
        p_arrival[i] = int(f_lines[i].split()[1])
        p_cpu[i] = int(f_lines[i].split()[2])
    
    return p_arrival, p_cpu

def printQueue(q):
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

def getTimeline(p_arrival, p_cpu, quantum = 3):
    currProcess = 0 #current working process (index)
    counter = quantum
    timeline = []
    total_time = sum(p_cpu)  #total burst time
    q = queue.Queue()
    isNewQuantum = True
    #running all processes
    for i in range(total_time):
        #put arrived processe in queue
        if(i in p_arrival):
            indexes = [n for n, x in enumerate(p_arrival) if x is i]
            for idx in indexes:
                q.put(idx)
        
        print('Second ' + str(i) + ' ', end = '')
        #printQueue(q)
            
        if isNewQuantum: #start of a new quantum
            currProcess = q.get()
            #resets counter
            if p_cpu[currProcess] >= quantum:
                counter = quantum
            else:
                counter = p_cpu[currProcess] 
            isNewQuantum = False
            p_cpu[currProcess] -= 1
            counter -= 1
        else:
            p_cpu[currProcess] -= 1
            counter -= 1

        if counter is 0: 
            isNewQuantum = True
            if p_cpu[currProcess] > 0:
                q.put(currProcess)

        timeline.append(currProcess)

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