declare namespace Entity {
  type Gender = "male" | "female" | "other";

  type AppRole = "doctor" | "patient";

  type MockPatient = {
    id: string;
    name: string;
    date_of_birth?: string;
    gender?: Gender;
  };

  type NewPatientForm = {
    name: string;
    date_of_birth: string;
    gender: Gender;
    email: string;
  };
}
