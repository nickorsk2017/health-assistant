declare namespace Entity {
  type Appointment = {
    appointment_id: string;
    complaint_id: string;
    user_id: string;
    appointment_date: string;
    doctor_type: string;
    problem_notes: string;
    created_at: string;
  };

  type CreateAppointment = {
    complaint_id: string;
    user_id: string;
    appointment_date: string;
    doctor_type: string;
    problem_notes: string;
  };
}
