import io, sys, time, os, glob
if "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

o = Options()
o.add_argument('--headless=new'); o.add_argument('--no-sandbox')
o.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
d = webdriver.Chrome(options=o)
bad = 0
try:
    for cap in sorted(glob.glob('*-capsule.html')):
        d.get('file:///' + os.path.abspath(cap).replace('\\', '/'))
        time.sleep(0.8)
        errs = [l for l in d.get_log('browser')
                if l['level'] == 'SEVERE' and 'webr' not in l['message'].lower()
                and 'favicon' not in l['message'].lower()]
        if errs:
            bad += 1
            print('FAIL', cap)
            for e in errs[:3]:
                print('   ', e['message'][:160])
        else:
            print('ok  ', cap)
finally:
    d.quit()
print('\n%d capsule(s) with SEVERE console errors' % bad)
sys.exit(1 if bad else 0)
