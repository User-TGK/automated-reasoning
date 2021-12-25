from typing import Final
from z3 import *

NR_OF_STUDENTS: Final = 90
NR_OF_COURSES: Final = 9
NR_OF_ROUNDS: Final = 4

# At most 30 students can enrol for each course in each round
MAX_STUDENTS_PER_COURSE_PER_ROUND: Final = 45

# In total, each student can enrol for at most four courses per round
MAX_ENROLMENTS_STUDENT_PER_ROUD: Final = 3

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

def is_calculus_one_course(course_number):
    return course_number == 0

def is_calculus_two_course(course_number):
    return course_number == 1

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

for j in range(NR_OF_STUDENTS):
    calculus_one_courses = []
    calculus_two_courses = []

    for i in range(NR_OF_COURSES):
        if (is_calculus_one_course(i)):
            for l in range(NR_OF_ROUNDS):
                calculus_one_courses.append(student_follows_course_in_round[l][i][j])
        elif (is_calculus_two_course(i)):
            for l in range(NR_OF_ROUNDS):
                calculus_two_courses.append(student_follows_course_in_round[l][i][j])
        else:
            continue
    
    calculus_one_of_student = bool_to_int_array(calculus_one_courses)
    s.add(calculus_two_courses[0] == False)
    s.add(Implies(calculus_two_courses[1], calculus_one_courses[0]))
    s.add(Implies(calculus_two_courses[2], Or(calculus_one_courses[0], calculus_one_courses[1])))
    s.add(Implies(calculus_two_courses[3], Or(calculus_one_courses[0], calculus_one_courses[1], calculus_one_courses[2])))

for i in range(NR_OF_COURSES):
    if (not is_calculus_two_course(i)):
        continue

    for j in range(NR_OF_STUDENTS):
        s.add(Implies(student_follows_course_in_round[1][i][j], student_follows_course_in_round[0][i-1][j]))
        s.add(Implies(student_follows_course_in_round[2][i][j], 
                        And(student_follows_course_in_round[1][i-1][j], student_follows_course_in_round[0][i-1][j])))

x = s.check()
print(x)
if (x == sat):
    print('')
    m = s.model()
    for l in range(NR_OF_ROUNDS):
        print('Round ' + str(l + 1) + ': ')
        print('-----------------------------------------------------------')

        for i in range(NR_OF_COURSES):
            if (is_calculus_one_course(i)): 
                print('    Course ' + str(i + 1) + ' (Calculus 1): ')
            elif (is_calculus_two_course(i)):
                print('    Course ' + str(i + 1) + ' (Calculus 2):')
            else:
                print('    Course ' + str(i + 1) + ':')

            number_of_students = 0

            for j in range(NR_OF_STUDENTS):
                if (m[student_follows_course_in_round[l][i][j]]):
                    print('        student ' + str(j + 1))
                    number_of_students += 1
            print('    Total students: ' + str(number_of_students))
            print('')
# print(m)