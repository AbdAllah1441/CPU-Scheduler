class Process:
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority


class Priority_NP():
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        self.processes.sort(key=lambda p: (p.priority, p.arrival_time))

        gantt_chart = []
        burst_time = []
        waiting_time = []
        turnaround_time = []
        current_time = 0
        remaining_processes = self.processes.copy()

        while remaining_processes:
            # find the process with highest priority available at current time
            highest_priority = float('inf')
            highest_priority_process = None
            for process in remaining_processes:
                if process.arrival_time <= current_time and process.priority < highest_priority:
                    highest_priority_process = process
                    highest_priority = process.priority

            # calculate waiting time and update current time
            waiting_time.append(current_time - highest_priority_process.arrival_time)
            current_time += highest_priority_process.burst_time

            # calculate turnaround time and update lists
            turnaround_time.append(current_time - highest_priority_process.arrival_time)
            # name - start time - end time
            gantt_chart.append((highest_priority_process.name, current_time - highest_priority_process.burst_time, current_time))
            burst_time.append([highest_priority_process.name, highest_priority_process.burst_time])

            # remove the processed job from the list
            remaining_processes.remove(highest_priority_process)

        # calculate the average waiting and turnaround times
        avg_waiting_time = sum(waiting_time) / len(self.processes)
        avg_turnaround_time = sum(turnaround_time) / len(self.processes)

        return gantt_chart, burst_time, avg_waiting_time, avg_turnaround_time

processes = []

limit = int(input("enter number of processes: "))

for i in range(limit):
    name = input("enter name of the process: ")
    arr = int(input("enter arrival time: ")) 
    bur = int(input("enter burst time: ")) 
    pr = int(input("enter priority: "))
    processes.append(Process(name, arr, bur, pr))



scheduler = Priority_NP()
for process in processes:
    scheduler.add_process(process)

gantt_chart, burst_time, avg_waiting_time, avg_turnaround_time = scheduler.run()

print("Gantt Chart:")
print(gantt_chart)

print("Burst Time:")
print(burst_time)

print("Average Waiting Time:", avg_waiting_time)
print("Average Turnaround Time:", avg_turnaround_time)
