class SubjectService:
    def __init__(self):
        # Tạm dùng list giả lập database
        self.subjects = []
        self.next_id = 1

    def get_all_subjects(self):
        return self.subjects

    def get_subject_by_id(self, subject_id):
        return next((s for s in self.subjects if s["id"] == subject_id), None)

    def create_subject(self, data):
        subject = {
            "id": self.next_id,
            "name": data.get("name"),
            "description": data.get("description")
        }
        self.subjects.append(subject)
        self.next_id += 1
        return subject