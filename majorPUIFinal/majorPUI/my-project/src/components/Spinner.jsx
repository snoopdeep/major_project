// Spinner Component
const Spinner = () => (
  <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
    <div className="bg-white rounded-2xl p-8 shadow-2xl text-center">
      <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
      <h3 className="text-xl font-semibold text-gray-800 mb-2">Analyzing Genome</h3>
      <p className="text-gray-600">Processing genetic variants and generating insights...</p>
    </div>
  </div>
);
export default Spinner;