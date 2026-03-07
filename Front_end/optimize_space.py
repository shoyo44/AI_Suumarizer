import os

filepath = 'src/components/Analyzer.css'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace 480px block with aggressive vertical space optimizations
old_480_block = """@media (max-width: 480px) {
  .main-content {
    padding: 1rem;
    gap: 1rem;
  }
  .sidebar {
    padding: 1rem;
    max-height: 350px;
  }
  .sidebar-header h2 {
    font-size: 1.15rem;
  }
  .roles-header h3 {
    font-size: 0.9rem;
  }
  .role-card {
    padding: 10px 12px;
  }
  .role-icon {
    font-size: 1rem;
  }
  .role-card-header h4 {
    font-size: 0.85rem;
  }
  .role-card p {
    font-size: 0.75rem;
  }
  .output-actions {
    flex-direction: column;
    width: 100%;
  }
  .action-btn {
    width: 100%;
    justify-content: center;
  }
}"""

new_480_block = """@media (max-width: 480px) {
  .main-content {
    padding: 0.75rem;
    gap: 0.75rem; /* Tighter gap */
  }
  .sidebar {
    padding: 0.75rem;
    max-height: 220px; /* Reduced from 350px */
  }
  .sidebar-header {
    margin-bottom: 0.75rem;
  }
  .sidebar-header h2 {
    font-size: 1.1rem;
    margin-bottom: 0px;
  }
  .sidebar-header p {
    font-size: 0.75rem;
    line-height: 1.3;
  }
  .roles-header {
    padding: 8px 12px;
  }
  .roles-header h3 {
    font-size: 0.85rem;
  }
  .search-box {
    padding: 8px 12px;
  }
  .search-box input {
    padding: 8px 10px 8px 34px;
    font-size: 0.85rem;
  }
  .roles-list {
    height: 140px; /* Reduced to fit in the 220px max-height */
    padding: 6px 8px;
    gap: 6px;
  }
  .role-card {
    padding: 8px 10px; /* Tighter card padding */
  }
  .role-icon {
    font-size: 1rem;
  }
  .role-card-header {
    margin-bottom: 2px;
  }
  .role-card-header h4 {
    font-size: 0.8rem;
  }
  .role-card p {
    font-size: 0.7rem;
    line-height: 1.35;
  }
  .input-section, .output-section {
    padding: 14px; /* Tighter box padding */
  }
  .section-label {
    margin-bottom: 2px;
  }
  .section-label h3 {
    font-size: 1rem;
  }
  .using-role {
    font-size: 0.75rem;
    margin-bottom: 10px;
    padding-bottom: 8px;
  }
  textarea {
    min-height: 100px; /* Reduced from 180/140px */
    padding: 12px;
    padding-bottom: 30px;
    font-size: 0.85rem;
  }
  .char-count {
    bottom: 8px;
    right: 12px;
  }
  .upload-btn {
    bottom: 6px;
    left: 8px;
    width: 28px;
    height: 28px;
  }
  .textarea-wrapper {
    margin-bottom: 12px;
  }
  .generate-btn {
    padding: 10px;
    font-size: 0.9rem;
  }
  .output-header {
    margin-bottom: 12px;
    padding-bottom: 10px;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  .output-actions {
    flex-direction: row; /* Better to have a tight grid */
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
  .output-content {
    min-height: 100px;
    padding: 14px;
  }
  .result-text {
    font-size: 0.85rem;
    line-height: 1.6;
  }
}"""

content = content.replace(old_480_block, new_480_block)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated vertical spacing for maximum mobile real estate.")
