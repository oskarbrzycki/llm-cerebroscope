import os
import re
import time
import sys
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import print as rprint

# Internal Imports
from cerebro.ingester import Ingester, CerebroChunk
from cerebro.tracer import CerebroTracer
from cerebro.validator import CerebroValidator
from cerebro.vector_store import CerebroVectorStore
from cerebro.reporter import CerebroReporter

from cerebro.ui.formatter import CerebroFormatter 

# Initialize Rich Console
console = Console()

def get_ollama_models():
    """Robustly fetches available models from Ollama."""
    try:
        models_info = ollama.list()
        # Handle different library versions (Object vs Dict)
        if hasattr(models_info, 'models'):
            raw_models = models_info.models
        elif isinstance(models_info, dict) and 'models' in models_info:
            raw_models = models_info['models']
        else:
            raw_models = []

        clean_names = []
        for m in raw_models:
            if isinstance(m, dict):
                name = m.get('name') or m.get('model')
            else:
                name = getattr(m, 'model', getattr(m, 'name', None))
            if name: clean_names.append(name)
                
        return clean_names if clean_names else ["llama3"]
    except Exception:
        console.print("[bold red]❌ Error: Could not connect to Ollama. Make sure it's running![/bold red]")
        return ["llama3 (Offline)"]

def main():
    # --- 1. WELCOME SCREEN ---
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]🕵️  LLM-CEREBROSCOPE CLI[/bold cyan]\n"
        "[dim]Forensic Data Analysis & Logic Engine[/dim]",
        border_style="cyan"
    ))

    # --- 2. MODEL SELECTION ---
    available_models = get_ollama_models()
    
    rprint("\n[bold]🧠 Available AI Models:[/bold]")
    for idx, model in enumerate(available_models):
        rprint(f"  [cyan]{idx+1}.[/cyan] {model}")
    
    choice = Prompt.ask("Select Model ID", default="1")
    try:
        selected_model = available_models[int(choice)-1]
    except:
        selected_model = available_models[0]
        
    rprint(f"[green]✔ Active Brain:[/green] [bold]{selected_model}[/bold]\n")

    # --- 3. INITIALIZE COMPONENTS ---
    with console.status("[bold green]Initializing Core Systems...[/bold green]"):
        ingester = Ingester()
        tracer = CerebroTracer()
        validator = CerebroValidator()
        vector_db = CerebroVectorStore()
        formatter = CerebroFormatter()
        reporter = CerebroReporter()

    # --- 4. INGESTION PHASE ---
    raw_path = "data/raw"
    if not os.path.exists(raw_path):
        os.makedirs(raw_path)
        rprint(f"[yellow]⚠ Created empty directory: {raw_path}. Add files there![/yellow]")

    with console.status("[bold yellow]Scanning Evidence Locker...[/bold yellow]"):
        new_chunks = ingester.ingest_directory(raw_path)
        
    if new_chunks:
        console.print(f"[bold green]💾 Indexed {len(new_chunks)} new fragments into Vector DB.[/bold green]")
        vector_db.add_chunks(new_chunks)
    else:
        console.print("[dim]ℹ️  No new documents found. Using existing database.[/dim]")

    # --- 5. INTERACTIVE LOOP ---
    rprint("\n[bold]💬 System Ready. Type 'exit' to quit.[/bold]")
    
    while True:
        try:
            query = Prompt.ask("\n[bold cyan]Query[/bold cyan]")
        except (KeyboardInterrupt, EOFError):
            break
            
        if query.lower() in ['exit', 'quit']:
            rprint("[bold red]Shutting down systems...[/bold red]")
            break

        # A. RETRIEVAL
        with console.status(f"[bold]🧠 {selected_model} is thinking...[/bold]"):
            # Note: CLI searches ALL sources by default
            search_results = vector_db.search(query, n_results=5)
            
            retrieved_chunks = []
            if search_results['ids'] and search_results['ids'][0]:
                for i in range(len(search_results['ids'][0])):
                    meta = search_results['metadatas'][0][i]
                    chunk = CerebroChunk(
                        chunk_id=search_results['ids'][0][i],
                        text=search_results['documents'][0][i],
                        source=meta['source'],
                        page=meta['page'],
                        timestamp=meta.get('timestamp', time.time())
                    )
                    retrieved_chunks.append(chunk)
            else:
                rprint("[bold red]❌ No relevant evidence found.[/bold red]")
                continue

            # B. VALIDATION & TRACING (With Model Name!)
            conflicts = validator.check_for_conflicts(retrieved_chunks, model_name=selected_model)
            answer = tracer.analyze_query(query, retrieved_chunks, model_name=selected_model)

            # C. REPORT GENERATION
            report_path = reporter.save_report(query, answer, conflicts, retrieved_chunks)

        # D. VISUALIZATION
        formatter.display_investigation(query, answer)
        
        # Heatmap
        used_ids = re.findall(r"ID: ([a-f0-9]+)", answer)
        formatter.highlight_relevance(retrieved_chunks, used_ids, validator=validator)
        
        # Verdict
        formatter.display_recommendation(conflicts)

        rprint(f"\n[dim]📄 Report saved to: {report_path}[/dim]")

if __name__ == "__main__":
    main()