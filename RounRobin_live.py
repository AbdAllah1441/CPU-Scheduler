class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time

class RoundRobin():
    def __init__(self, time_quantum):
        self.quantum = time_quantum
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        gantt_chart = []
        burst_time = []
        waiting_time = [0] * len(self.processes)

        turnaround_time = []
        current_time = 0

        # create a copy of the processes list to avoid modifying the original list
        remaining_processes = self.processes.copy()
        
        # create a dictionary to map the name of each process to its index in the list
        process_index = {process.name: i for i, process in enumerate(self.processes)}

        while remaining_processes:
            # get the next process in the list
            current_process = remaining_processes.pop(0)

            # calculate waiting time
            if current_process.arrival_time > current_time:
                waiting_time.append(current_process.arrival_time - current_time)
                current_time = current_process.arrival_time

            # add the process to the Gantt chart
            gantt_chart.append((current_process.name, current_time, current_time + min(self.quantum, current_process.remaining_time)))

            x = min(self.quantum, current_process.remaining_time)

            exist = False

            # update the burst time and remaining time of the process
            for i in range(len(burst_time)):
                if current_process.name == burst_time[i][0]:
                    exist = True
            
            if exist:
                for i in range(len(burst_time)):
                    if current_process.name == burst_time[i][0]:
                        burst_time[i][1] = burst_time[i][1] + x
            else:
                burst_time.append([current_process.name, x])


            if current_process.remaining_time <= self.quantum:
                current_time += current_process.remaining_time
                turnaround_time.append(current_time - current_process.arrival_time)
                current_process.remaining_time = 0
            else:
                current_time += self.quantum
                current_process.remaining_time -= self.quantum
                remaining_processes.append(current_process)

            # update the waiting time of all remaining processes
            for process in remaining_processes:
                if process.arrival_time <= current_time:
                    index = process_index[process.name]
                    waiting_time[index] += x

        # calculate the average waiting and turnaround times
        avg_waiting_time = sum(waiting_time) / len(self.processes)
        avg_turnaround_time = sum(turnaround_time) / len(self.processes)

        slot_gantt_chart = []

        for i in range(len(gantt_chart)):
                for j in range(gantt_chart[i][2] - gantt_chart[i][1]):
                    slot_gantt_chart.append(gantt_chart[i][0])

        return slot_gantt_chart, burst_time, avg_waiting_time, avg_turnaround_time

        


gantt= []
ask = True
rem = []
addProcess = "no"
processes = []
counter = 0
j = -1
# Create the Round Robin scheduler with time quantum = 2
quantum = int(input("enter quantum: "))
scheduler = RoundRobin(time_quantum = quantum)

while True:
    j = j + 1

    if ask == True:
        addProcess = input("do you want to add process? ")

    if addProcess.lower() == "close":
        break

    if addProcess.lower() == "yes":
        limit = int(input("enter number of processes: "))
        for i in range(limit):
            name = input("enter name of the process: ")
            bur = int(input("enter burst time: ")) 
            processes.append(Process(name, counter, bur))

        # Sort the processes by arrival time
        processes.sort(key=lambda process: process.arrival_time)

        # Add the processes to the scheduler
        for process in processes:
            scheduler.add_process(process)

        # Run the scheduler
        slot_gantt_chart, burst_time, avg_waiting_time, avg_turnaround_time = scheduler.run()

    for process in processes:
        processes.pop()
    
    counter += 1

    for i in range(len(slot_gantt_chart)):
        process_name = slot_gantt_chart[i]
        existing_process = [process for process in gantt if process == process_name]
        if not existing_process:
            gantt.append(slot_gantt_chart[i])

    for i in range(len(burst_time)):
        process_name = burst_time[i][0]
        existing_process = [process for process in rem if process[0] == process_name]
        if not existing_process:
            rem.append(burst_time[i])

    final = []

    for i in range(len(gantt)):
        for j in range(len(rem)):
            if gantt[i] == rem[j][0]:
                minimum = min(rem[j][1], quantum)
                for k in range(minimum):
                    final.append(gantt[i])

    j = 1

    if len(final) == len(set(final)) + 1 and len(final) > 0:
        for i in range(len(rem)):
            if rem[i][0] == final[-1]:
                rem[i][1] = rem[i][1] - 1 
        print(final[-1])
        print(rem)


    elif len(final) == len(set(final)) and len(final) > 0:
        for i in range(len(rem)):
            if rem[i][0] == final[0]:
                rem[i][1] = rem[i][1] - 1 
        print(final[0])
        print(rem)

    else:

        if j >= len(final):
            break
        else:
            # Print the results

            for i in range(len(rem)):
                if final[j] == rem[i][0]:
                    if rem[i][1] > 0:
                        ask = True
                        for i in range(len(rem)):
                            if rem[i][0] == final[j]:
                                rem[i][1] = rem[i][1] - 1    
                        c = 0
                        for i in range(len(rem)):
                            c = c + rem[i][1]
                        if c >= 0:
                            print(final[j])
                            print(rem)
                    else:
                        ask = False
        


print("Average Waiting Time:", avg_waiting_time)
print("Average Turnaround Time:", avg_turnaround_time)

