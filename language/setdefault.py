student_grades = {}

# Prints nothing because only {} was returned
math_grades = student_grades.get('Alice', {})
math_grades['math'] = 90
print(student_grades)

# Assigned the default value then returns that to you. This allows you
# to modify the original dictionary.
math_grades = student_grades.setdefault('Alice', {})
math_grades['math'] = 90
print(student_grades)
