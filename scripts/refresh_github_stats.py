#!/usr/bin/env python3
"""Refresh the public snapshot and rebuild the profile. No credentials required."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
OWNER='araxis07'

def get_json(url):
    req=Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'araxis07-profile-stats'})
    with urlopen(req,timeout=30) as res:return json.load(res)

def authored_count(kind):
    url='https://api.github.com/search/issues?'+urlencode({'q':f'author:{OWNER} is:{kind} is:public','per_page':1})
    data=get_json(url)
    if data.get('incomplete_results'):raise RuntimeError('GitHub returned incomplete search results')
    return data['total_count']

def main():
    snapshot=json.loads((ROOT/'data/github-stats.json').read_text())
    rows=[];page=1
    while True:
        batch=get_json(f'https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}')
        if not isinstance(batch,list):raise RuntimeError('Unexpected repository response')
        rows.extend(r for r in batch if not r['private'] and r['owner']['login'].lower()==OWNER)
        if len(batch)<100:break
        page+=1
    if not rows or len({r['id'] for r in rows})!=len(rows):raise RuntimeError('Missing or duplicate repository data')
    snapshot['repositories']=[dict(name=r['name'],full_name=r['full_name'],url=r['html_url'],private=False,fork=r['fork'],archived=r['archived'],language=r['language'],stars=r['stargazers_count'],forks=r['forks_count'],created_at=r['created_at'],updated_at=r['updated_at'],default_branch=r['default_branch']) for r in sorted(rows,key=lambda r:r['name'].lower())]
    snapshot['authored_public_pull_requests']=authored_count('pr')
    snapshot['authored_public_issues']=authored_count('issue')
    snapshot['snapshot_date']=datetime.datetime.now(ZoneInfo('Asia/Tokyo')).date().isoformat()
    path=ROOT/'data/github-stats.json'
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
    temporary.replace(path)
    subprocess.run([sys.executable,str(ROOT/'scripts/build_profile.py')],check=True)
    print(f'Refreshed {len(rows)} public repositories. Review the changes before committing.')

if __name__=='__main__':main()
