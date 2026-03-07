import os

files = [
    'src/components/Dashboard.css',
    'src/components/Analyzer.css',
    'src/components/History.css',
    'src/components/Login.css'
]

css_appends = {
    'src/components/Dashboard.css': """
/* Responsive Adjustments */
@media (max-width: 768px) {
  .top-navbar {
    padding: 0 16px;
    height: 56px;
  }
  .nav-logo-img {
    width: 28px;
    height: 28px;
  }
  .nav-left h1 {
    font-size: 1rem;
  }
  .user-name {
    display: none;
  }
  .modal-content {
    padding: 1.5rem;
  }
  .modal-header h2 {
    font-size: 1.15rem;
  }
}

@media (max-width: 480px) {
  .nav-left h1 {
    display: none;
  }
  .user-profile {
    padding: 2px;
    border: none;
    background: transparent;
  }
  .avatar {
    width: 32px;
    height: 32px;
  }
  .modal-overlay {
    padding: 1rem;
  }
  .usecase-card {
    padding: 10px;
  }
}
""",
    'src/components/Analyzer.css': """
/* Responsive Adjustments */
@media (max-width: 1024px) {
  .analyzer-container {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
    max-height: 400px;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
  .roles-list {
    height: 180px;
  }
  .main-content {
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .input-section, .output-section {
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
    min-height: 140px;
    font-size: 0.9rem;
  }
  .generate-btn {
    padding: 12px;
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
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
}
""",
    'src/components/History.css': """
/* Responsive Adjustments */
@media (max-width: 1024px) {
  .history-grid {
    grid-template-columns: 1fr;
  }
  .history-list {
    position: static;
    max-height: 400px;
  }
}

@media (max-width: 768px) {
  .history {
    padding: 1.5rem;
  }
  .history-empty {
    min-height: 400px;
    padding: 2rem;
  }
  .detail-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }
}

@media (max-width: 480px) {
  .history {
    padding: 1rem;
  }
  .history-empty h3 {
    font-size: 1.25rem;
  }
  .history-empty p {
    font-size: 0.85rem;
  }
  .history-list {
    max-height: 350px;
  }
  .list-header {
    padding: 1rem;
  }
  .history-item {
    padding: 1rem;
  }
  .item-usecase {
    font-size: 0.75rem;
  }
  .item-preview {
    font-size: 0.75rem;
  }
  .history-detail {
    padding: 1.25rem;
    min-height: auto;
  }
  .detail-header h3 {
    font-size: 1.1rem;
  }
  .detail-content {
    padding: 1rem;
    font-size: 0.85rem;
  }
  .reuse-btn, .copy-btn {
    flex: 1;
    justify-content: center;
  }
}
""",
    'src/components/Login.css': """
/* Responsive Adjustments */
@media (max-width: 480px) {
  .login-container {
    padding: 1rem;
  }
  .login-card {
    padding: 2rem;
  }
  .login-header h1 {
    font-size: 1.5rem;
  }
  .logo-icon {
    width: 64px;
    height: 64px;
    font-size: 1.75rem;
  }
  .google-btn {
    padding: 1rem;
    font-size: 0.95rem;
  }
}
"""
}

for filepath in files:
    try:
        # Read the file as bytes to avoid decoding errors
        with open(filepath, 'rb') as f:
            content = f.read()

        # The corruption happens exactly after the final } or sometimes before.
        # But looking at the bug, it happened after `echo ... >>`, meaning it's 
        # at the end of the file. So finding the last } in the uncorrupted file
        # is a safe bounding box.
        
        # We find the corrupted prefix: it starts with `\\ n / *`
        corrupted_idx = content.find(b'\\ n / *')
        if corrupted_idx != -1:
            clean_content = content[:corrupted_idx].decode('utf-8', errors='ignore')
            # Look for the last '}' before the corruption
            last_brace = clean_content.rfind('}')
            if last_brace != -1:
                clean_content = clean_content[:last_brace + 1]
        else:
            # If couldn't find, just cut at last '}' as fallback
            clean_content = content[:content.rfind(b'}') + 1].decode('utf-8', errors='ignore')
            
        # Append proper text
        clean_content += '\n' + css_appends[filepath]
        
        # Rewrite cleanly
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        print(f"Fixed {filepath}")
    except Exception as e:
        print(f"Error {filepath}: {e}")
