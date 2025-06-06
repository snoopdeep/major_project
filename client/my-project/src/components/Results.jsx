// // Results Component
import { Upload, FileText,ChevronRight, CheckCircle,Activity,AlertTriangle , AlertCircle } from "lucide-react";
import ShapPanel from './ShapPanel'
import InteractiveRagPanel from './RagChatbotPanel'
// const Results = ({ fileName, history, results, onRerun }) => (
//   <div className="space-y-8">
//     {/* Status Banner */}
//     <div className={`p-6 rounded-2xl shadow-lg ${
//       results.anomalyDetected 
//         ? 'bg-gradient-to-r from-red-500 to-orange-500 text-white'
//         : 'bg-gradient-to-r from-green-500 to-emerald-500 text-white'
//     }`}>
//       <div className="flex items-center justify-center space-x-3">
//         {results.anomalyDetected ? (
//           <AlertTriangle className="w-8 h-8" />
//         ) : (
//           <CheckCircle className="w-8 h-8" />
//         )}
//         <div className="text-center">
//           <h2 className="text-2xl font-bold">
//             {results.anomalyDetected ? 'Genetic Anomalies Detected' : 'No Anomalies Detected'}
//           </h2>
//           {/* <p className="text-lg opacity-90 mt-1">
//             Reconstruction Error: {results.reconstructionError} (Threshold: {results.threshold})
//           </p> */}
//         </div>
//       </div>
//     </div>
    
//     {/* Analysis Panels */}
//     <div className="grid lg:grid-cols-2 gap-8">
//       <ShapPanel shapValues={results.shapValues} />
//       <InteractiveRagPanel ragData={results.ragSummaryData} />
//     </div>
    
//     <div className="text-center">
//       <button 
//         onClick={onRerun}
//         className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-8 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg"
//       >
//         Run New Analysis
//       </button>
//     </div>
//   </div>
// );
// export default Results;


// Results Component
const Results = ({ fileName, results, onRerun }) => (
  <div className="max-w-4xl mx-auto space-y-6">
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
      <div className="bg-gradient-to-r from-green-50 to-blue-50 p-8 border-b">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Analysis Results</h2>
        <p className="text-gray-600">Analysis completed for {fileName}</p>
      </div>
      
      <div className="p-8">
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Activity className="w-5 h-5 text-blue-600" />
              <span className="font-semibold text-gray-800">Anomaly Detection</span>
            </div>
            <p className={`text-lg font-bold ${results.anomalyDetected ? 'text-red-600' : 'text-green-600'}`}>
              {results.anomalyDetected ? 'Variants Found' : 'No Variants Found'}
            </p>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <AlertCircle className="w-5 h-5 text-orange-600" />
              <span className="font-semibold text-gray-800">Reconstruction Error</span>
            </div>
            <p className="text-lg font-bold text-gray-700">{results.reconstructionError}</p>
          </div>
        </div>
        
        {results.shapValues && results.shapValues.length > 0 && (
          <div className="mb-8">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Key Genetic Features</h3>
            <div className="grid gap-3">
              {results.shapValues.slice(0, 5).map((item, index) => (
                <div key={index} className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                  <span className="font-medium text-gray-800">{item.feature}</span>
                  <span className="text-blue-600 font-semibold">{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {results.ragSummaryData && (
          <div className="mb-8">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Detailed Analysis</h3>
            <div className="space-y-4">
              {Object.entries(results.ragSummaryData).map(([key, value]) => (
                <div key={key} className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold text-gray-800 mb-2">{key}</h4>
                  <p className="text-gray-600 text-sm">{value}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        
        <button
          onClick={onRerun}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all"
        >
          Run New Analysis
        </button>
      </div>
    </div>
  </div>
);

export default Results;