from multiprocessing import cpu_count

class CPU:

    def __init__(self, cpus_number):        
        self.cpus = int(cpus_number)
        self.check()

    @staticmethod
    def count_cpus():
        "Count aviable cpus"
        cpus = cpu_count()
        return cpus

    @staticmethod
    def get_avaiable_cpus():
        "Print avaiable cpus"
        print(f"Avaiable CPUs: {CPU.count_cpus()}")

    def check(self):
        "Check if aviable cpus could handle requested cpus. If not use max cpus available"
        available_cpus = CPU.count_cpus()
        if self.cpus > available_cpus:
            self.cpus = available_cpus

