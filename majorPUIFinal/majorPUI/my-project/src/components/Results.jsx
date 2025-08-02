// Results Component
import { Upload, FileText,ChevronRight, CheckCircle,Activity,AlertTriangle , } from "lucide-react";
import ShapPanel from './ShapPanel'
import InteractiveRagPanel from './RagChatbotPanel'
const Results = ({ fileName, history, results, onRerun }) => (
  <div className="space-y-8">
    {/* Status Banner */}
    <div className={`p-6 rounded-2xl shadow-lg ${
      results.anomalyDetected 
        ? 'bg-gradient-to-r from-red-500 to-orange-500 text-white'
        : 'bg-gradient-to-r from-green-500 to-emerald-500 text-white'
    }`}>
      <div className="flex items-center justify-center space-x-3">
        {results.anomalyDetected ? (
          <AlertTriangle className="w-8 h-8" />
        ) : (
          <CheckCircle className="w-8 h-8" />
        )}
        <div className="text-center">
          <h2 className="text-2xl font-bold">
            {results.anomalyDetected ? 'Genetic Anomalies Detected' : 'No Anomalies Detected'}
          </h2>
          {/* <p className="text-lg opacity-90 mt-1">
            Reconstruction Error: {results.reconstructionError} (Threshold: {results.threshold})
          </p> */}
        </div>
      </div>
    </div>
    
    {/* Analysis Panels */}
    <div className="grid lg:grid-cols-2 gap-8">
      <ShapPanel shapValues={results.shapValues} />
      <InteractiveRagPanel ragData={results.ragSummaryData} />
    </div>
    
    <div className="text-center">
      <button 
        onClick={onRerun}
        className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-8 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg"
      >
        Run New Analysis
      </button>
    </div>
  </div>
);
export default Results;