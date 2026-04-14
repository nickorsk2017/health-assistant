const BASE = `${process.env.NEXT_PUBLIC_API_URL}/patients`;

type ApiPatient = {
  id: string;
  full_name: string;
  dob: string;
  gender: string;
  email?: string | null;
};

function toEntity(p: ApiPatient): Entity.MockPatient {
  return {
    id: p.id,
    name: p.full_name,
    date_of_birth: p.dob,
    gender: p.gender as Entity.Gender,
  };
}

export class PatientService {
  static async getAll(): Promise<Entity.MockPatient[]> {
    const res = await fetch(BASE, { cache: "no-store" });
    if (!res.ok) throw new Error(`PatientService.getAll failed: ${res.status}`);
    const data: ApiPatient[] = await res.json();
    return data.map(toEntity);
  }

  static async create(form: Entity.NewPatientForm): Promise<Entity.MockPatient> {
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: form.name,
        dob: form.date_of_birth,
        gender: form.gender,
        email: form.email || null,
      }),
    });
    if (!res.ok) throw new Error(`PatientService.create failed: ${res.status}`);
    return toEntity(await res.json());
  }
}
