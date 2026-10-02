#!/usr/bin/env python3
"""Verify the packaged HCM_1000 V2 inputs and archived feasible witnesses."""
import argparse,array,collections,csv,hashlib,json,math,re,sys
from pathlib import Path

def instance(path):
    lines=path.read_text(encoding='utf-8-sig').splitlines()
    h=next(i for i,s in enumerate(lines) if s.strip()=='NUMBER     CAPACITY')
    limit,capacity=map(int,lines[h+1].split())
    rows=[]
    for s in lines[h+2:]:
        fields=s.split()
        if len(fields)==9 and fields[0].isdigit():rows.append(list(map(float,fields)))
    assert len(rows)==1001, f'{path.name}: row count'
    assert [r[0] for r in rows]==list(range(1001)),f'{path.name}: node IDs'
    assert all(all(math.isfinite(v) for v in r) for r in rows),f'{path.name}: nonfinite'
    assert all(-90<=r[3]<=90 and -180<=r[4]<=180 and 0<=r[5]<=capacity and r[6]<=r[7] and r[8]>=0 for r in rows),f'{path.name}: attributes'
    assert rows[0][5]==0 and rows[0][8]==0,f'{path.name}: depot attributes'
    assert limit>0 and capacity>0,f'{path.name}: vehicle header'
    return limit,capacity,rows

def matrix(path,geometry):
    with (path.parent / f'node_order_{geometry}.csv').open(newline='',encoding='utf-8') as f:
        mapping=list(csv.DictReader(f))
    assert len(mapping)==1001 and [int(x['node_id']) for x in mapping]==list(range(1001)), 'node-order mapping'
    expected=[x['matrix_label'] for x in mapping]
    assert expected[0]=='DEPOT' and len(set(expected))==1001, 'unique matrix labels'
    if geometry!='RC':assert expected==['DEPOT']+[f'{geometry}_{i}' for i in range(1,1001)], 'geometry labels'
    values=array.array('d')
    with path.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.reader(f);header=next(reader)
        assert header[1:]==expected,f'{path.name}: column labels'
        count=0
        for i,line in enumerate(reader):
            assert i<1001 and len(line)==1002 and line[0]==expected[i],f'{path.name}: row labels/width'
            nums=list(map(float,line[1:]))
            assert all(math.isfinite(v) and (v==0 if i==j else v>0) for j,v in enumerate(nums)),f'{path.name}: numeric integrity at row {i}'
            values.extend(nums);count+=1
        assert count==1001,f'{path.name}: shape'
    return values

def witness(rows,dm,tm,routes,capacity,limit):
    assert isinstance(routes,list) and 0<len(routes)<=limit,'fleet limit'
    visits=[];distance=0.;eps=1e-7
    for route in routes:
        assert isinstance(route,list) and len(route)>=3 and route[0]==route[-1]==0 and 0 not in route[1:-1],'route structure'
        assert all(type(i)==int and 0<=i<=1000 for i in route),'route IDs'
        visits.extend(route[1:-1]);assert sum(rows[i][5] for i in route[1:-1])<=capacity+eps,'capacity'
        clock=rows[0][6]
        for a,b in zip(route,route[1:]):
            start=max(rows[b][6],clock+tm[a*1001+b]/60.)
            assert start<=rows[b][7]+eps,f'time window/depot return: {b}'
            clock=start+rows[b][8];distance+=dm[a*1001+b]
    assert collections.Counter(visits)==collections.Counter(range(1,1001)),'unique customer coverage'
    return {'feasible':True,'vehicles':len(routes),'distance_m':distance}

def verify(root):
    errors=[];results=[];checks=[]
    meta=json.loads((root/'documentation/release_metadata.json').read_text())
    manifest=json.loads((root/'documentation/file_manifest.json').read_text())
    for item in manifest:
        p=root/item['path']
        if not p.is_file() or p.stat().st_size!=item['size_bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:errors.append('Digest mismatch: '+item['path'])
    print(f'File integrity: {len(manifest)} entries; errors: {len(errors)}',flush=True)
    paths=sorted((root/'data/instances').glob('*/*.txt'))
    counts=collections.Counter(p.parent.name for p in paths)
    if dict(counts)!=meta['family_counts']:errors.append('Family counts do not match expected 56 instances')
    if errors:return {'passed':False,'errors':errors,'instances':results,'matrix_checks':checks}
    for geometry in meta['geometries']:
        try:
            dm=matrix(root/f'data/matrices/Distance_Matrix_{geometry}.csv',geometry)
            tm=matrix(root/f'data/matrices/Time_Matrix_{geometry}.csv',geometry)
            checks.append({'geometry':geometry,'shape':[1001,1001],'finite':True,'diagonal_zero':True,'off_diagonal_positive':True,'node_labels_aligned':True})
            canonical=None
            for p in paths:
                family=p.parent.name
                g=family if family in ['C1','C2'] else ('RC' if family.startswith('RC') else 'R')
                if g!=geometry:continue
                try:
                    limit,capacity,rows=instance(p)
                    coords=[r[1:5] for r in rows]
                    if canonical is None:canonical=coords
                    assert coords==canonical,'shared geometry mismatch'
                    result=witness(rows,dm,tm,json.loads((root/f'validation/witnesses/{p.stem}/routes.json').read_text()),capacity,limit)
                    archived=json.loads((root/f'validation/witnesses/{p.stem}/validation.json').read_text())
                    assert archived['feasible'] is True,'archived witness not feasible'
                    result.update(instance=p.stem,family=family);results.append(result)
                except (AssertionError,ValueError,KeyError,OSError) as e:errors.append(f'{p.stem}: {e}')
            print(f'{geometry}: matrices checked, cumulative {len(results)} feasible witnesses',flush=True)
            del dm,tm
        except (AssertionError,ValueError,KeyError,OSError) as e:errors.append(f'{geometry}: {e}')
    return {'passed':not errors and len(results)==56,'dataset':'HCM_1000 V2','source_archive_sha256':meta['source_archive_sha256'],'verified_manifest_files':len(manifest),'validated_witnesses':len(results),'errors':errors,'instances':results,'matrix_checks':checks,'optimality_proven':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--output',type=Path);args=parser.parse_args()
    try:report=verify(args.root.resolve())
    except Exception as e:report={'passed':False,'errors':[f'{type(e).__name__}: {e}']}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['instances','matrix_checks']},indent=2))
    sys.exit(0 if report['passed'] else 1)
