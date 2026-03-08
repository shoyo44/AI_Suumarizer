"""
Final cleanup of Analyzer.css.
Keeps all content from the start up to (but not including) everything 
from the FIRST occurrence of '\\n' followed by a responsive comment,
then appends the single clean responsive block.
"""

src = "src/components/Analyzer.css"

with open(src, "r", encoding="utf-8") as f:
    content = f.read()

# The clean base (everything before the first responsive block contamination)
# Find the boundary: line 1064 ends with '.checkbox-desc { ... }' block
# We'll look for the first occurrence of "\\n" which marks the corrupt start
cutoff = content.find('\\n\n/* Responsive Adjustments */')
if cutoff == -1:
    cutoff = content.find('\\n/* Responsive Adjustments */')

if cutoff != -1:
    base = content[:cutoff].rstrip()
else:
    print("Could not find cutoff, using whole file")
    base = content

# Append the one single clean responsive block
clean_responsive = """

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE — Mobile-first layout
   ═══════════════════════════════════════════════════════════════ */

@media (max-width: 1024px) {
  .analyzer-container {
    flex-direction: column;
    height: auto;
    overflow: visible;
  }

  .sidebar {
    width: 100%;
    max-height: none;
    height: auto;
    overflow: visible;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }

  .roles-list {
    height: auto;
    max-height: 250px;
    overflow-y: auto;
  }

  .main-content {
    padding: 1.5rem;
    overflow: visible;
  }
}

@media (max-width: 768px) {
  .input-section,
  .output-section {
    padding: 16px;
  }

  .section-label h3 {
    font-size: 1.05rem;
  }

  .using-role {
    font-size: 0.8rem;
    margin-bottom: 12px;
    padding-bottom: 10px;
  }

  textarea {
    min-height: 120px;
    font-size: 0.9rem;
  }

  .generate-btn {
    padding: 12px;
    font-size: 0.95rem;
  }

  .output-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 12px;
    padding-bottom: 10px;
  }

  .output-actions {
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
  }

  .action-btn {
    flex: 1;
    min-width: 45%;
    justify-content: center;
    padding: 6px 10px;
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .sidebar {
    padding: 0.75rem;
    max-height: none;
    overflow: visible;
  }

  .roles-list {
    max-height: 250px;
    overflow-y: auto;
  }

  .main-content {
    padding: 0.75rem;
    gap: 0.75rem;
    overflow: visible;
  }

  .sidebar-header h2 {
    font-size: 1.1rem;
  }

  .roles-header h3 {
    font-size: 0.9rem;
  }

  .role-card {
    padding: 10px 12px;
  }

  .role-card-header h4 {
    font-size: 0.85rem;
  }

  .role-card p {
    font-size: 0.75rem;
  }

  .input-section,
  .output-section {
    padding: 14px;
  }

  textarea {
    min-height: 100px;
  }

  .output-actions {
    flex-direction: column;
    width: 100%;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }
}
"""

result = base + clean_responsive

with open(src, "w", encoding="utf-8", newline="\n") as f:
    f.write(result)

lines = result.split('\n')
print(f"Done! Final file: {len(lines)} lines")
print(f"Cutoff was at char {cutoff}")
