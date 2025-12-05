"""Simple FastAPI server exposing /inspect and /report endpoints."""
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import uvicorn, os, logging
from controllers.crawler_controller import CrawlerController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='SEO Inspector MVP API')

TASKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))

@app.get('/inspect')
async def inspect(url: str = Query(..., description='URL to inspect')):
    controller = CrawlerController(url)
    try:
        res = controller.run()
        return JSONResponse(res)
    except Exception as e:
        logger.exception('Inspection failed')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/report/{task_id}')
async def get_report(task_id: str):
    report_dir = os.path.join(TASKS_DIR, task_id)
    report_file = os.path.join(report_dir, 'report.html')
    if not os.path.exists(report_file):
        raise HTTPException(status_code=404, detail='Report not found')
    return FileResponse(report_file, media_type='text/html')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
