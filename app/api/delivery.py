from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db import get_db
from app.models.models import Widget

router = APIRouter()

@router.get("/widgets/{widget_id}/config")
def get_config(widget_id: str, response: Response, db: Session = Depends(get_db)):
    w = db.query(Widget).filter(Widget.id == widget_id).first()
    if not w: raise HTTPException(404, "not found")
    response.headers["Cache-Control"] = "public, max-age=60"  # short-lived config cache
    return {
        "id": w.id, "type": w.type, "title": w.title, "description": w.description,
        "fields": w.fields, "button_text": w.button_text, "version": w.version,
    }

@router.get("/widget.js")
def get_widget_script(response: Response):
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"  # long cache, versioned via query param
    return Response(content=WIDGET_JS, media_type="application/javascript")

WIDGET_JS = """
(function() {
  const script = document.currentScript;
  const id = new URL(script.src).searchParams.get('id');
  fetch(`http://localhost:8000/widgets/${id}/config`)
    .then(r => r.json())
    .then(cfg => {
      const div = document.createElement('div');
      div.innerHTML = `<form id="w-form">
        ${cfg.fields.map(f => `<input name="${f.name}" placeholder="${f.name}" ${f.required ? 'required' : ''}>`).join('')}
        <input type="text" name="honeypot" style="display:none">
        <button type="submit">${cfg.button_text}</button>
      </form>`;
      script.parentNode.insertBefore(div, script.nextSibling);
      div.querySelector('#w-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));
        const honeypot = data.honeypot; delete data.honeypot;
        fetch('http://localhost:8000/submissions', {
          method: 'POST', headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({widget_id: id, data, honeypot})
        }).then(() => alert('Submitted!'));
      });
    });
})();
"""