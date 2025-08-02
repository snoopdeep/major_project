import React, { useState } from 'react';
import { Upload, FileText, ChevronRight, CheckCircle, Activity, Atom, AlertTriangle, Brain, MessageSquare, Search, Zap } from 'lucide-react';

// Header Component
const Header = () => (
  <header className="relative bg-gradient-to-r from-blue-900 via-purple-900 to-indigo-900 text-white">
    <div className="absolute inset-0 bg-black/20"></div>
    <div className="relative container mx-auto px-6 py-8">
      <div className="flex items-center justify-center space-x-3 mb-2">
        <Atom className="w-8 h-8 text-cyan-400" />
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
          Genomic Anomaly Detection
        </h1>
      </div>
      <p className="text-center text-blue-200 text-lg">
        AI-Powered Genetic Analysis with Explainable Insights
      </p>
    </div>
  </header>
);

export default Header;