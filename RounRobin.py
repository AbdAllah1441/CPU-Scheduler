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

        return gantt_chart, burst_time, avg_waiting_time, avg_turnaround_time




# Create the Round Robin scheduler with time quantum = 2
quantum = int(input("enter quantum: "))
scheduler = RoundRobin(time_quantum = quantum)

processes = []

limit = int(input("enter number of processes: "))

for i in range(limit):
    name = input("enter name of the process: ")
    arr = int(input("enter arrival time: ")) 
    bur = int(input("enter burst time: ")) 
    processes.append(Process(name, arr, bur))




# Sort the processes by arrival time
processes.sort(key=lambda process: process.arrival_time)



# Add the processes to the scheduler
for process in processes:
    scheduler.add_process(process)

# Run the scheduler
gantt_chart, burst_time, avg_waiting_time, avg_turnaround_time = scheduler.run()

# Print the results
print("Gantt Chart:")
print(gantt_chart)
print("Burst Time:")
print(burst_time)
print("Average Waiting Time:", avg_waiting_time)
print("Average Turnaround Time:", avg_turnaround_time)

