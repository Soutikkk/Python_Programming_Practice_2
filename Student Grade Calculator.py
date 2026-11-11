
print("===== STUDENT GRADE CALCULATOR =====")

name = input("Enter student name: ")

marks = []

for i in range(1, 6):
    mark = float(input(f"Enter marks for subject {i}: "))
    marks.append(mark)

total = sum(marks)
percentage = total / 5

if any(mark < 40 for mark in marks):
    grade = "F"
    result = "FAIL"
elif percentage >= 90:
    grade = "A+"
    result = "PASS"
elif percentage >= 80:
    grade = "A"
    result = "PASS"
elif percentage >= 70:
    grade = "B"
    result = "PASS"
elif percentage >= 60:
    grade = "C"
    result = "PASS"
else:
    grade = "D"
    result = "PASS"

print("\n===== RESULT =====")
print("Name:", name)
print("Total Marks:", total, "/ 500")
print("Percentage:", round(percentage, 2), "%")
print("Grade:", grade)
print("Result:", result)
