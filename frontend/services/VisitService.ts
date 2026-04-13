const BASE = `${process.env.NEXT_PUBLIC_API_URL}/visits`;
const HISTORY_BASE = `${process.env.NEXT_PUBLIC_API_URL}/history`;

export class VisitService {
  static async recordVisit(data: Entity.CreateVisit): Promise<Entity.RecordVisitResponse> {
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`VisitService.recordVisit failed: ${res.status}`);
    return res.json();
  }

  static async fetchHistory(userId: string, lastDateVisit: string): Promise<Entity.VisitRecord[]> {
    const url = `${HISTORY_BASE}/${userId}?last_date_visit=${lastDateVisit}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`VisitService.fetchHistory failed: ${res.status}`);
    return res.json();
  }

  static async createByPrompt(data: Entity.VisitsByPromptRequest): Promise<Entity.VisitsByPromptResponse> {
    const res = await fetch(`${BASE}/by-prompt`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`VisitService.createByPrompt failed: ${res.status}`);
    return res.json();
  }

  static async updateVisit(visitId: string, data: Entity.UpdateVisit): Promise<Entity.MutateVisitResponse> {
    const res = await fetch(`${BASE}/${visitId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`VisitService.updateVisit failed: ${res.status}`);
    return res.json();
  }

  static async deleteVisit(visitId: string): Promise<Entity.MutateVisitResponse> {
    const res = await fetch(`${BASE}/${visitId}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`VisitService.deleteVisit failed: ${res.status}`);
    return res.json();
  }
}
