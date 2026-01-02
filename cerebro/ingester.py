import uuid
import os
import time
import pandas as pd
from typing import List
from pypdf import PdfReader

class CerebroChunk:
    def __init__(self, text, source, page, timestamp=None, chunk_id=None):
        self.chunk_id = chunk_id if chunk_id else str(uuid.uuid4())[:8]
        self.text = text
        self.source = source
        self.page = page
        
        self.timestamp = timestamp if timestamp else time.time()

    def to_context_format(self) -> str:
        """Formats the chunk for the LLM prompt, including the date."""
        date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp))
        return f"[ID: {self.chunk_id} | SOURCE: {self.source} | DATE: {date_str}]\nCONTENT: {self.text}"

class Ingester:
    def __init__(self, chunk_size=800, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def ingest_directory(self, directory_path: str) -> List[CerebroChunk]:
        """Scans a directory and converts files into chunks."""
        all_chunks = []
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            return []

        print(f"📂 Scanning directory: {directory_path} ...")
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # Skip directories
            if not os.path.isfile(file_path):
                continue

            # Get file modification timestamp from OS
            file_timestamp = os.path.getmtime(file_path)

            try:
                if filename.endswith(".pdf"):
                    all_chunks.extend(self._process_pdf(file_path, filename, file_timestamp))
                elif filename.endswith(".txt"):
                    all_chunks.extend(self._process_txt(file_path, filename, file_timestamp))
                elif filename.endswith(".csv"):
                    all_chunks.extend(self._process_csv(file_path, filename, file_timestamp))
                elif filename.endswith(".xlsx") or filename.endswith(".xls"):
                    all_chunks.extend(self._process_excel(file_path, filename, file_timestamp))
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

        return all_chunks

    def _process_pdf(self, path, name, timestamp):
        chunks = []
        try:
            reader = PdfReader(path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    chunks.extend(self._split_into_chunks(text, name, i + 1, timestamp))
        except Exception as e:
            print(f"⚠️ PDF Error ({name}): {e}")
        return chunks

    def _process_txt(self, path, name, timestamp):
        with open(path, 'r', encoding='utf-8') as f:
            return self._split_into_chunks(f.read(), name, 1, timestamp)

    def _process_csv(self, path, name, timestamp):
        chunks = []
        try:
            df = pd.read_csv(path)
            for i, row in df.iterrows():
                # Convert row to a descriptive string
                row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
                chunks.append(CerebroChunk(row_text, name, i + 1, timestamp))
        except Exception as e:
            print(f"⚠️ CSV Error ({name}): {e}")
        return chunks

    def _process_excel(self, path, name, timestamp):
        chunks = []
        try:
            df_dict = pd.read_excel(path, sheet_name=None)
            for sheet_name, df in df_dict.items():
                for i, row in df.iterrows():
                    row_text = f"Sheet: {sheet_name} | " + " | ".join([f"{col}: {val}" for col, val in row.items()])
                    chunks.append(CerebroChunk(row_text, name, i + 1, timestamp))
        except Exception as e:
            print(f"⚠️ Excel Error ({name}): {e}")
        return chunks

    def _split_into_chunks(self, text, source, page_num, timestamp):
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(CerebroChunk(chunk_text, source, page_num, timestamp))
            start += (self.chunk_size - self.chunk_overlap)
        return chunks