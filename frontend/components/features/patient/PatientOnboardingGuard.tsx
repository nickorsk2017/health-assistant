"use client";

import { useEffect, useState } from "react";

import { usePatientStore } from "@/stores/usePatientStore";

import PatientRegistrationModal from "./PatientRegistrationModal";

const PATIENT_KEY = "health_os_patient_id";

export default function PatientOnboardingGuard() {
  const { setSelectedPatientIdSilent } = usePatientStore();
  const [showRegistration, setShowRegistration] = useState(false);

  useEffect(() => {
    const storedId = localStorage.getItem(PATIENT_KEY);
    if (storedId) {
      setSelectedPatientIdSilent(storedId);
    } else {
      setShowRegistration(true);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return <PatientRegistrationModal isOpen={showRegistration} />;
}
