// // Questionnaire Component
// import { Upload, FileText,ChevronRight, CheckCircle,Activity,AlertTriangle  } from "lucide-react";
// const Questionnaire = ({ answers, onChange, onBack, onSubmit }) => (
//   <div className="max-w-2xl mx-auto">
//     <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
//       <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-8 border-b">
//         <div className="flex items-center space-x-3 mb-4">
//           <Activity className="w-8 h-8 text-purple-600" />
//           <h2 className="text-2xl font-bold text-gray-800">Medical History</h2>
//         </div>
//         <p className="text-gray-600">Provide your medical background for comprehensive analysis</p>
//       </div>
      
//       <div className="p-8 space-y-6">
//         {[
//           { key: 'hereditaryCardio', label: 'Hereditary cardiovascular risk?' },
//           { key: 'familyCancer', label: 'Family history of cancer?' },
//           { key: 'bmiOver30', label: 'BMI greater than 30?' },
//           { key: 'priorGeneTherapy', label: 'Previous gene therapy?' }
//         ].map((question) => (
//           <div key={question.key} className="space-y-2">
//             <label className="block text-sm font-medium text-gray-700">
//               {question.label}
//             </label>
//             <select
//               name={question.key}
//               value={answers[question.key]}
//               onChange={onChange}
//               className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
//             >
//               <option value="">Select an option</option>
//               <option value="yes">Yes</option>
//               <option value="no">No</option>
//             </select>
//           </div>
//         ))}
        
//         <div className="flex space-x-4 pt-6">
//           <button 
//             onClick={onBack}
//             className="flex-1 bg-gray-100 text-gray-700 font-semibold py-3 px-6 rounded-xl hover:bg-gray-200 transition-colors"
//           >
//             Back to Upload
//           </button>
//           <button 
//             onClick={onSubmit}
//             className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all"
//           >
//             Analyze Genome
//           </button>
//         </div>
//       </div>
//     </div>
//   </div>
// );

// export default Questionnaire;



import React from 'react';
import { Activity } from 'lucide-react';

const Questionnaire = ({ answers, onChange, onBack, onSubmit }) => {
  const handleMultiSelectChange = (questionKey, value) => {
    const currentValues = answers[questionKey] || [];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value];
    
    const event = {
      target: {
        name: questionKey,
        value: newValues
      }
    };
    onChange(event);
  };

  const isSelected = (questionKey, value) => {
    const currentValues = answers[questionKey] || [];
    return currentValues.includes(value);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-8 border-b">
          <div className="flex items-center space-x-3 mb-4">
            <Activity className="w-8 h-8 text-purple-600" />
            <h2 className="text-2xl font-bold text-gray-800">Comprehensive Medical History</h2>
          </div>
          <p className="text-gray-600">Provide detailed medical background for comprehensive genetic analysis</p>
        </div>
        
        <div className="p-8 space-y-8 max-h-96 overflow-y-auto">
          {/* Question 1: Ethnic Background */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              1. What is your ethnic background and ancestral origin?
            </label>
            <select
              name="ethnicBackground"
              value={answers.ethnicBackground || ''}
              onChange={onChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">Select your ethnic background</option>
              <option value="european">European/Caucasian</option>
              <option value="african">African/African American</option>
              <option value="eastAsian">Asian (East Asian)</option>
              <option value="southAsian">Asian (South Asian)</option>
              <option value="hispanic">Hispanic/Latino</option>
              <option value="nativeAmerican">Native American</option>
              <option value="middleEastern">Middle Eastern</option>
              <option value="mixed">Mixed ethnicity</option>
              <option value="other">Other</option>
            </select>
          </div>

          {/* Question 2: Family Medical Conditions */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              2. Please list any medical conditions that run in your family (check all that apply):
            </label>
            <div className="grid grid-cols-2 gap-3">
              {[
                'Heart disease', 'Cancer', 'Diabetes', 'Mental health disorders',
                'Neurological disorders', 'Blood disorders', 'Kidney disease',
                'Vision/hearing problems', 'Birth defects', 'Other'
              ].map((condition) => (
                <label key={condition} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isSelected('familyConditions', condition)}
                    onChange={() => handleMultiSelectChange('familyConditions', condition)}
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-700">{condition}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Question 3: Personal Diagnoses */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              3. Have you been diagnosed with any of the following conditions? (Select all that apply)
            </label>
            <div className="grid grid-cols-2 gap-3">
              {[
                'Intellectual disability or developmental delay', 'Autism spectrum disorder',
                'Seizures or epilepsy', 'Heart defects', 'Vision or hearing problems',
                'Growth disorders', 'Metabolic disorders', 'Cancer', 'None of the above', 'Other'
              ].map((condition) => (
                <label key={condition} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isSelected('personalDiagnoses', condition)}
                    onChange={() => handleMultiSelectChange('personalDiagnoses', condition)}
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-700">{condition}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Question 4: Age of First Diagnosis */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              4. At what age were you first diagnosed with a medical condition?
            </label>
            <select
              name="ageFirstDiagnosis"
              value={answers.ageFirstDiagnosis || ''}
              onChange={onChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">Select age range</option>
              <option value="birth-1">Birth to 1 year</option>
              <option value="1-5">1-5 years</option>
              <option value="6-12">6-12 years</option>
              <option value="13-18">13-18 years</option>
              <option value="19-30">19-30 years</option>
              <option value="over30">Over 30 years</option>
              <option value="never">Never diagnosed with any condition</option>
            </select>
          </div>

          {/* Question 5: Consanguinity */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              5. Are your parents related to each other?
            </label>
            <select
              name="parentsRelated"
              value={answers.parentsRelated || ''}
              onChange={onChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">Select an option</option>
              <option value="no">No, not related</option>
              <option value="cousins">Yes, they are cousins</option>
              <option value="closelyRelated">Yes, they are more closely related than cousins</option>
              <option value="dontKnow">I don't know</option>
              <option value="preferNotToAnswer">Prefer not to answer</option>
            </select>
          </div>

          {/* Question 6: Pregnancy Complications */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              6. Have you or your partner experienced any pregnancy complications? (Select all that apply)
            </label>
            <div className="grid grid-cols-2 gap-3">
              {[
                'Recurrent miscarriages (3 or more)', 'Stillbirth', 'Infertility issues',
                'Birth defects in children', 'Premature births', 'None of the above', 'Not applicable'
              ].map((complication) => (
                <label key={complication} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isSelected('pregnancyComplications', complication)}
                    onChange={() => handleMultiSelectChange('pregnancyComplications', complication)}
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-700">{complication}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Question 7: Physical Features */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              7. Do you have any unusual physical features or characteristics?
            </label>
            <div className="grid grid-cols-2 gap-3">
              {[
                'Unusually tall or short stature', 'Distinctive facial features',
                'Skin abnormalities', 'Hand/foot abnormalities',
                'Spine curvature problems', 'None of the above', 'Other'
              ].map((feature) => (
                <label key={feature} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isSelected('physicalFeatures', feature)}
                    onChange={() => handleMultiSelectChange('physicalFeatures', feature)}
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-700">{feature}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Question 8: Severe Reactions */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              8. Have you experienced any severe reactions to foods, medications, or environmental factors?
            </label>
            <div className="grid grid-cols-2 gap-3">
              {[
                'Yes, severe food reactions or intolerances', 'Yes, unusual medication reactions',
                'Yes, environmental sensitivities', 'Episodes of severe illness during fasting or stress',
                'Unusual body odors', 'None of the above'
              ].map((reaction) => (
                <label key={reaction} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isSelected('severeReactions', reaction)}
                    onChange={() => handleMultiSelectChange('severeReactions', reaction)}
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-700">{reaction}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Question 9: Family Cancer History */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              9. How many family members (including yourself) have been diagnosed with cancer?
            </label>
            <select
              name="familyCancerCount"
              value={answers.familyCancerCount || ''}
              onChange={onChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">Select number</option>
              <option value="none">None</option>
              <option value="1">1 person</option>
              <option value="2-3">2-3 people</option>
              <option value="4-5">4-5 people</option>
              <option value="more5">More than 5 people</option>
            </select>
          </div>

          {/* Question 10: Genetic Testing History */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              10. Have you ever had genetic testing or counseling?
            </label>
            <select
              name="geneticTestingHistory"
              value={answers.geneticTestingHistory || ''}
              onChange={onChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">Select an option</option>
              <option value="testingCompleted">Yes, genetic testing completed</option>
              <option value="counselingOnly">Yes, genetic counseling only</option>
              <option value="interestedToLearn">No, but interested in learning more</option>
              <option value="notInterested">No, not interested</option>
              <option value="dontKnow">I don't know what genetic testing involves</option>
            </select>
          </div>
        </div>

        <div className="flex space-x-4 p-8 pt-6 border-t bg-gray-50">
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
  );
};

export default Questionnaire;