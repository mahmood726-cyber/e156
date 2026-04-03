"""Scan C: drive for projects not yet in the E156 workbook."""
import os, re

# Known paths in workbook (lowercased, forward slashes)
with open('C:/E156/rewrite-workbook.txt', 'r', encoding='utf-8') as f:
    text = f.read()

known = set()
for m in re.finditer(r'PATH:\s*(.+)', text):
    p = m.group(1).strip().rstrip('/\\')
    known.add(p.lower().replace('\\', '/'))

new_projects = []

def scan_dir(base):
    if not os.path.isdir(base):
        return
    for name in sorted(os.listdir(base)):
        full = os.path.join(base, name).replace('\\', '/')
        if not os.path.isdir(full):
            continue
        if name.startswith('.') or name.startswith('_'):
            continue
        norm = full.lower()
        if norm in known:
            continue

        # Check substance
        file_count = 0
        has_html = False
        has_test = False
        has_manuscript = False
        has_dashboard = False
        has_protocol = False
        try:
            for root, dirs, files in os.walk(full):
                root = root.replace('\\', '/')
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env']]
                for f in files:
                    fp = os.path.join(root, f)
                    if f.endswith(('.py', '.R', '.r', '.html', '.js', '.ts')):
                        file_count += 1
                    if f.endswith('.html'):
                        try:
                            sz = os.path.getsize(fp)
                            if sz > 5000:
                                has_html = True
                            if sz > 50000:
                                has_dashboard = True
                        except:
                            pass
                    if 'test' in f.lower() or 'spec' in f.lower():
                        has_test = True
                    if any(w in f.lower() for w in ['manuscript', 'paper', 'draft', 'abstract']):
                        has_manuscript = True
                    if 'protocol' in f.lower() or 'e156' in f.lower():
                        has_protocol = True
                if file_count > 50:
                    break
        except PermissionError:
            pass

        substance = 'SUBSTANTIAL' if file_count >= 3 else 'THIN'
        tags = []
        if has_dashboard: tags.append('DASHBOARD')
        elif has_html: tags.append('HTML')
        if has_test: tags.append('TESTS')
        if has_manuscript: tags.append('MS')
        if has_protocol: tags.append('E156')
        tag_str = ' [' + ','.join(tags) + ']' if tags else ''

        new_projects.append((full, file_count, substance, tag_str, name))

# Scan all locations
scan_dir('C:/Models')
scan_dir('C:/Projects')
scan_dir('C:/HTML apps')

# Root level candidates
for name in os.listdir('C:/'):
    full = 'C:/' + name
    if not os.path.isdir(full):
        continue
    if name.lower() in ['windows', 'program files', 'program files (x86)', 'users',
                         'perflogs', '$recycle.bin', 'system volume information',
                         'recovery', 'msys64', 'intel', 'amd', 'drivers',
                         'models', 'projects', 'html apps', 'e156', 'c', 'data',
                         'projectindex', 'archive', 'ongoing chats']:
        continue
    norm = full.lower().replace('\\', '/')
    if norm in known:
        continue
    # Quick check
    fc = 0
    try:
        for root, dirs, files in os.walk(full):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
            fc += sum(1 for f in files if f.endswith(('.py', '.R', '.r', '.html', '.js')))
            if fc > 50:
                break
    except:
        pass
    if fc > 0:
        sub = 'SUBSTANTIAL' if fc >= 3 else 'THIN'
        new_projects.append((full, fc, sub, '', name))

# Report
substantial = [p for p in new_projects if p[2] == 'SUBSTANTIAL']
thin = [p for p in new_projects if p[2] == 'THIN']

print(f"New projects not in workbook: {len(new_projects)}")
print(f"  Substantial (>=3 code files): {len(substantial)}")
print(f"  Thin (<3 code files): {len(thin)}")
print()

# Count ctgov projects
ctgov_new = [p for p in new_projects if 'ctgov' in p[0].lower()]
non_ctgov = [p for p in new_projects if 'ctgov' not in p[0].lower()]
print(f"  CT.gov analysis projects: {len(ctgov_new)}")
print(f"  Other projects: {len(non_ctgov)}")
print()

print("=== SUBSTANTIAL NON-CTGOV NEW PROJECTS ===")
for path, fc, sub, tags, name in sorted(non_ctgov, key=lambda x: -x[1]):
    if sub == 'SUBSTANTIAL':
        print(f"  {fc:4d} files  {path}{tags}")

print()
print(f"=== SUBSTANTIAL CT.GOV PROJECTS ({len([p for p in ctgov_new if p[2]=='SUBSTANTIAL'])}) ===")
for path, fc, sub, tags, name in sorted(ctgov_new, key=lambda x: -x[1])[:10]:
    if sub == 'SUBSTANTIAL':
        print(f"  {fc:4d} files  {path}{tags}")
if len([p for p in ctgov_new if p[2]=='SUBSTANTIAL']) > 10:
    print(f"  ... and {len([p for p in ctgov_new if p[2]=='SUBSTANTIAL'])-10} more")

print()
print("=== THIN PROJECTS (likely scaffolds) ===")
for path, fc, sub, tags, name in sorted(non_ctgov, key=lambda x: x[0]):
    if sub == 'THIN':
        print(f"  {fc:4d} files  {path}{tags}")
