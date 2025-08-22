
tutors = []
tutor_id_counter = 1

def get_all_tutors():
    return tutors

def get_tutor_by_id(tutor_id):
    return next((t for t in tutors if t["id"] == tutor_id), None)

def create_tutor(data):
    global tutor_id_counter
    new_tutor = {
        "id": tutor_id_counter,
        "name": data.get("name"),
        "email": data.get("email"),
        "subject": data.get("subject")
    }
    tutors.append(new_tutor)
    tutor_id_counter += 1
    return new_tutor

def update_tutor(tutor_id, data):
    tutor = get_tutor_by_id(tutor_id)
    if tutor:
        tutor.update({
            "name": data.get("name", tutor["name"]),
            "email": data.get("email", tutor["email"]),
            "subject": data.get("subject", tutor["subject"])
        })
        return tutor
    return None

def delete_tutor(tutor_id):
    global tutors
    tutor = get_tutor_by_id(tutor_id)
    if tutor:
        tutors = [t for t in tutors if t["id"] != tutor_id]
        return True
    return False
