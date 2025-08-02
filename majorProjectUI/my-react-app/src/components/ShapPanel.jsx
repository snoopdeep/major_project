// ShapPanel Component
import { Upload, FileText,ChevronRight, CheckCircle,Activity,AlertTriangle , } from "lucide-react";
const ShapPanel = ({ shapValues }) => (
  <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
    <div className="bg-gradient-to-r from-red-50 to-orange-50 p-6 border-b">
      <div className="flex items-center space-x-3">
        <Activity className="w-6 h-6 text-red-600" />
        <h3 className="text-xl font-bold text-gray-800">Feature Importance Analysis</h3>
      </div>
      <p className="text-gray-600 mt-1">SHAP values for top genetic variants</p>
    </div>
    
    <div className="p-6">
      <div className="space-y-3">
        {shapValues.map((item, idx) => (
          <div key={idx} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
            <div className="flex-shrink-0 w-8 h-8 bg-red-100 text-red-600 rounded-full flex items-center justify-center font-bold text-sm">
              {idx + 1}
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-900">{item.feature}</div>
              <div className="text-sm text-gray-600 truncate">{item.value}</div>
            </div>
            <div className="flex-shrink-0">
              <div className="w-20 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-red-500 to-orange-500 h-2 rounded-full"
                  style={{ width: `${Math.max(20, 100 - idx * 8)}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);

export default ShapPanel;