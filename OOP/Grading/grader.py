from OOP.Grading.grading import AssignmentGrader
from grading import Assignment
import uuid

class Grader:
    #Student_grader stores student name as key and an instance of AssignmentGrader as value
    #assignment_class stores id as key and the assignement_class itself as value
    def __init__(self):
        self.student_graders = {}
        self.assignment_classes = {}

    #assignment_class is meant to be an actual class not an instance of the class. This is cause classes are objects that can be passed around too and can be passed around
    #Therefore we can register a class like IntroToPython which was defined earlier without instantiating it
    #Method first checks whether the class is a subclass of the Assignment class. If it does not then it raises an exception
    #Then it generates a random id for that specific assignemnt which is stored in the dict assignment_class
    def register(self, assignment_class):
        if not issubclass(assignment_class, Assignment):
            raise RuntimeError(
                "Your class does not have the right methods"
            )

        id = uuid.uuid4()
        self.assignment_classes[id] = assignment_class
        return id

    #Allow student to start working on an assignment given the ID of that assignment
    #Constructs an instance of the AssignmentGrader class defined earlier and store it in the dict student_grader
    def start_assignment(self, student, id):
        self.student_graders[student] = AssignmentGrader(
            student, self.assignment_classes[id]
        )
    
    def get_lesson(self, student):
        assignment = self.student_graders[student]
        return assignment.lesson()
    
    def check_assignment(self, student, code):
        assignment = self.student_graders[student]
        return assignment.check(code)

    def assignment_summary(self, student):
        grader = self.student_graders[student]
        return f"""
        {student}'s attempts at {grader.assigment.__class__.__name__}:
        attemps: {grader.attempts}
        correct: {grader.correct_attemps}

        passed: {grader.correct_attemps > 0}
        """