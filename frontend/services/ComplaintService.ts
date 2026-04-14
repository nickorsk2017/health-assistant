const BASE = `${process.env.NEXT_PUBLIC_API_URL}/complaints`;

export class ComplaintService {
  static async getAll(userId: string): Promise<Entity.Complaint[]> {
    const res = await fetch(`${BASE}?user_id=${encodeURIComponent(userId)}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`ComplaintService.getAll failed: ${res.status}`);
    return res.json();
  }

  static async create(userId: string, form: Entity.CreateComplaint): Promise<Entity.Complaint> {
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, ...form }),
    });
    if (!res.ok) throw new Error(`ComplaintService.create failed: ${res.status}`);
    return res.json();
  }

  static async update(
    complaintId: string,
    userId: string,
    form: Entity.UpdateComplaint,
  ): Promise<Entity.Complaint> {
    const res = await fetch(`${BASE}/${complaintId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, ...form }),
    });
    if (!res.ok) throw new Error(`ComplaintService.update failed: ${res.status}`);
    return res.json();
  }

  static async markRead(complaintId: string): Promise<void> {
    const res = await fetch(`${BASE}/${complaintId}/read`, { method: "PATCH" });
    if (!res.ok) throw new Error(`ComplaintService.markRead failed: ${res.status}`);
  }

  static async remove(complaintId: string): Promise<void> {
    const res = await fetch(`${BASE}/${complaintId}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`ComplaintService.remove failed: ${res.status}`);
  }
}
