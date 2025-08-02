// // FileUpload Component
// import { Upload, FileText,ChevronRight, CheckCircle,Activity  } from "lucide-react";
// const FileUpload = ({ fileName, onFileChange, onNext }) => (
//   <div className="max-w-2xl mx-auto">
//     <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
//       <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-8 border-b">
//         <div className="flex items-center space-x-3 mb-4">
//           <Upload className="w-8 h-8 text-blue-600" />
//           <h2 className="text-2xl font-bold text-gray-800">Upload Genomic Data</h2>
//         </div>
//         <p className="text-gray-600">Upload your FASTA or VCF or CSV file to begin genetic analysis</p>
//       </div>
      
//       <div className="p-8">
//         <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 transition-colors">
//           <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
//           <input 
//             type="file"
//             accept=".fa,.fasta,.vcf,.csv"
//             onChange={onFileChange}
//             className="hidden"
//             id="file-upload"
//           />
//           <label htmlFor="file-upload" className="cursor-pointer">
//             <span className="text-lg font-medium text-gray-700 hover:text-blue-600">
//               Click to upload genomic file
//             </span>
//             <p className="text-sm text-gray-500 mt-2">FASTA, VCF files supported</p>
//           </label>
//         </div>
        
//         {fileName && (
//           <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-200">
//             <div className="flex items-center space-x-2">
//               <CheckCircle className="w-5 h-5 text-green-600" />
//               <span className="font-medium text-green-800">File uploaded: {fileName}</span>
//             </div>
//           </div>
//         )}
        
//         <button
//           onClick={onNext}
//           className="w-full mt-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all flex items-center justify-center space-x-2"
//         >
//           <span>Continue to Medical History</span>
//           <ChevronRight className="w-5 h-5" />
//         </button>
//       </div>
//     </div>
//   </div>
// );

// export default FileUpload;

import { useState } from 'react';
import { Upload, FileText, ChevronRight, CheckCircle, Activity, AlertCircle, Info } from "lucide-react";

// FileUpload Component
const FileUpload = ({ fileName, onFileChange, onNext }) => (
  <div className="max-w-2xl mx-auto">
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-8 border-b">
        <div className="flex items-center space-x-3 mb-4">
          <Upload className="w-8 h-8 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-800">Upload Genomic Data</h2>
        </div>
        <p className="text-gray-600">Upload your FASTA, VCF, or CSV file to begin genetic analysis</p>
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-start space-x-2">
            <Info className="w-5 h-5 text-blue-600 mt-0.5" />
            <div className="text-sm text-blue-700">
              <p className="font-medium mb-1">Supported file formats:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>VCF files with CHROM, POS, REF, ALT columns</li>
                <li>FASTA files for sequence analysis</li>
                <li>CSV files (demo analysis will be provided for non-genomic data)</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div className="p-8">
        <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 transition-colors">
          <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <input 
            type="file"
            accept=".fa,.fasta,.vcf,.csv"
            onChange={onFileChange}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <span className="text-lg font-medium text-gray-700 hover:text-blue-600">
              Click to upload genomic file
            </span>
            <p className="text-sm text-gray-500 mt-2">FASTA, VCF, CSV files supported</p>
          </label>
        </div>
        
        {fileName && (
          <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-200">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <span className="font-medium text-green-800">File uploaded: {fileName}</span>
            </div>
          </div>
        )}
        
        <button
          onClick={onNext}
          className="w-full mt-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all flex items-center justify-center space-x-2"
        >
          <span>Continue to Medical History</span>
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
);

export default FileUpload;