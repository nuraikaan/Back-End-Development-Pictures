from flask import Flask, jsonify, request
from pathlib import Path
import json
app=Flask(__name__)
DATA_FILE=Path(__file__).with_name('pictures.json')
def load(): return json.loads(DATA_FILE.read_text())
def save(x): DATA_FILE.write_text(json.dumps(x,indent=2))
@app.get('/health')
def health(): return jsonify({'status':'OK'})
@app.get('/count')
def count(): return jsonify({'count':len(load())})
@app.get('/picture')
def pictures(): return jsonify(load())
@app.get('/picture/<int:pid>')
def picture(pid):
    x=next((p for p in load() if p['id']==pid),None)
    return (jsonify(x),200) if x else (jsonify({'error':'Picture not found'}),404)
@app.post('/picture')
def post():
    x=request.get_json(silent=True) or {}; req=['id','pic_url','event_country','event_state','event_city','event_date']
    if any(k not in x for k in req): return jsonify({'error':'Missing required field'}),400
    data=load()
    if any(p['id']==x['id'] for p in data): return jsonify(x),409
    data.append(x); save(data); return jsonify(x),201
@app.put('/picture/<int:pid>')
def put(pid):
    x=request.get_json(silent=True) or {}; data=load()
    for i,p in enumerate(data):
        if p['id']==pid:
            data[i]={**p,**x,'id':pid}; save(data); return jsonify(data[i])
    return jsonify({'error':'Picture not found'}),404
@app.delete('/picture/<int:pid>')
def delete(pid):
    data=load(); new=[p for p in data if p['id']!=pid]
    if len(new)==len(data): return jsonify({'error':'Picture not found'}),404
    save(new); return jsonify({'status':'Deleted'})
if __name__=='__main__': app.run(host='0.0.0.0',port=5001)
