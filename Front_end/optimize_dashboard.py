import os

filepath = 'src/components/Dashboard.css'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the 768px dashboard query to tighten the nav
old_768_block = """@media (max-width: 768px) {
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
}"""

new_768_block = """@media (max-width: 768px) {
  .top-navbar {
    padding: 0 12px;
    height: 50px; /* Reduced from 56px/64px */
  }
  .nav-logo-img {
    width: 24px;
    height: 24px;
  }
  .nav-left h1 {
    font-size: 0.95rem;
  }
  .user-name {
    display: none;
  }
  .avatar {
    width: 26px;
    height: 26px;
    font-size: 0.7rem;
  }
  .nav-icon-btn, .menu-btn {
    width: 32px;
    height: 32px;
    padding: 4px;
  }
  .modal-content {
    padding: 1.25rem;
  }
  .modal-header {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
  }
  .modal-header h2 {
    font-size: 1.1rem;
  }
}"""

content = content.replace(old_768_block, new_768_block)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated dashboard vertical spacing.")
