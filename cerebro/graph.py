import spacy
from streamlit_agraph import agraph, Node, Edge, Config

class CerebroGraph:
    def __init__(self):
        # Load the small English model for Entity Recognition
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # Fallback if not downloaded
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def visualize_connections(self, chunks):
        """
        Creates a Knowledge Graph from retrieved chunks.
        Nodes = Documents (Source) & Entities (People, Orgs, Products)
        Edges = Connection between Document and Entity
        """
        nodes = []
        edges = []
        node_ids = set()

        for chunk in chunks:
            # 1. Create a Node for the Document/Source
            # Shorten filename for display
            source_label = chunk.source.split('/')[-1]
            
            if source_label not in node_ids:
                nodes.append(Node(
                    id=source_label, 
                    label=source_label, 
                    size=25, 
                    shape="circularImage",
                    image="https://img.icons8.com/dusk/64/file.png", 
                    color="#FFD700" 
                ))
                node_ids.add(source_label)

            # 2. Extract Entities from the text (NLP)
            doc = self.nlp(chunk.text)
            
            # Filter distinct entities to avoid clutter
            seen_entities = set()
            
            for ent in doc.ents:
                # Filter interesting entities: ORG (Companies), PERSON, GPE (Locations), PRODUCT, DATE, MONEY
                if ent.label_ in ["ORG", "PERSON", "PRODUCT", "GPE", "MONEY", "DATE"] and ent.text.lower() not in seen_entities:
                    
                    clean_ent = ent.text.strip()
                    if len(clean_ent) < 2: continue # Skip noise
                    
                    seen_entities.add(clean_ent.lower())

                    # Add Entity Node if not exists
                    if clean_ent not in node_ids:
                        # Choose icon based on type
                        icon = "https://img.icons8.com/fluency/48/connection.png"
                        if ent.label_ == "PERSON": icon = "https://img.icons8.com/fluency/48/person-male.png"
                        elif ent.label_ == "ORG": icon = "https://img.icons8.com/fluency/48/company.png"
                        elif ent.label_ == "MONEY": icon = "https://img.icons8.com/fluency/48/us-dollar-circled.png"

                        nodes.append(Node(
                            id=clean_ent,
                            label=clean_ent,
                            size=15,
                            shape="circularImage",
                            image=icon,
                            color="#00FF00" # Neon Green
                        ))
                        node_ids.add(clean_ent)

                    # 3. Create Edge (Link) from Document to Entity
                    # ID combination ensures uniqueness
                    edge_id = f"{source_label}-{clean_ent}"
                    edges.append(Edge(
                        source=source_label,
                        target=clean_ent,
                        label=ent.label_, # e.g. "MONEY"
                        color="#555555"
                    ))

        # 4. Configuration for the Physics Engine
        config = Config(
            width="100%",
            height=500,
            directed=False, 
            physics=True, 
            hierarchical=False,
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=False
        )

        return nodes, edges, config