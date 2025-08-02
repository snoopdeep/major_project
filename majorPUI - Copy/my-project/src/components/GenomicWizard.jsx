// File: src/components/GenomicWizard.jsx
import React, { useState } from "react";
import axios from "axios";

import FileUpload from "./FileUpload";
import Questionnaire from "./Questionnaire";
import Results from "./Results";

export default function GenomicWizard() {
  // ------------------------------------------------
  // 1) track which step we’re on: "upload", "questionnaire", or "results"
  // ------------------------------------------------
  const [step, setStep] = useState("upload");

  // ------------------------------------------------
  // 2) store the File object + its name for upload
  // ------------------------------------------------
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState("");

  // ------------------------------------------------
  // 3) accumulate questionnaire answers in an object
  // ------------------------------------------------
  const [answers, setAnswers] = useState({});

  // ------------------------------------------------
  // 4) once the backend responds with JSON, stash it here
  //    The Results.jsx component expects at least:
  //      results.anomalyDetected (boolean)
  //      results.shapValues       (object or array)
  //      results.ragSummaryData   (whatever shape your RAG panel expects)
  // ------------------------------------------------
  const [resultsData, setResultsData] = useState(null);

  // ------------------------------------------------
  // Handler: user picks a file in <FileUpload />
  // ------------------------------------------------
  const handleFileChange = (e) => {
    const file = e.target.files[0] || null;
    if (!file) {
      setSelectedFile(null);
      setFileName("");
      return;
    }
    setSelectedFile(file);
    setFileName(file.name);
  };

  // ------------------------------------------------
  // Handler: user clicks “Continue to Medical History”
  //   → upload file to backend, then advance to questionnaire
  // ------------------------------------------------
  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert("Please choose a file before continuing.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("genomicFile", selectedFile);

      // If you need to send any additional metadata, e.g. userId, you can do:
      // formData.append("userId", someUserId);

      const resp = await axios.post(
        "/api/genome/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            // If you have an authentication token, add it here:
            // Authorization: `Bearer ${yourToken}`
          },
        }
      );

      console.log("File upload response:", resp.data);
      // On success, move to the questionnaire step:
      setStep("questionnaire");
    } catch (err) {
      console.error("Error uploading file:", err);
      alert("There was an error uploading the file. Please try again.");
    }
  };

  // ------------------------------------------------
  // Handler: user changes any questionnaire input
  //   → we receive `(e)` where `e.target.name` is the question key
  //     and `e.target.value` is a string or an array (for multi‐select)
  //   → merge into `answers`
  // ------------------------------------------------
  const handleAnswerChange = (e) => {
    const { name, value } = e.target;
    setAnswers((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // ------------------------------------------------
  // Handler: user clicks “Analyze Genome”
  //   → POST { answers } to /api/genome/answers
  //   → the backend must return JSON shaped like:
  //       {
  //         anomalyDetected: true/false,
  //         shapValues: { … } or [ … ],
  //         ragSummaryData: { … },
  //         /* plus any other fields you want to pass along */
  //       }
  //   → we store that payload in `resultsData` and setStep("results")
  // ------------------------------------------------
  const handleQuestionnaireSubmit = async () => {
    // (Optional) quick validation
    if (Object.keys(answers).length === 0) {
      alert("Please answer at least one question before submitting.");
      return;
    }

    try {
      const resp = await axios.post(
        "/api/genome/answers",
        { answers },
        {
          headers: {
            "Content-Type": "application/json",
            // Authorization: `Bearer ${yourToken}`,
          },
        }
      );

      console.log("Questionnaire response:", resp.data);

      // Expect `resp.data` to look like:
      // {
      //   anomalyDetected: true/false,
      //   shapValues: { … },
      //   ragSummaryData: { … },
      //   /* etc. */
      // }

      setResultsData(resp.data);
      setStep("results");
    } catch (err) {
      console.error("Error sending questionnaire:", err);
      alert("There was an error submitting your answers. Please try again.");
    }
  };

  // ------------------------------------------------
  // Handler: “Back to Upload” from the questionnaire
  //   → simply go back to step="upload"
  // ------------------------------------------------
  const handleBackToUpload = () => {
    setStep("upload");
  };

  // ------------------------------------------------
  // Handler: “Run New Analysis” from the Results screen
  //   → reset everything so the user can start fresh
  // ------------------------------------------------
  const handleRerun = () => {
    setStep("upload");
    setSelectedFile(null);
    setFileName("");
    setAnswers({});
    setResultsData(null);
  };

  // ------------------------------------------------
  // Render logic: show whichever step we’re on
  // ------------------------------------------------
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      {step === "upload" && (
        <FileUpload
          fileName={fileName}
          onFileChange={handleFileChange}
          onNext={handleFileUpload}
        />
      )}

      {step === "questionnaire" && (
        <Questionnaire
          answers={answers}
          onChange={handleAnswerChange}
          onBack={handleBackToUpload}
          onSubmit={handleQuestionnaireSubmit}
        />
      )}

      {step === "results" && resultsData && (
        <Results
          fileName={fileName}
          history={answers}
          results={resultsData}
          onRerun={handleRerun}
        />
      )}
    </div>
  );
}
