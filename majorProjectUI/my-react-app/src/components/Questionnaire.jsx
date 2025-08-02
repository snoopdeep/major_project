// Questionnaire Component
import { Upload, FileText,ChevronRight, CheckCircle,Activity,AlertTriangle  } from "lucide-react";
const Questionnaire = ({ answers, onChange, onBack, onSubmit }) => (
  <div className="max-w-2xl mx-auto">
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-8 border-b">
        <div className="flex items-center space-x-3 mb-4">
          <Activity className="w-8 h-8 text-purple-600" />
          <h2 className="text-2xl font-bold text-gray-800">Medical History</h2>
        </div>
        <p className="text-gray-600">Provide your medical background for comprehensive analysis</p>
      </div>
      
      <div className="p-8 space-y-6">
        {[
          { key: 'hereditaryCardio', label: 'Hereditary cardiovascular risk?' },
          { key: 'familyCancer', label: 'Family history of cancer?' },
          { key: 'bmiOver30', label: 'BMI greater than 30?' },
          { key: 'priorGeneTherapy', label: 'Previous gene therapy?' }
        ].map((question) => (
          <div key={question.key} className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {question.label}
            </label>
            <select
              name={question.key}
              value={answers[question.key]}
              onChange={onChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">Select an option</option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
        ))}
        
        <div className="flex space-x-4 pt-6">
          <button 
            onClick={onBack}
            className="flex-1 bg-gray-100 text-gray-700 font-semibold py-3 px-6 rounded-xl hover:bg-gray-200 transition-colors"
          >
            Back to Upload
          </button>
          <button 
            onClick={onSubmit}
            className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all"
          >
            Analyze Genome
          </button>
        </div>
      </div>
    </div>
  </div>
);

export default Questionnaire;