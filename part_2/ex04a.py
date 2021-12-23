from typing import Final
from z3 import *

NR_OF_STUDENTS: Final = 90
NR_OF_COURSES: Final = 9
NR_OF_ROUNDS: Final = 3

# At most 30 students can enrol for each course in each round
MAX_STUDENTS_PER_COURSE_PER_ROUND: Final = 30

# In total, each student can enrol for at most four courses per round
MAX_ENROLMENTS_STUDENT_PER_ROUD: Final = 4

# A three-dimensional array, containing NR_OF_ROUNDS × NR_OF_COURSES × NR_OF_STUDENTS
# boolean variables
student_follows_course_in_round = [
    [
        [
            Bool(f"r{l+1}c{i+1}s{j+1}")
            for j in range(NR_OF_STUDENTS)
        ]
        for i in range(NR_OF_COURSES)
    ]
    for l in range(NR_OF_ROUNDS)]

s = Solver()

# Converts an array of booleans to an array of integers, where 1 represents a 'True' value
# and 0 represents a 'False' value
def bool_to_int_array(xs):
    return [If(xs[i], 1, 0) for i in range(len(xs))]

for l in range(NR_OF_ROUNDS):
    for i in range(NR_OF_COURSES):
        # constraint; max number of students per course per round
        students_enroled_courses = bool_to_int_array(student_follows_course_in_round[l][i])
        s.add(Sum(students_enroled_courses) <= MAX_STUDENTS_PER_COURSE_PER_ROUND)

for i in range(NR_OF_COURSES):
    for j in range(NR_OF_STUDENTS):
        # constraint; each student follows each course exactly once
        student_follows_course_in_all_rounds = []
        for l in range(NR_OF_ROUNDS):
            student_follows_course_in_all_rounds.append(student_follows_course_in_round[l][i][j])
        course_per_student = bool_to_int_array(student_follows_course_in_all_rounds)
        s.add(Sum(course_per_student) == 1)

for j in range(NR_OF_STUDENTS):
    for l in range(NR_OF_ROUNDS):
        # constraint; max number of enrolments per student
        followed_courses_in_round = []
        for i in range(NR_OF_COURSES):
            followed_courses_in_round.append(student_follows_course_in_round[l][i][j])
        followed_courses_per_round = bool_to_int_array(followed_courses_in_round)
        s.add(Sum(followed_courses_per_round) <= MAX_ENROLMENTS_STUDENT_PER_ROUD)

x = s.check()
s.model()
print(x)