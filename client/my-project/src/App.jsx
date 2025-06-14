// import { useState } from 'react';
import Header from './components/Header.jsx';
import FileUpload from './components/FileUpload.jsx'
import Footer from './components/Footer.jsx'
import Questionnaire from './components/Questionnaire.jsx'
import Spinner from './components/Spinner.jsx'
import Results from './components/Results.jsx';


// // Main App Component
// function App() {
//   const [step, setStep] = useState(1);
//   const [fileName, setFileName] = useState('');
//   const [historyAnswers, setHistoryAnswers] = useState({
//     hereditaryCardio: '',
//     familyCancer: '',
//     bmiOver30: '',
//     priorGeneTherapy: '',
//   });
//   const [showSpinner, setShowSpinner] = useState(false);

//   const hardcodedResults = {
//     anomalyDetected: true,
//     reconstructionError: 0.024,
//     threshold: 0.01,
//     shapValues: [
//       { feature: 'TP53', value: 'Breast Cancer Risk' },
//       { feature: 'BRCA1', value: 'Ovarian Cancer Risk' },
//       { feature: 'CFTR', value: 'Cystic Fibrosis' },
//       { feature: 'MLH1', value: 'Lynch Syndrome' },
//       { feature: 'BRCA2', value: 'Pancreatic Cancer Risk' },
//       { feature: 'PTEN', value: 'Cowden Syndrome' },
//       { feature: 'EGFR', value: 'Lung Cancer Risk' },
//       { feature: 'KRAS', value: 'Colorectal Cancer Risk' },
//       { feature: 'APC', value: 'Familial Adenomatous Polyposis' },
//       { feature: 'RB1', value: 'Retinoblastoma Risk' },
//     ],
//     ragSummaryData: {
//       TP53: `TP53 (c.215C>G): This missense mutation is pathogenic in Li-Fraumeni syndrome cases. The disruption of the p53 DNA-binding domain impairs cell-cycle regulation, increasing cancer susceptibility. Given your medical history, enhanced screening protocols are recommended.`,
//       BRCA1: `BRCA1 (c.5123_5125del GAC): This in-frame deletion correlates with early-onset breast cancer. The variant shows high penetrance and, combined with your family history, warrants immediate genetic counseling and preventive measures.`,
//       MLH1: `MLH1 (splice-site variant): This anomaly suggests mismatch repair deficiency associated with Lynch syndrome. Patients typically require enhanced colorectal cancer screening starting at age 20-25.`,
//       CFTR: `CFTR variants can cause cystic fibrosis or CFTR-related disorders. This particular variant may contribute to pancreatic insufficiency and respiratory complications requiring specialized care.`,
//       Recommendation: `Immediate genetic counseling is recommended. Consider confirmatory Sanger sequencing, cascade family testing, and enhanced screening protocols for identified cancer risks.`,
//       References: `ClinVar, OMIM, and peer-reviewed literature from 2024 support these interpretations.`,
//     },
//   };

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (file) {
//       setFileName(file.name);
//     }
//   };

//   const handleHistoryChange = (e) => {
//     const { name, value } = e.target;
//     setHistoryAnswers((prev) => ({
//       ...prev,
//       [name]: value,
//     }));
//   };

//   const goToQuestionnaire = () => {
//     if (!fileName) {
//       alert('Please select a genomic file before proceeding.');
//       return;
//     }
//     setStep(2);
//   };

//   const submitHistory = () => {
//     setShowSpinner(true);
//     setTimeout(() => {
//       setShowSpinner(false);
//       setStep(3);
//     }, 3000);
//   };

//   const rerunAnalysis = () => {
//     setStep(1);
//     setFileName('');
//     setHistoryAnswers({
//       hereditaryCardio: '',
//       familyCancer: '',
//       bmiOver30: '',
//       priorGeneTherapy: '',
//     });
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
//       <Header />
//       <main className="container mx-auto px-6 py-12">
//         {step === 1 && (
//           <FileUpload
//             fileName={fileName}
//             onFileChange={handleFileChange}
//             onNext={goToQuestionnaire}
//           />
//         )}
//         {step === 2 && (
//           <Questionnaire
//             answers={historyAnswers}
//             onChange={handleHistoryChange}
//             onBack={() => setStep(1)}
//             onSubmit={submitHistory}
//           />
//         )}
//         {step === 3 && !showSpinner && (
//           <Results
//             fileName={fileName}
//             history={historyAnswers}
//             results={hardcodedResults}
//             onRerun={rerunAnalysis}
//           />
//         )}
//       </main>
//       {showSpinner && <Spinner />}
//       <Footer />
//     </div>
//   );
// }

// export default App;


import { useState } from 'react';
// import Header from './components/Header.jsx';
// import FileUpload from './components/FileUpload.jsx'
// import Footer from './components/Footer.jsx'
// import Questionnaire from './components/Questionnaire.jsx'
// import Spinner from './components/Spinner.jsx'
// import Results from './components/Results.jsx';

// // Main App Component
// function App() {
//   const [step, setStep] = useState(1);
//   const [fileName, setFileName] = useState('');
//   const [fileData, setFileData] = useState(null); // Store the actual file
//   const [historyAnswers, setHistoryAnswers] = useState({
//     ethnicBackground: '',
//     familyConditions: [],
//     familyCancerCount: '',
//     geneticTestingHistory: '',
//     // Add other fields as needed from your questionnaire
//   });
//   const [showSpinner, setShowSpinner] = useState(false);
//   const [results, setResults] = useState(null);
//   const [error, setError] = useState(null);

//   const hardcodedResults = {
//     anomalyDetected: true,
//     reconstructionError: 0.024,
//     threshold: 0.01,
//     shapValues: [
//       { feature: 'TP53', value: 'Breast Cancer Risk' },
//       { feature: 'BRCA1', value: 'Ovarian Cancer Risk' },
//       { feature: 'CFTR', value: 'Cystic Fibrosis' },
//       { feature: 'MLH1', value: 'Lynch Syndrome' },
//       { feature: 'BRCA2', value: 'Pancreatic Cancer Risk' },
//       { feature: 'PTEN', value: 'Cowden Syndrome' },
//       { feature: 'EGFR', value: 'Lung Cancer Risk' },
//       { feature: 'KRAS', value: 'Colorectal Cancer Risk' },
//       { feature: 'APC', value: 'Familial Adenomatous Polyposis' },
//       { feature: 'RB1', value: 'Retinoblastoma Risk' },
//     ],
//     ragSummaryData: {
//       TP53: `TP53 (c.215C>G): This missense mutation is pathogenic in Li-Fraumeni syndrome cases. The disruption of the p53 DNA-binding domain impairs cell-cycle regulation, increasing cancer susceptibility. Given your medical history, enhanced screening protocols are recommended.`,
//       BRCA1: `BRCA1 (c.5123_5125del GAC): This in-frame deletion correlates with early-onset breast cancer. The variant shows high penetrance and, combined with your family history, warrants immediate genetic counseling and preventive measures.`,
//       MLH1: `MLH1 (splice-site variant): This anomaly suggests mismatch repair deficiency associated with Lynch syndrome. Patients typically require enhanced colorectal cancer screening starting at age 20-25.`,
//       CFTR: `CFTR variants can cause cystic fibrosis or CFTR-related disorders. This particular variant may contribute to pancreatic insufficiency and respiratory complications requiring specialized care.`,
//       Recommendation: `Immediate genetic counseling is recommended. Consider confirmatory Sanger sequencing, cascade family testing, and enhanced screening protocols for identified cancer risks.`,
//       References: `ClinVar, OMIM, and peer-reviewed literature from 2024 support these interpretations.`,
//     },
//   };

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (file) {
//       setFileName(file.name);
//       setFileData(file); // Store the actual file object
//       setError(null);
//     }
//   };

//   const handleHistoryChange = (e) => {
//     const { name, value } = e.target;
//     setHistoryAnswers((prev) => ({
//       ...prev,
//       [name]: value,
//     }));
//   };

//   const goToQuestionnaire = () => {
//     if (!fileName) {
//       alert('Please select a genomic file before proceeding.');
//       return;
//     }
//     setStep(2);
//   };

//   // Submit questionnaire and process with ML model
//   const submitHistory = async () => {
//     if (!fileData) {
//       setError('No file uploaded');
//       return;
//     }

//     setShowSpinner(true);
//     setError(null);

//     try {
//       // Create FormData to send file and questionnaire data
//       const formData = new FormData();
//       formData.append('file', fileData);
//       formData.append('questionnaire', JSON.stringify(historyAnswers));
//       formData.append('fileName', fileName);

//       // Send to Flask backend
//       const response = await fetch('http://localhost:5000/api/analyze', {
//         method: 'POST',
//         body: formData,
//       });
//       console.log('response :: ',response);

//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       const result = await response.json();
//       setResults(result);
//       setStep(3);
//     } catch (err) {
//       console.error('Analysis error:', err);
//       setError(err.message || 'An error occurred during analysis');
//       // Fallback to hardcoded results for demo purposes
//       console.log('Using hardcoded results as fallback');
//       setResults(hardcodedResults);
//       setStep(3);
//     } finally {
//       setShowSpinner(false);
//     }
//   };

//   const rerunAnalysis = () => {
//     setStep(1);
//     setFileName('');
//     setFileData(null);
//     setHistoryAnswers({
//       ethnicBackground: '',
//       familyConditions: [],
//       familyCancerCount: '',
//       geneticTestingHistory: '',
//     });
//     setResults(null);
//     setError(null);
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
//       <Header />
//       <main className="container mx-auto px-6 py-12">
//         {/* Error display */}
//         {error && (
//           <div className="max-w-2xl mx-auto mb-6">
//             <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
//               <h3 className="text-red-800 font-semibold mb-2">Connection Error</h3>
//               <p className="text-red-600 mb-4">{error}</p>
//               <p className="text-sm text-red-500">Using demo results for display purposes.</p>
//             </div>
//           </div>
//         )}

//         {step === 1 && (
//           <FileUpload
//             fileName={fileName}
//             onFileChange={handleFileChange}
//             onNext={goToQuestionnaire}
//           />
//         )}
//         {step === 2 && (
//           <Questionnaire
//             answers={historyAnswers}
//             onChange={handleHistoryChange}
//             onBack={() => setStep(1)}
//             onSubmit={submitHistory}
//           />
//         )}
//         {step === 3 && !showSpinner && (
//           <Results
//             fileName={fileName}
//             history={historyAnswers}
//             results={results || hardcodedResults}
//             onRerun={rerunAnalysis}
//           />
//         )}
//       </main>
//       {showSpinner && <Spinner />}
//       <Footer />
//     </div>
//   );
// }

// export default App;


// / Main App Component
function App() {
  const [step, setStep] = useState(1);
  const [fileName, setFileName] = useState('');
  const [fileData, setFileData] = useState(null);
  const [historyAnswers, setHistoryAnswers] = useState({
    ethnicBackground: '',
    familyConditions: [],
    familyCancerCount: '',
    geneticTestingHistory: '',
  });
  const [showSpinner, setShowSpinner] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      setFileData(file);
      setError(null);
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

  const submitHistory = async () => {
    if (!fileData) {
      setError('No file uploaded');
      return;
    }

    setShowSpinner(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', fileData);
      formData.append('questionnaire', JSON.stringify(historyAnswers));
      formData.append('fileName', fileName);

      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        body: formData,
      });
      console.log('response :: ',response);
      const result = await response.json();
      console.log('result :: ',result);
      
      if (response.ok) {
        setResults(result);
        setStep(3);
      } else {
        throw new Error(result.message || 'Analysis failed');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError(`Connection issue: ${err.message}`);
      
      // Fallback to demo results
      const fallbackResults = {
        anomalyDetected: true,
        reconstructionError: 0.024,
        threshold: 0.01,
        shapValues: [
          { feature: 'TP53', value: 'Breast Cancer Risk' },
          { feature: 'BRCA1', value: 'Ovarian Cancer Risk' },
          { feature: 'CFTR', value: 'Cystic Fibrosis' },
          { feature: 'MLH1', value: 'Lynch Syndrome' },
          { feature: 'BRCA2', value: 'Pancreatic Cancer Risk' }
        ],
        ragSummaryData: {
          'Demo Note': 'This is a demonstration analysis as the server connection failed.',
          'TP53': 'TP53 mutations are associated with Li-Fraumeni syndrome and increased cancer risk.',
          'BRCA1': 'BRCA1 mutations significantly increase breast and ovarian cancer risk.',
          'Recommendation': 'For actual genetic analysis, ensure proper server connection and upload genomic data files.',
          'References': 'Demo data for testing purposes only.'
        }
      };
      
      setResults(fallbackResults);
      setStep(3);
    } finally {
      setShowSpinner(false);
    }
  };

  const rerunAnalysis = () => {
    setStep(1);
    setFileName('');
    setFileData(null);
    setHistoryAnswers({
      ethnicBackground: '',
      familyConditions: [],
      familyCancerCount: '',
      geneticTestingHistory: '',
    });
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header />
      <main className="container mx-auto px-6 py-12">
        {error && (
          <div className="max-w-2xl mx-auto mb-6">
            <div className="bg-orange-50 border border-orange-200 rounded-2xl p-6">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-6 h-6 text-orange-600 mt-0.5" />
                <div>
                  <h3 className="text-orange-800 font-semibold mb-2">Connection Notice</h3>
                  <p className="text-orange-700 mb-2">{error}</p>
                  <p className="text-sm text-orange-600">Demo results will be displayed for testing purposes.</p>
                </div>
              </div>
            </div>
          </div>
        )}

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
        {step === 3 && !showSpinner && results && (
          <Results
            fileName={fileName}
            results={results}
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