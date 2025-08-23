class BookingService:
    def __init__(self):
        # Tạm dùng list giả lập database
        self.bookings = []
        self.next_id = 1

    def get_all_bookings(self):
        return self.bookings

    def get_booking_by_id(self, booking_id):
        return next((b for b in self.bookings if b["id"] == booking_id), None)

    def create_booking(self, data):
        booking = {
            "id": self.next_id,
            "student_name": data.get("student_name"),
            "subject_id": data.get("subject_id"),
            "time": data.get("time")
        }
        self.bookings.append(booking)
        self.next_id += 1
        return booking