// // Spinner Component
// const Spinner = () => (
//   <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
//     <div className="bg-white rounded-2xl p-8 shadow-2xl text-center">
//       <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
//       <h3 className="text-xl font-semibold text-gray-800 mb-2">Analyzing Genome</h3>
//       <p className="text-gray-600">Processing genetic variants and generating insights...</p>
//     </div>
//   </div>
// );
// export default Spinner;

// Spinner Component
const Spinner = () => (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div className="bg-white rounded-2xl p-8 max-w-sm mx-4">
      <div className="flex flex-col items-center space-y-4">
        <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
        <h3 className="text-lg font-semibold text-gray-800">Analyzing Genomic Data</h3>
        <p className="text-gray-600 text-center">Processing your genetic information...</p>
      </div>
    </div>
  </div>
);
export default Spinner;