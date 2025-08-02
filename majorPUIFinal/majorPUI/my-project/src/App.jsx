import { useState } from 'react';
import Header from './components/Header.jsx';
import FileUpload from './components/FileUpload.jsx'
import Footer from './components/Footer.jsx'
import Questionnaire from './components/Questionnaire.jsx'
import Spinner from './components/Spinner.jsx'
import Results from './components/Results.jsx';
// import ShapPanel from './components/ShapPanel.jsx';


// Main App Component
function App() {
  const [step, setStep] = useState(1);
  const [fileName, setFileName] = useState('');
  const [historyAnswers, setHistoryAnswers] = useState({
    hereditaryCardio: '',
    familyCancer: '',
    bmiOver30: '',
    priorGeneTherapy: '',
  });
  const [showSpinner, setShowSpinner] = useState(false);

  const hardcodedResults = {
    anomalyDetected: true,
    reconstructionError: 0.024,
    threshold: 0.01,
    shapValues: [
      { feature: 'TP53', value: 'Breast Cancer Risk' },
      { feature: 'BRCA1', value: 'Ovarian Cancer Risk' },
      { feature: 'CFTR', value: 'Cystic Fibrosis' },
      { feature: 'MLH1', value: 'Lynch Syndrome' },
      { feature: 'BRCA2', value: 'Pancreatic Cancer Risk' },
      { feature: 'PTEN', value: 'Cowden Syndrome' },
      { feature: 'EGFR', value: 'Lung Cancer Risk' },
      { feature: 'KRAS', value: 'Colorectal Cancer Risk' },
      { feature: 'APC', value: 'Familial Adenomatous Polyposis' },
      { feature: 'RB1', value: 'Retinoblastoma Risk' },
    ],
    ragSummaryData: {
      TP53: `TP53 (c.215C>G): This missense mutation is pathogenic in Li-Fraumeni syndrome cases. The disruption of the p53 DNA-binding domain impairs cell-cycle regulation, increasing cancer susceptibility. Given your medical history, enhanced screening protocols are recommended.`,
      BRCA1: `BRCA1 (c.5123_5125del GAC): This in-frame deletion correlates with early-onset breast cancer. The variant shows high penetrance and, combined with your family history, warrants immediate genetic counseling and preventive measures.`,
      MLH1: `MLH1 (splice-site variant): This anomaly suggests mismatch repair deficiency associated with Lynch syndrome. Patients typically require enhanced colorectal cancer screening starting at age 20-25.`,
      CFTR: `CFTR variants can cause cystic fibrosis or CFTR-related disorders. This particular variant may contribute to pancreatic insufficiency and respiratory complications requiring specialized care.`,
      Recommendation: `Immediate genetic counseling is recommended. Consider confirmatory Sanger sequencing, cascade family testing, and enhanced screening protocols for identified cancer risks.`,
      References: `ClinVar, OMIM, and peer-reviewed literature from 2024 support these interpretations.`,
    },
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
    }
  };

  const handleHistoryChange = (e) => {
    const { name, value } = e.target;
    setHistoryAnswers((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const goToQuestionnaire = () => {
    if (!fileName) {
      alert('Please select a genomic file before proceeding.');
      return;
    }
    setStep(2);
  };

  const submitHistory = () => {
    setShowSpinner(true);
    setTimeout(() => {
      setShowSpinner(false);
      setStep(3);
    }, 3000);
  };

  const rerunAnalysis = () => {
    setStep(1);
    setFileName('');
    setHistoryAnswers({
      hereditaryCardio: '',
      familyCancer: '',
      bmiOver30: '',
      priorGeneTherapy: '',
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header />
      <main className="container mx-auto px-6 py-12">
        {step === 1 && (
          <FileUpload
            fileName={fileName}
            onFileChange={handleFileChange}
            onNext={goToQuestionnaire}
          />
        )}
        {step === 2 && (
          <Questionnaire
            answers={historyAnswers}
            onChange={handleHistoryChange}
            onBack={() => setStep(1)}
            onSubmit={submitHistory}
          />
        )}
        {step === 3 && !showSpinner && (
          <Results
            fileName={fileName}
            history={historyAnswers}
            results={hardcodedResults}
            onRerun={rerunAnalysis}
          />
        )}
      </main>
      {showSpinner && <Spinner />}
      <Footer />
    </div>
  );
}

export default App;


