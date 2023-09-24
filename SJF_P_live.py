current_time = 0


class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time


class SJF_P():
    def __init__(self):
        super().__init__()
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def run(self, current_time):
        self.processes.sort(key=lambda p: p.arrival_time)

        gantt_chart = []  # initialize the Gantt chart
        burst_time = []
        waiting_time = []
        turnaround_time = []
        
        remaining_processes = self.processes.copy()

        while remaining_processes:
            print(str(remaining_processes[0].name))
            # find the shortest job available at current time
            min_burst_time = float('inf')
            shortest_job = None
            for process in remaining_processes:
                
                if process.arrival_time <= current_time and process.remaining_time < min_burst_time:
                    shortest_job = process
                    min_burst_time = process.remaining_time


            # update Gantt chart
            if not gantt_chart:
                # If Gantt chart is empty, add the first process
                gantt_chart.append((shortest_job.name, current_time, current_time+1))
            elif gantt_chart[-1][0] == shortest_job.name:
                # If the last process in Gantt chart is the same as the current process, update its end time
                gantt_chart[-1] = (shortest_job.name, gantt_chart[-1][1], current_time+1)
            else:
                # If the last process in Gantt chart is different from the current process, add the current process
                gantt_chart.append((shortest_job.name, current_time, current_time+1))

            # reduce remaining time of current job and update current time
            shortest_job.remaining_time -= 1
            current_time += 1

            print("here 111111111111111111111111111111111")
            print("remaining_time:  " + str(shortest_job.remaining_time))

            # add completed job to the lists
            if shortest_job.remaining_time <= 0:
                
                burst_time.append([shortest_job.name, shortest_job.burst_time])

                waiting_time.append(current_time - shortest_job.arrival_time - shortest_job.burst_time)
                turnaround_time.append(current_time - shortest_job.arrival_time)
                remaining_processes.remove(shortest_job)
                print("here 2222222222222222222222222")

            print("enfffffffffdddddddddddddddddd")

        # calculate the average waiting and turnaround times
        avg_waiting_time = sum(waiting_time) / len(self.processes)
        avg_turnaround_time = sum(turnaround_time) / len(self.processes)

        # add the end time for the last process in the Gantt chart
        gantt_chart[-1] = (gantt_chart[-1][0], gantt_chart[-1][1], current_time)

        slot_gantt_chart = []

        for i in range(len(gantt_chart)):
                for j in range(gantt_chart[i][2] - gantt_chart[i][1]):
                    slot_gantt_chart.append(gantt_chart[i][0])

        self.processes.clear()

        return slot_gantt_chart, burst_time, avg_waiting_time, avg_turnaround_time

rem = []
ask = True
# Get user input for processes
addProcess = "no"

counter = 0
j = 0   

# Create the SJF Preemptive scheduler
scheduler = SJF_P()

while True:
    processes = []
    if ask == True:
        addProcess = input("do you want to add process? ")

    if addProcess.lower() == "close":
        break

    if addProcess.lower() == "yes":

        limit = int(input("Enter number of processes: "))
        for i in range(limit):
            name = input("Enter name of the process: ")
            bur = int(input("Enter burst time: "))
            processes.append(Process(name, counter, bur))

        # Add the processes to the scheduler
        for process in processes:
            scheduler.add_process(process)

        # Run the scheduler
        gantt_chart, burst_time, avg_waiting_time, avg_turnaround_time = scheduler.run(current_time)

    counter += 1




    for i in range(len(burst_time)):
        process_name = burst_time[i][0]
        existing_process = [process for process in rem if process[0] == process_name]
        if not existing_process:
            rem.append(burst_time[i])

    

    if j >= len(gantt_chart):
        break
    else:
        # Print the results

        for i in range(len(rem)):
            if gantt_chart[j] == rem[i][0]:
                if rem[i][1] > 0:
                    ask = True
                    for i in range(len(rem)):
                        if rem[i][0] == gantt_chart[j]:
                            rem[i][1] = rem[i][1] - 1    
                    c = 0
                    for i in range(len(rem)):
                        c = c + rem[i][1]
                    if c >= 0:
                        print(gantt_chart[j])
                        print(rem)
                else:
                    ask = False

        # # print burst time table live
        # for i in range(len(burst_time)):
        #     if burst_time[i][0] == gantt_chart[j]:
        #         burst_time[i][1] = burst_time[i][1] - 1    
        
        # print(burst_time)

    j += 1



print("Average Waiting Time:", avg_waiting_time)
print("Average Turnaround Time:", avg_turnaround_time)
