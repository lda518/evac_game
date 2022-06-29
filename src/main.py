from master import Master
ITERATIONS = 5
if __name__ == '__main__':
    for i in range(ITERATIONS):
        master = Master()
        master.normal_run()
        master.save()
        master.non_adaptive()
        master.save()
