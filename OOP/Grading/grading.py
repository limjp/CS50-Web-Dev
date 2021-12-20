import abc

class Assignment(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def lesson(self, student):
        pass

    @abc.abstractmethod
    def check(self, code):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Assignment:
            attrs = set(dir(C))
            if set(cls.__abstractmethods__) <= attrs:
                return True

        return NotImplemented

#Both IntroToPython and Statistics "inherit" from Assignment via duck-typing 
class IntroToPython:
    def lesson(self):
        return f"""
            Hello {self.student}. Define 2 variables,
            an integer named a with value 1
            and a string named b with value 'hello'
        """
    
    def check(self, code):
        return code == "a = 1\nb = 'hello'"

class Statistics(Assignment):
    def lesson(self):
        return (
            "Good work so far, "
            + self.student
            + ". Now calculate the average of the numbers "
            + " 1, 5, 18, -3 and assign to a variable named 'avg'"
        )

    #Code is the student's code
    #Bad example as exec will execute student code right inside grading system giving them access to entire system. 
    def check(self, code):
        import statistics

        code = "import statistics\n" + code

        local_vars = {}
        global_vars = {}
        exec(code, global_vars, local_vars)

        return local_vars.get("avg") == statistics.mean([1, 5, 18, -3])        

#This class uses composition rather than inheritance. Class meant to grade students. Above 2 classes meant to check if answers are correct.
#self.assignment is meant to be either 1 of the 2 classes defined above. 
class AssignmentGrader:
    def __init__(self, student, AssignmentClass):
        self.assignment = AssignmentClass()
        self.assignment.student = student
        self.attempts = 0
        self.correct_attempts = 0

    def check(self, code):
        self.attempts += 1
        result = self.assignment.check(code)
        if result:
            self.correct_attempts += 1

        return result

    #This just proxies through to the same method on the assignment object. We only need this method cause we are using composition rather than inheritance
    def lesson(self):
        return self.assignment.lesson()