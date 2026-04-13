"use client";

import { useState } from "react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Modal from "@/components/common/Modal/Modal";
import TextArea from "@/components/common/TextArea/TextArea";
import { usePatientStore } from "@/stores/usePatientStore";
import { useVisitStore } from "@/stores/useVisitStore";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
};

export default function AddHistoryByPromptModal({ isOpen, onClose, onSuccess }: Props) {
  const { selectedPatientId } = usePatientStore();
  const { isProcessingPrompt, promptError, submitByPrompt, clearPromptError } = useVisitStore();
  const [prompt, setPrompt] = useState("");

  const handleClose = () => {
    setPrompt("");
    clearPromptError();
    onClose();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = await submitByPrompt({ user_id: selectedPatientId!, prompt });
    if (ok) {
      setPrompt("");
      onSuccess();
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      title="Add history by prompt"
      onClose={handleClose}
      className="max-w-xl"
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <p className="text-sm text-slate-500">
          Add client history by prompt. Use SOAP methodology if possible. Our AI will
          automatically categorize the data and save it to the patient&apos;s record.
        </p>
        <TextArea
          label="Clinical notes"
          value={prompt}
          rows={8}
          placeholder={`e.g. On March 5 I saw a cardiologist. Chest pain on exertion for 2 weeks. ECG showed normal sinus rhythm. Diagnosed with musculoskeletal pain. Prescribed ibuprofen 400mg and rest.\n\nOn March 20 visited endocrinologist. HbA1c 7.2%, fasting glucose 142 mg/dL. Adjusted metformin to 1000mg twice daily.`}
          onChange={setPrompt}
        />
        {promptError && <Alert message={promptError} onDismiss={clearPromptError} />}
        <div className="flex items-center justify-end gap-2 border-t border-slate-100 pt-4">
          <Button variant="ghost" type="button" onClick={handleClose}>
            Cancel
          </Button>
          <Button type="submit" loading={isProcessingPrompt} disabled={!prompt.trim()}>
            Process & Save
          </Button>
        </div>
      </form>
    </Modal>
  );
}
