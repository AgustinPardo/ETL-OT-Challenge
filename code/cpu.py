from multiprocessing import cpu_count


class CPU:
    """Class to store and check cpu info""" 

    def __init__(self, cpus_number):        
        self.cpus = int(cpus_number)
        self.check()

    @staticmethod
    def count_cpus():
        """Count aviable cpus""" 

        cpus = cpu_count()
        return cpus

    @staticmethod
    def get_avaiable_cpus():
        """Print avaiable cpus"""

        print(f"Avaiable CPUs: {CPU.count_cpus()}")

    def check(self):
        """Check CPUs input value"""

        if self.cpus < 1:
            raise Exception(f'{self.cpus} is not a valid CPUs number usage')
        # If available CPUs could not handle requested CPUs, use max available
        available_cpus = CPU.count_cpus()
        if self.cpus > available_cpus:
            self.cpus = available_cpus
