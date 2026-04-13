declare namespace Entity {
  type DoctorType =
    | "oncology"
    | "gastroenterology"
    | "cardiology"
    | "hematology"
    | "nephrology"
    | "nutrition"
    | "endocrinology"
    | "mental_health"
    | "pulmonology"
    | "general_practitioner";

  type CreateVisit = {
    user_id: string;
    doctor_type: DoctorType;
    visit_at: string;
    subjective: string;
    objective: string;
    assessment: string;
    plan: string;
  };

  type VisitRecord = {
    visit_id: string;
    user_id: string;
    doctor_type: string;
    visit_at: string;
    subjective: string;
    objective: string;
    assessment: string;
    plan: string;
    created_at: string;
  };

  type RecordVisitResponse = {
    success: boolean;
    visit_id: string;
  };

  type VisitsByPromptRequest = {
    user_id: string;
    prompt: string;
  };

  type VisitsByPromptResponse = {
    success: boolean;
    count: number;
  };

  type UpdateVisit = {
    visit_at: string;
    subjective: string;
    objective: string;
    assessment: string;
    plan: string;
  };

  type MutateVisitResponse = {
    success: boolean;
  };
}
