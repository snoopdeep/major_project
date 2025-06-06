#  ONLY TAKING QUERY FOR THE RETRIVAL



# import os
# import sys
# import time
# import pandas as pd
# import json
# from tqdm import tqdm
# from langchain.prompts import PromptTemplate
# from langchain.chains import RetrievalQA
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.llms import CTransformers
# from langchain.vectorstores import FAISS

# class GenomicRAGSystem:
#     def __init__(self, book_file_path="bookAAA.txt", index_name="book_index", 
#                  autoencoder_file="data/autoencoder_output.csv", 
#                  shap_file="data/shap_output.csv"):
#         self.book_file_path = book_file_path
#         self.index_name = index_name
#         self.autoencoder_file = autoencoder_file
#         self.shap_file = shap_file
#         self.qa_chain = None
#         self.autoencoder_data = None
#         self.shap_data = None
        
#     def load_autoencoder_data(self):
#         """Load autoencoder output data"""
#         try:
#             if os.path.exists(self.autoencoder_file):
#                 self.autoencoder_data = pd.read_csv(self.autoencoder_file)
#                 print(f"Loaded autoencoder data: {len(self.autoencoder_data)} records")
#             else:
#                 print(f"Warning: Autoencoder file not found: {self.autoencoder_file}")
#                 # Create sample data structure for demonstration
#                 self.autoencoder_data = pd.DataFrame({
#                     'tax_id_x': [9606], 'GeneID': [59342], 'Symbol': ['SCPEP1'],
#                     'chromosome_x': [17], 'type_of_gene': ['serine carboxypeptidase 1'],
#                     'description': ['17q22'], 'reconstruction_error': [0.25097194],
#                     'is_anomaly': [False]
#                 })
#         except Exception as e:
#             print(f"Error loading autoencoder data: {str(e)}")
#             self.autoencoder_data = None
    
#     def load_shap_data(self):
#         """Load SHAP explanation data"""
#         try:
#             if os.path.exists(self.shap_file):
#                 self.shap_data = pd.read_csv(self.shap_file)
#                 print(f"Loaded SHAP data: {len(self.shap_data)} records")
#             else:
#                 print(f"Warning: SHAP file not found: {self.shap_file}")
#                 # Create sample SHAP data structure
#                 self.shap_data = pd.DataFrame({
#                     'GeneID': [59342],
#                     'feature_importance': [0.85],
#                     'shap_values': ['reconstruction_error: 0.45, gene_length: 0.25, go_terms: 0.15'],
#                     'explanation': ['High reconstruction error indicates potential anomaly in gene expression patterns']
#                 })
#         except Exception as e:
#             print(f"Error loading SHAP data: {str(e)}")
#             self.shap_data = None

#     def load_text_file(self, file_path):
#         """Load and return documents from text file"""
#         try:
#             loader = TextLoader(file_path, encoding="utf-8")
#             documents = loader.load()
#             print(f"Loaded document: {file_path}")
#             return documents
#         except Exception as e:
#             print(f"Error loading text file: {str(e)}")
#             sys.exit(1)

#     def split_docs(self, documents, chunk_size=500, chunk_overlap=50):
#         """Split documents into chunks"""
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap
#         )
#         chunks = text_splitter.split_documents(documents)
#         print(f"Split into {len(chunks)} chunks")
#         return chunks

#     def create_embeddings(self, chunks):
#         """Create or load FAISS embeddings"""
#         index_path = f"{self.index_name}"
        
#         if os.path.exists(index_path):
#             print(f"Loading existing FAISS index from {index_path}...")
#             embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-large-en-v1.5')
#             try:
#                 docsearch = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
#                 return docsearch
#             except:
#                 print("Error loading existing index, creating new one...")
        
#         print("Creating new FAISS index...")
#         embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-large-en-v1.5')
#         docsearch = FAISS.from_documents(chunks, embeddings)
        
#         print(f"Saving FAISS index to {index_path}...")
#         docsearch.save_local(index_path)
        
#         return docsearch

#     def setup_qa_chain(self, docsearch):
#         """Setup the QA chain with enhanced prompt template"""
#         enhanced_prompt_template = """
#         You are a genomic data analysis expert. Use the following context and additional data to answer the question comprehensively.

#         Context from knowledge base: {context}

#         Additional Genomic Data:
#         {genomic_context}

#         Question: {question}

#         Instructions:
#         1. Analyze the genomic data provided alongside the knowledge base context
#         2. If anomalies are detected, explain their potential biological significance
#         3. Reference SHAP feature importance when explaining model predictions
#         4. Provide actionable insights for further research or clinical consideration
#         5. Be specific about gene functions, pathways, and potential disease associations

#         Answer:
#         """
        
#         PROMPT = PromptTemplate(
#             template=enhanced_prompt_template, 
#             input_variables=["context", "question", "genomic_context"]
#         )
        
#         llm = CTransformers(
#             model="llama-2-7b-chat.ggmlv3.q4_0.bin",
#             model_type="llama",
#             config={
#                 'max_new_tokens': 512,
#                 'context_length': 2048,  
#                 'temperature': 0.7
#             }
#         )

#         # Custom QA chain that handles our enhanced prompt
#         class EnhancedRetrievalQA:
#             def __init__(self, llm, retriever, prompt):
#                 self.llm = llm
#                 self.retriever = retriever
#                 self.prompt = prompt
            
#             def __call__(self, inputs):
#                 query = inputs["query"]
#                 genomic_context = inputs.get("genomic_context", "")
                
#                 # Retrieve relevant documents
#                 docs = self.retriever.get_relevant_documents(query)
#                 context = "\n\n".join([doc.page_content for doc in docs])
                
#                 # Format the prompt
#                 formatted_prompt = self.prompt.format(
#                     context=context,
#                     question=query,
#                     genomic_context=genomic_context
#                 )
                
#                 # Get LLM response
#                 result = self.llm(formatted_prompt)
                
#                 return {
#                     "result": result,
#                     "source_documents": docs
#                 }

#         qa = EnhancedRetrievalQA(
#             llm=llm,
#             retriever=docsearch.as_retriever(search_kwargs={'k': 3}),
#             prompt=PROMPT
#         )

#         return qa

#     def get_gene_context(self, gene_id_or_symbol=None):
#         """Get genomic context for a specific gene or general context"""
#         context_parts = []
        
#         # Autoencoder data context
#         if self.autoencoder_data is not None:
#             if gene_id_or_symbol:
#                 # Try to find specific gene
#                 gene_data = self.autoencoder_data[
#                     (self.autoencoder_data['GeneID'].astype(str) == str(gene_id_or_symbol)) |
#                     (self.autoencoder_data['Symbol'].astype(str).str.upper() == str(gene_id_or_symbol).upper())
#                 ]
#                 if not gene_data.empty:
#                     gene_info = gene_data.iloc[0]
#                     context_parts.append(f"""
# GENE INFORMATION:
# - Gene ID: {gene_info.get('GeneID', 'N/A')}
# - Symbol: {gene_info.get('Symbol', 'N/A')}
# - Chromosome: {gene_info.get('chromosome_x', 'N/A')}
# - Type: {gene_info.get('type_of_gene', 'N/A')}
# - Description: {gene_info.get('description', 'N/A')}
# - Reconstruction Error: {gene_info.get('reconstruction_error', 'N/A')}
# - Anomaly Status: {'ANOMALY DETECTED' if gene_info.get('is_anomaly', False) else 'NORMAL'}
#                     """)
#             else:
#                 # General statistics
#                 total_genes = len(self.autoencoder_data)
#                 anomalies = self.autoencoder_data['is_anomaly'].sum() if 'is_anomaly' in self.autoencoder_data.columns else 0
#                 context_parts.append(f"""
# DATASET OVERVIEW:
# - Total genes analyzed: {total_genes}
# - Anomalies detected: {anomalies}
# - Anomaly rate: {(anomalies/total_genes)*100:.2f}%
#                 """)
        
#         # SHAP data context
#         if self.shap_data is not None:
#             if gene_id_or_symbol:
#                 shap_info = self.shap_data[
#                     self.shap_data['GeneID'].astype(str) == str(gene_id_or_symbol)
#                 ]
#                 if not shap_info.empty:
#                     shap_data = shap_info.iloc[0]
#                     context_parts.append(f"""
# FEATURE IMPORTANCE ANALYSIS (SHAP):
# - Feature Importance Score: {shap_data.get('feature_importance', 'N/A')}
# - Key Contributing Features: {shap_data.get('shap_values', 'N/A')}
# - Explanation: {shap_data.get('explanation', 'N/A')}
#                     """)
#             else:
#                 context_parts.append("""
# FEATURE IMPORTANCE ANALYSIS:
# SHAP values available for detailed feature contribution analysis.
#                 """)
        
#         return "\n".join(context_parts) if context_parts else "No additional genomic context available."

#     def extract_gene_info_from_query(self, query):
#         """Extract potential gene ID or symbol from user query"""
#         # Simple extraction - can be enhanced with NLP
#         words = query.upper().split()
        
#         # Check if autoencoder data is available
#         if self.autoencoder_data is not None:
#             # Check for gene symbols
#             symbols = self.autoencoder_data['Symbol'].astype(str).str.upper().tolist()
#             for word in words:
#                 if word in symbols:
#                     return word
            
#             # Check for gene IDs
#             gene_ids = self.autoencoder_data['GeneID'].astype(str).tolist()
#             for word in words:
#                 if word in gene_ids:
#                     return word
        
#         return None

#     def initialize_system(self):
#         """Initialize the complete RAG system"""
#         print("Initializing Genomic RAG System...")
        
#         # Load genomic data
#         self.load_autoencoder_data()
#         self.load_shap_data()
        
#         # Check if book file exists
#         if not os.path.exists(self.book_file_path):
#             print(f"Error: Knowledge base file does not exist: {self.book_file_path}")
#             sys.exit(1)
        
#         # Handle index creation/loading
#         create_new_index = not os.path.exists(self.index_name)
        
#         if not create_new_index:
#             try:
#                 doc_mtime = os.path.getmtime(self.book_file_path)
#                 index_mtime = os.path.getmtime(self.index_name)
#                 if doc_mtime > index_mtime:
#                     print("Knowledge base has been modified. Recreating index...")
#                     create_new_index = True
#             except:
#                 create_new_index = True
        
#         if create_new_index:
#             documents = self.load_text_file(self.book_file_path)
#             chunks = self.split_docs(documents, chunk_size=300, chunk_overlap=30)
#             docsearch = self.create_embeddings(chunks)
#         else:
#             print("Loading existing embeddings...")
#             embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-large-en-v1.5')
#             docsearch = FAISS.load_local(self.index_name, embeddings, allow_dangerous_deserialization=True)
        
#         self.qa_chain = self.setup_qa_chain(docsearch)
#         print("System initialization complete!")

#     def run_interactive_session(self):
#         """Run the interactive chat session"""
#         print("\n===== Genomic Data Analysis RAG System =====")
#         print("Ask questions about genomic data, gene analysis, or general bioinformatics.")
#         print("Examples:")
#         print("- 'What is the significance of gene SCPEP1?'")
#         print("- 'Explain the anomaly detected in gene 59342'") 
#         print("- 'What are the implications of high reconstruction error?'")
#         print("Type 'exit' to quit.\n")

#         while True:
#             user_input = input("Your question: ")

#             if user_input.lower() == 'exit':
#                 print('Exiting Genomic RAG System. Goodbye!')
#                 break

#             if not user_input.strip():
#                 continue

#             try:
#                 start_time = time.time()
                
#                 # Extract gene information from query
#                 gene_info = self.extract_gene_info_from_query(user_input)
                
#                 # Get relevant genomic context
#                 genomic_context = self.get_gene_context(gene_info)
                
#                 # Query the system
#                 result = self.qa_chain({
#                     "query": user_input,
#                     "genomic_context": genomic_context
#                 })
                
#                 end_time = time.time()

#                 print(f"\nAnswer: {result['result']}")
#                 print(f"\nTime taken: {end_time - start_time:.2f} seconds")

#                 if result.get("source_documents") and len(result["source_documents"]) > 0:
#                     print("\nRelevant Knowledge Base Sources:")
#                     for i, doc in enumerate(result["source_documents"]):
#                         print(f"Source {i+1}: {doc.page_content[:150]}...")
                        
#             except Exception as e:
#                 if "context length" in str(e).lower():
#                     print("\nError: The question with context is too long for the model.")
#                     print("Try asking a more specific question or recreate your index with smaller chunks.")
#                 else:
#                     print(f"\nError: {str(e)}")

# def main():
#     # Initialize the system
#     rag_system = GenomicRAGSystem(
#         book_file_path="bookAAA.txt",
#         index_name="book_index",
#         autoencoder_file="data/autoencoder_output.csv",
#         shap_file="data/shap_output.csv"
#     )
    
#     # Initialize and run
#     rag_system.initialize_system()
#     rag_system.run_interactive_session()

# if __name__ == "__main__":
#     main()




import os
import sys
import time
import pandas as pd
import json
from tqdm import tqdm
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import CTransformers
from langchain.vectorstores import FAISS

class GenomicRAGSystem:
    def __init__(self, book_file_path="bookAAA.txt", index_name="book_index", 
                 autoencoder_file="data/autoencoder_output.csv", 
                 shap_file="data/shap_output.csv"):
        self.book_file_path = book_file_path
        self.index_name = index_name
        self.autoencoder_file = autoencoder_file
        self.shap_file = shap_file
        self.qa_chain = None
        self.autoencoder_data = None
        self.shap_data = None
        
    def load_autoencoder_data(self):
        """Load autoencoder output data"""
        try:
            if os.path.exists(self.autoencoder_file):
                self.autoencoder_data = pd.read_csv(self.autoencoder_file)
                print(f"Loaded autoencoder data: {len(self.autoencoder_data)} records")
            else:
                print(f"Warning: Autoencoder file not found: {self.autoencoder_file}")
                # Create sample data structure for demonstration
                self.autoencoder_data = pd.DataFrame({
                    'tax_id_x': [9606], 'GeneID': [59342], 'Symbol': ['SCPEP1'],
                    'chromosome_x': [17], 'type_of_gene': ['serine carboxypeptidase 1'],
                    'description': ['17q22'], 'reconstruction_error': [0.25097194],
                    'is_anomaly': [False]
                })
        except Exception as e:
            print(f"Error loading autoencoder data: {str(e)}")
            self.autoencoder_data = None
    
    def load_shap_data(self):
        """Load SHAP explanation data"""
        try:
            if os.path.exists(self.shap_file):
                self.shap_data = pd.read_csv(self.shap_file)
                print(f"Loaded SHAP data: {len(self.shap_data)} records")
            else:
                print(f"Warning: SHAP file not found: {self.shap_file}")
                # Create sample SHAP data structure
                self.shap_data = pd.DataFrame({
                    'GeneID': [59342],
                    'feature_importance': [0.85],
                    'shap_values': ['reconstruction_error: 0.45, gene_length: 0.25, go_terms: 0.15'],
                    'explanation': ['High reconstruction error indicates potential anomaly in gene expression patterns']
                })
        except Exception as e:
            print(f"Error loading SHAP data: {str(e)}")
            self.shap_data = None

    def load_text_file(self, file_path):
        """Load and return documents from text file"""
        try:
            loader = TextLoader(file_path, encoding="utf-8")
            documents = loader.load()
            print(f"Loaded document: {file_path}")
            return documents
        except Exception as e:
            print(f"Error loading text file: {str(e)}")
            sys.exit(1)

    def split_docs(self, documents, chunk_size=500, chunk_overlap=50):
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks

    def create_embeddings(self, chunks):
        """Create or load FAISS embeddings"""
        index_path = f"{self.index_name}"
        
        if os.path.exists(index_path):
            print(f"Loading existing FAISS index from {index_path}...")
            embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-large-en-v1.5')
            try:
                # Try with allow_dangerous_deserialization first (newer versions)
                docsearch = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
                return docsearch
            except TypeError:
                try:
                    # Fallback for older versions without the parameter
                    docsearch = FAISS.load_local(index_path, embeddings)
                    return docsearch
                except Exception as e:
                    print(f"Error loading existing index: {e}, creating new one...")
            except Exception as e:
                print(f"Error loading existing index: {e}, creating new one...")
        
        print("Creating new FAISS index...")
        embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-large-en-v1.5')
        docsearch = FAISS.from_documents(chunks, embeddings)
        
        print(f"Saving FAISS index to {index_path}...")
        docsearch.save_local(index_path)
        
        return docsearch

    def setup_qa_chain(self, docsearch):
        """Setup the QA chain with enhanced prompt template"""
        enhanced_prompt_template = """
        You are a genomic data analysis expert. Use the following context and additional data to answer the question comprehensively.

        Context from knowledge base: {context}

        Additional Genomic Data:
        {genomic_context}

        Question: {question}

        Instructions:
        1. Analyze the genomic data provided alongside the knowledge base context
        2. If anomalies are detected, explain their potential biological significance
        3. Reference SHAP feature importance when explaining model predictions
        4. Provide actionable insights for further research or clinical consideration
        5. Be specific about gene functions, pathways, and potential disease associations

        Answer:
        """
        
        PROMPT = PromptTemplate(
            template=enhanced_prompt_template, 
            input_variables=["context", "question", "genomic_context"]
        )
        
        llm = CTransformers(
            model="llama-2-7b-chat.ggmlv3.q4_0.bin",
            model_type="llama",
            config={
                'max_new_tokens': 512,
                'context_length': 2048,  
                'temperature': 0.7
            }
        )

        # Custom QA chain that handles our enhanced prompt with genomic data integration
        class EnhancedRetrievalQA:
            def __init__(self, llm, retriever, prompt, rag_system):
                self.llm = llm
                self.retriever = retriever
                self.prompt = prompt
                self.rag_system = rag_system
            
            def __call__(self, inputs):
                query = inputs["query"]
                genomic_context = inputs.get("genomic_context", "")
                gene_info = inputs.get("gene_info", None)
                
                # Create enhanced search queries using genomic data
                search_queries = self._create_enhanced_search_queries(query, gene_info)
                
                # Retrieve relevant documents using multiple queries
                all_docs = []
                for search_query in search_queries:
                    docs = self.retriever.get_relevant_documents(search_query)
                    all_docs.extend(docs)
                
                # Remove duplicates while preserving order
                unique_docs = []
                seen_content = set()
                for doc in all_docs:
                    if doc.page_content not in seen_content:
                        unique_docs.append(doc)
                        seen_content.add(doc.page_content)
                
                # Limit to top documents to avoid context overflow
                unique_docs = unique_docs[:5]
                
                context = "\n\n".join([doc.page_content for doc in unique_docs])
                
                # Format the prompt
                formatted_prompt = self.prompt.format(
                    context=context,
                    question=query,
                    genomic_context=genomic_context
                )
                
                # Get LLM response
                result = self.llm(formatted_prompt)
                
                return {
                    "result": result,
                    "source_documents": unique_docs
                }
            
            def _create_enhanced_search_queries(self, original_query, gene_info):
                """Create multiple search queries using genomic data"""
                queries = [original_query]  # Always include original query
                
                if gene_info and self.rag_system.autoencoder_data is not None:
                    # Get gene-specific data
                    gene_data = self.rag_system.autoencoder_data[
                        (self.rag_system.autoencoder_data['GeneID'].astype(str) == str(gene_info)) |
                        (self.rag_system.autoencoder_data['Symbol'].astype(str).str.upper() == str(gene_info).upper())
                    ]
                    
                    if not gene_data.empty:
                        gene_row = gene_data.iloc[0]
                        
                        # Add gene symbol based query
                        if 'Symbol' in gene_row:
                            queries.append(f"{gene_row['Symbol']} gene function")
                            queries.append(f"{gene_row['Symbol']} protein")
                        
                        # Add gene type/description based query
                        if 'type_of_gene' in gene_row and pd.notna(gene_row['type_of_gene']):
                            queries.append(f"{gene_row['type_of_gene']}")
                        
                        # Add chromosome location based query
                        if 'chromosome_x' in gene_row and pd.notna(gene_row['chromosome_x']):
                            queries.append(f"chromosome {gene_row['chromosome_x']} genes")
                        
                        # Add GO terms if available
                        if 'go_terms_list' in gene_row and pd.notna(gene_row['go_terms_list']):
                            go_terms = str(gene_row['go_terms_list']).split('|')[:3]  # First 3 GO terms
                            for go_term in go_terms:
                                if go_term.strip():
                                    queries.append(f"GO:{go_term}")
                        
                        # Add anomaly-related queries if gene is anomalous
                        if 'is_anomaly' in gene_row and gene_row['is_anomaly']:
                            queries.append("gene expression anomaly")
                            queries.append("abnormal gene regulation")
                            queries.append("gene mutation effects")
                        
                        # Add organism-specific query
                        if 'tax_id_x' in gene_row and pd.notna(gene_row['tax_id_x']):
                            if gene_row['tax_id_x'] == 9606:  # Human
                                queries.append("human genome")
                            queries.append(f"taxonomy {gene_row['tax_id_x']}")
                
                # Add SHAP-based queries
                if gene_info and self.rag_system.shap_data is not None:
                    shap_data = self.rag_system.shap_data[
                        self.rag_system.shap_data['GeneID'].astype(str) == str(gene_info)
                    ]
                    
                    if not shap_data.empty:
                        shap_row = shap_data.iloc[0]
                        
                        # Extract feature names from SHAP values
                        if 'shap_values' in shap_row and pd.notna(shap_row['shap_values']):
                            shap_features = str(shap_row['shap_values'])
                            # Extract feature names (assuming format: "feature1: value, feature2: value")
                            if 'reconstruction_error' in shap_features:
                                queries.append("gene expression reconstruction")
                            if 'gene_length' in shap_features:
                                queries.append("gene length significance")
                            if 'go_terms' in shap_features:
                                queries.append("gene ontology terms")
                
                # Remove duplicates and empty queries
                unique_queries = []
                for q in queries:
                    if q and q.strip() and q not in unique_queries:
                        unique_queries.append(q.strip())
                
                return unique_queries[:6]  # Limit to 6 queries to avoid overwhelming

        qa = EnhancedRetrievalQA(
            llm=llm,
            retriever=docsearch.as_retriever(search_kwargs={'k': 2}),  # Reduced k since we're doing multiple searches
            prompt=PROMPT,
            rag_system=self  # Pass self reference for data access
        )

        return qa

    def get_gene_context(self, gene_id_or_symbol=None):
        """Get genomic context for a specific gene or general context"""
        context_parts = []
        
        # Autoencoder data context
        if self.autoencoder_data is not None:
            if gene_id_or_symbol:
                # Try to find specific gene
                gene_data = self.autoencoder_data[
                    (self.autoencoder_data['GeneID'].astype(str) == str(gene_id_or_symbol)) |
                    (self.autoencoder_data['Symbol'].astype(str).str.upper() == str(gene_id_or_symbol).upper())
                ]
                if not gene_data.empty:
                    gene_info = gene_data.iloc[0]
                    context_parts.append(f"""
GENE INFORMATION:
- Gene ID: {gene_info.get('GeneID', 'N/A')}
- Symbol: {gene_info.get('Symbol', 'N/A')}
- Chromosome: {gene_info.get('chromosome_x', 'N/A')}
- Type: {gene_info.get('type_of_gene', 'N/A')}
- Description: {gene_info.get('description', 'N/A')}
- Reconstruction Error: {gene_info.get('reconstruction_error', 'N/A')}
- Anomaly Status: {'ANOMALY DETECTED' if gene_info.get('is_anomaly', False) else 'NORMAL'}
                    """)
            else:
                # General statistics
                total_genes = len(self.autoencoder_data)
                anomalies = self.autoencoder_data['is_anomaly'].sum() if 'is_anomaly' in self.autoencoder_data.columns else 0
                context_parts.append(f"""
DATASET OVERVIEW:
- Total genes analyzed: {total_genes}
- Anomalies detected: {anomalies}
- Anomaly rate: {(anomalies/total_genes)*100:.2f}%
                """)
        
        # SHAP data context
        if self.shap_data is not None:
            if gene_id_or_symbol:
                shap_info = self.shap_data[
                    self.shap_data['GeneID'].astype(str) == str(gene_id_or_symbol)
                ]
                if not shap_info.empty:
                    shap_data = shap_info.iloc[0]
                    context_parts.append(f"""
FEATURE IMPORTANCE ANALYSIS (SHAP):
- Feature Importance Score: {shap_data.get('feature_importance', 'N/A')}
- Key Contributing Features: {shap_data.get('shap_values', 'N/A')}
- Explanation: {shap_data.get('explanation', 'N/A')}
                    """)
            else:
                context_parts.append("""
FEATURE IMPORTANCE ANALYSIS:
SHAP values available for detailed feature contribution analysis.
                """)
        
        return "\n".join(context_parts) if context_parts else "No additional genomic context available."

    def extract_gene_info_from_query(self, query):
        """Extract potential gene ID or symbol from user query"""
        # Simple extraction - can be enhanced with NLP
        words = query.upper().split()
        
        # Check if autoencoder data is available
        if self.autoencoder_data is not None:
            # Check for gene symbols
            symbols = self.autoencoder_data['Symbol'].astype(str).str.upper().tolist()
            for word in words:
                if word in symbols:
                    return word
            
            # Check for gene IDs
            gene_ids = self.autoencoder_data['GeneID'].astype(str).tolist()
            for word in words:
                if word in gene_ids:
                    return word
        
        return None

    def initialize_system(self):
        """Initialize the complete RAG system"""
        print("Initializing Genomic RAG System...")
        
        # Load genomic data
        self.load_autoencoder_data()
        self.load_shap_data()
        
        # Check if book file exists
        if not os.path.exists(self.book_file_path):
            print(f"Error: Knowledge base file does not exist: {self.book_file_path}")
            sys.exit(1)
        
        # Handle index creation/loading
        create_new_index = not os.path.exists(self.index_name)
        
        if not create_new_index:
            try:
                doc_mtime = os.path.getmtime(self.book_file_path)
                index_mtime = os.path.getmtime(self.index_name)
                if doc_mtime > index_mtime:
                    print("Knowledge base has been modified. Recreating index...")
                    create_new_index = True
            except:
                create_new_index = True
        
        if create_new_index:
            documents = self.load_text_file(self.book_file_path)
            chunks = self.split_docs(documents, chunk_size=300, chunk_overlap=30)
            docsearch = self.create_embeddings(chunks)
        else:
            print("Loading existing embeddings...")
            embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-large-en-v1.5')
            try:
                # Try with allow_dangerous_deserialization first (newer versions)
                docsearch = FAISS.load_local(self.index_name, embeddings, allow_dangerous_deserialization=True)
            except TypeError:
                # Fallback for older versions without the parameter
                docsearch = FAISS.load_local(self.index_name, embeddings)
        
        self.qa_chain = self.setup_qa_chain(docsearch)
        print("System initialization complete!")

    def run_interactive_session(self):
        """Run the interactive chat session"""
        print("\n===== Genomic Data Analysis RAG System =====")
        print("Ask questions about genomic data, gene analysis, or general bioinformatics.")
        print("Examples:")
        print("- 'What is the significance of gene SCPEP1?'")
        print("- 'Explain the anomaly detected in gene 59342'") 
        print("- 'What are the implications of high reconstruction error?'")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("Your question: ")

            if user_input.lower() == 'exit':
                print('Exiting Genomic RAG System. Goodbye!')
                break

            if not user_input.strip():
                continue

            try:
                start_time = time.time()
                
                # Extract gene information from query
                gene_info = self.extract_gene_info_from_query(user_input)
                
                # Get relevant genomic context
                genomic_context = self.get_gene_context(gene_info)
                
                # Query the system with gene information
                result = self.qa_chain({
                    "query": user_input,
                    "genomic_context": genomic_context,
                    "gene_info": gene_info  # Pass gene info for enhanced search
                })
                
                end_time = time.time()

                print(f"\nAnswer: {result['result']}")
                print(f"\nTime taken: {end_time - start_time:.2f} seconds")

                if result.get("source_documents") and len(result["source_documents"]) > 0:
                    print("\nRelevant Knowledge Base Sources:")
                    for i, doc in enumerate(result["source_documents"]):
                        print(f"Source {i+1}: {doc.page_content[:150]}...")
                        
            except Exception as e:
                if "context length" in str(e).lower():
                    print("\nError: The question with context is too long for the model.")
                    print("Try asking a more specific question or recreate your index with smaller chunks.")
                else:
                    print(f"\nError: {str(e)}")

def main():
    # Initialize the system
    rag_system = GenomicRAGSystem(
        book_file_path="bookAAA.txt",
        index_name="book_index",
        autoencoder_file="data/autoencoder_output.csv",
        shap_file="data/shap_output.csv"
    )
    
    # Initialize and run
    rag_system.initialize_system()
    rag_system.run_interactive_session()

if __name__ == "__main__":
    main()