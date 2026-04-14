"""
Seed script: inserts a 10-visit clinical history for patient Alex Rivera (52 yo)
into the client_history_agent PostgreSQL database.

Hidden diagnosis: Primary Hyperparathyroidism — symptoms are deliberately scattered
across multiple specialties to exercise the doctors_agent's cross-specialty
reasoning.

Usage (from the client_history_agent directory):
    python seeds/seed_clinical_history.py

The script is idempotent when run against an empty table. Running it again will
insert duplicate rows, so only run it once per environment.
"""

import asyncio
import sys
import uuid
from datetime import date

from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings
from db.models import Base, Visit

USER_ID = "45533b8e-9c1a-4d3f-8c2a-123456789abc"

VISITS: list[dict] = [
    # ── Visit 1 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "cardiology",
        "visit_at": date(2026, 1, 10),
        "subjective": (
            "Patient reports mild palpitations over the past 6 weeks and persistent "
            "'brain fog' affecting concentration at work. Denies chest pain, dyspnea, or syncope."
        ),
        "objective": (
            "BP 145/90 mmHg. HR 72 bpm, regular rhythm. ECG: normal sinus rhythm, "
            "no ST-segment changes, no conduction abnormalities. BMI 27.1. Auscultation unremarkable."
        ),
        "assessment": (
            "Essential Hypertension, Stage 1 (I10). Palpitations likely related to "
            "elevated systemic blood pressure. Brain fog is non-specific."
        ),
        "plan": (
            "Started Amlodipine 5mg once daily. Sodium-restricted diet (<2g/day) advised. "
            "Home BP monitoring instructed. Follow-up in 6 weeks."
        ),
    },
    # ── Visit 2 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "mental_health",
        "visit_at": date(2026, 1, 25),
        "subjective": (
            "Presents with significant fatigue over the past 3 months, loss of interest in hobbies "
            "he previously enjoyed (cycling, reading), and reports 'aching bones', particularly in "
            "the legs and lower back. Denies suicidal ideation or self-harm intent."
        ),
        "objective": (
            "PHQ-9 score: 14 (Moderate Depression). Affect is flat and constricted. "
            "No psychomotor retardation. No formal thought disorder. Vital signs within normal limits."
        ),
        "assessment": (
            "Depressive episode, unspecified (F32.9). Somatic complaints — bone ache and fatigue — "
            "noted as potential depressive equivalents or comorbid medical symptom."
        ),
        "plan": (
            "Start Sertraline 50mg daily for 2 weeks, then reassess. Psychoeducation provided. "
            "Sleep hygiene counseling scheduled. Follow-up in 2 weeks. Physical cause of bone pain "
            "to be explored if fatigue does not improve with antidepressant therapy."
        ),
    },
    # ── Visit 3 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "gastroenterology",
        "visit_at": date(2026, 3, 14),
        "subjective": (
            "Chronic constipation for approximately 2 months, opening bowels only every 3-2 days. "
            "Intermittent epigastric pain after meals, non-radiating, no hematemesis or melena. "
            "Reports nausea but no vomiting."
        ),
        "objective": (
            "Abdomen soft, non-distended, mild epigastric tenderness on deep palpation. "
            "Bowel sounds present and normal. No hepatosplenomegaly. Rectal exam deferred."
        ),
        "assessment": (
            "Dyspepsia with functional constipation, consistent with IBS-C pattern. "
            "No alarming features to suggest organic pathology at this stage."
        ),
        "plan": (
            "Dietary fiber supplementation initiated. PEG 3350 (Miralax) prescribed as needed. "
            "Avoid NSAIDs. H. pylori breath test ordered. Follow-up in 6 weeks or sooner if symptoms worsen."
        ),
    },
    # ── Visit 2 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "nephrology",
        "visit_at": date(2026, 3, 20),
        "subjective": (
            "Sudden-onset sharp right-sided flank pain radiating to the groin, rated 8/10, "
            "with associated nausea. Reports one prior episode of kidney stones approximately "
            "2 years ago that passed spontaneously. No fever or dysuria."
        ),
        "objective": (
            "Positive right costovertebral angle tenderness. Urinalysis: microscopic hematuria "
            "(15-20 RBC/hpf), no pyuria, no casts. Serum creatinine 0.9 mg/dL. BUN 18 mg/dL."
        ),
        "assessment": (
            "Nephrolithiasis, right ureter (N20.1). Second episode — recurrent stone disease. "
            "Metabolic etiology to be investigated."
        ),
        "plan": (
            "Increase fluid intake to >2.5L/day. IV ketorolac for acute pain. "
            "CT Urogram (non-contrast) scheduled. Metabolic stone panel deferred pending imaging confirmation."
        ),
    },
    # ── Visit 5 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "endocrinology",
        "visit_at": date(2026, 3, 5),
        "subjective": (
            "Reports persistent thirst and increased urination over the past 2 months. "
            "Self-referred, suspecting diabetes due to family history. Also mentions dry mouth "
            "and occasional mild confusion. Currently on Amlodipine and Sertraline."
        ),
        "objective": (
            "HbA1c: 5.6% (Normal). Fasting glucose: 94 mg/dL. Weight stable at 78 kg (BMI 27.1). "
            "No acanthosis nigricans. No thyroid enlargement on palpation."
        ),
        "assessment": (
            "Polydipsia and polyuria — Diabetes Mellitus ruled out. Symptoms (thirst, confusion, "
            "polyuria) may indicate an alternative metabolic disturbance; further workup warranted."
        ),
        "plan": (
            "Comprehensive metabolic panel (CMP) ordered including serum calcium, phosphorus, "
            "magnesium, and renal function. Thyroid function (TSH, free T4) also ordered. "
            "Follow-up in 3 weeks with lab results."
        ),
    },
    # ── Visit 6 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "cardiology",
        "visit_at": date(2026, 3, 15),
        "subjective": (
            "Blood pressure is better controlled on Amlodipine, patient satisfied. However, "
            "reports worsening 'bone pain' in both legs, described as a deep aching, worse at night. "
            "Denies new cardiac symptoms."
        ),
        "objective": (
            "BP 128/82 mmHg. HR 68 bpm, regular. ECG: normal sinus rhythm, QTc 420ms. "
            "Lower extremity pulses intact bilaterally. No peripheral edema."
        ),
        "assessment": (
            "Hypertension adequately controlled on current regimen. Bone pain is non-cardiac "
            "in origin — no evidence of peripheral vascular disease or heart failure."
        ),
        "plan": (
            "Continue Amlodipine 5mg. Vitamin D (25-OH) level check recommended. "
            "Bone pain referred back to GP for comprehensive metabolic evaluation. "
            "Next cardiac review in 3 months."
        ),
    },
    # ── Visit 7 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "mental_health",
        "visit_at": date(2026, 3, 25),
        "subjective": (
            "Patient reports Sertraline has not significantly improved fatigue after 8 weeks. "
            "States 'I feel like my bones are breaking from the inside.' Sleep has improved slightly "
            "but energy remains very low. No suicidal ideation."
        ),
        "objective": (
            "Patient appears tired and somewhat apathetic but is not clinically depressed in affect "
            "today. PHQ-9 score: 10 (Mild Depression — improved from 14). Thought content normal."
        ),
        "assessment": (
            "Partial response to Sertraline. Treatment-resistant fatigue with prominent somatic "
            "complaints (bone pain) that are disproportionate to the degree of depression — "
            "raises index of suspicion for an underlying medical cause."
        ),
        "plan": (
            "Hold Sertraline dose. Urgently recommend comprehensive blood work including serum "
            "electrolytes, calcium, PTH, and full metabolic panel before increasing psychiatric medication. "
            "Coordinate with GP."
        ),
    },
    # ── Visit 8 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "nephrology",
        "visit_at": date(2026, 2, 5),
        "subjective": (
            "Second acute episode of left-sided flank pain this year. Rates pain 7/10. "
            "Has been drinking adequate fluids as previously instructed. No fever."
        ),
        "objective": (
            "Renal ultrasound: 4mm calculus in the left ureter, no hydronephrosis. "
            "Urinalysis: hematuria 10-15 RBC/hpf. Serum creatinine 1.0 mg/dL. "
            "Urine pH 6.2."
        ),
        "assessment": (
            "Recurrent nephrolithiasis despite adequate hydration. Stone composition "
            "unknown. Recurrence pattern is strongly suggestive of a metabolic disorder "
            "driving hypercalciuria."
        ),
        "plan": (
            "Metabolic stone workup initiated: Serum Calcium, intact PTH, 24-hour urine "
            "calcium/oxalate/citrate/uric acid, Vitamin D (25-OH). Alpha-blocker (Tamsulosin 0.4mg) "
            "started for stone passage. Urgent results to be reviewed within 1 week."
        ),
    },
    # ── Visit 9 ────────────────────────────────────────────────────────────────
    {
        "doctor_type": "endocrinology",
        "visit_at": date(2026, 2, 15),
        "subjective": (
            "Review of lab results ordered by Nephrology. Patient is aware results are pending. "
            "Continues to have bone pain, fatigue, constipation, and has now noticed increased urination."
        ),
        "objective": (
            "Serum Calcium: 11.2 mg/dL (Reference: 8.5–10.2 mg/dL) — ELEVATED. "
            "Albumin: 2.1 g/dL (Normal — corrected calcium confirms true hypercalcemia). "
            "Phosphorus: 2.3 mg/dL (Low-normal). Creatinine: 1.0 mg/dL. "
            "Vitamin D (25-OH): 28 ng/mL (low-normal)."
        ),
        "assessment": (
            "Hypercalcemia, etiology undetermined. In the context of recurrent nephrolithiasis, "
            "bone pain, constipation, fatigue, polydipsia, and polyuria — primary "
            "hyperparathyroidism is the leading differential diagnosis and must be urgently excluded."
        ),
        "plan": (
            "Urgent referral to Endocrinology for intact PTH measurement and clinical review. "
            "Patient advised to maintain high fluid intake and avoid calcium supplements. "
            "Thiazide diuretics held/avoided due to risk of worsening hypercalcemia."
        ),
    },
    # ── Visit 10 ───────────────────────────────────────────────────────────────
    {
        "doctor_type": "endocrinology",
        "visit_at": date(2026, 2, 28),
        "subjective": (
            "Referred for hypercalcemia workup. On reviewing the full history, patient endorses "
            "the classical tetrad: 'Stones' (recurrent kidney stones), 'Bones' (deep bone pain), "
            "'Groans' (abdominal pain, constipation, nausea), and 'Psychic Moans' (fatigue, "
            "depression, cognitive slowing). All symptoms have been progressive over approximately 6 months."
        ),
        "objective": (
            "Intact PTH: 110 pg/mL (Reference: 15–65 pg/mL) — MARKEDLY ELEVATED. "
            "Serum Calcium: 11.2 mg/dL. Phosphorus: 2.1 mg/dL. "
            "24-hour urine calcium: 380 mg/day (elevated, >250 mg/day). "
            "DEXA scan: T-score -2.1 at lumbar spine (Osteoporosis range)."
        ),
        "assessment": (
            "Primary Hyperparathyroidism (E21.0). Autonomous overproduction of PTH leading to "
            "hypercalcemia, hypophosphatemia, hypercalciuria, nephrolithiasis, and metabolic bone disease. "
            "Symptomatic disease with end-organ involvement (kidneys, bone). Depression and cognitive "
            "symptoms are consistent with neurobehavioral manifestations of hypercalcemia."
        ),
        "plan": (
            "Sestamibi parathyroid scintigraphy + neck ultrasound ordered to localise parathyroid adenoma. "
            "Referred to Head & Neck Surgery for parathyroidectomy consultation — surgical cure expected. "
            "Cinacalcet considered as bridge if surgery is delayed. "
            "Bisphosphonate (Alendronate) initiated for osteoporosis. "
            "Sertraline and psychiatric follow-up to be reassessed post-parathyroidectomy as psychiatric "
            "symptoms are expected to resolve with normalisation of serum calcium."
        ),
    },
]


def _build_database_url() -> str:
    return (
        f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )


async def seed() -> None:
    database_url = _build_database_url()
    engine = create_async_engine(database_url, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        for i, visit_data in enumerate(VISITS, start=1):
            visit_id = uuid.uuid4()
            await session.execute(
                insert(Visit).values(
                    id=visit_id,
                    user_id=USER_ID,
                    **visit_data,
                )
            )
            await session.commit()

    await engine.dispose()


def run() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    run()
