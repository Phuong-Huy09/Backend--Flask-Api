

students = []
student_id_counter = 1

def get_all_students():
    return students

def get_student_by_id(student_id):
    return next((s for s in students if s["id"] == student_id), None)

def create_student(data):
    global student_id_counter
    new_student = {
        "id": student_id_counter,
        "name": data.get("name"),
        "email": data.get("email"),
        "major": data.get("major")
    }
    students.append(new_student)
    student_id_counter += 1
    return new_student

def update_student(student_id, data):
    student = get_student_by_id(student_id)
    if student:
        student.update({
            "name": data.get("name", student["name"]),
            "email": data.get("email", student["email"]),
            "major": data.get("major", student["major"])
        })
        return student
    return None

def delete_student(student_id):
    global students
    student = get_student_by_id(student_id)
    if student:
        students = [s for s in students if s["id"] != student_id]
        return True
    return False
