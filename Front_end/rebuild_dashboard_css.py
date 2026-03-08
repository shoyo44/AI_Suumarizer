"""
Clean up Dashboard.css - remove null bytes, \x00 characters,
and the corrupted mangled media query block starting at the .main-container closing brace.
"""
import re

src = "src/components/Dashboard.css"

with open(src, "rb") as f:
    raw = f.read()

# Decode, ignoring null bytes
text = raw.decode("utf-8", errors="replace")

# Remove all null bytes
text = text.replace('\x00', '')

# Normalize line endings
text = text.replace('\r\r\r\n', '\n').replace('\r\r\n', '\n').replace('\r\n', '\n').replace('\r', '\n')

# Find the cut point: right after .main-container block closes (before the corrupt block)
# The good clean code is at the top. The corruption starts after .main-container { ... }
# We can find this by looking for the first occurrence of the garbage block character sequence
# After cleanup the markers are "}\n\n\n/* Responsive..."  or just "\n\\n\n/* Responsive"
# Let's cut at the first occurrence of literal backslash-n which indicates corruption
corrupt_start = text.find('\n\\n\n/* Responsive Adjustments */')
if corrupt_start == -1:
    corrupt_start = text.find('\n\\n/* Responsive Adjustments */')

print(f"Corrupt section starts at: {corrupt_start}")

if corrupt_start != -1:
    base = text[:corrupt_start].rstrip()
else:
    # Try to find .main-container closing brace boundary
    mc_end = text.find('.main-container {')
    if mc_end != -1:
        brace_end = text.find('}', mc_end)
        if brace_end != -1:
            base = text[:brace_end+1].rstrip()
            print(f"Falling back to main-container end at {brace_end}")
        else:
            base = text
    else:
        base = text

# Append the single clean responsive block for Dashboard
clean_responsive = """

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE — Mobile-first layout
   ═══════════════════════════════════════════════════════════════ */

@media (max-width: 768px) {
  .top-navbar {
    padding: 0 12px;
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

  .avatar {
    width: 26px;
    height: 26px;
    font-size: 0.7rem;
  }

  .nav-icon-btn,
  .menu-btn {
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

  .app-layout {
    height: auto;
    min-height: 100dvh;
  }

  .main-container {
    height: auto;
    overflow: visible;
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
"""

result = base + clean_responsive

# Remove runs of 3+ blank lines
result = re.sub(r'\n{3,}', '\n\n', result)

with open(src, "w", encoding="utf-8", newline="\n") as f:
    f.write(result)

lines = result.split('\n')
print(f"Done! Final Dashboard.css: {len(lines)} lines")
