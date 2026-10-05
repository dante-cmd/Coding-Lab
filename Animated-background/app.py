from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from read_img import get_rgb
import numpy as np

app = FastAPI()

# templates
templates = Jinja2Templates(directory="templates")

# index, include css and js

@app.get("/", response_class=HTMLResponse)
async def index(request:Request):
    # 1. make the root in the sever
    # 2. where is the root
    # 3. the name for the html file
    app.mount("/static", StaticFiles(directory="static"), name="static")

    context = {'request': request}
    return templates.TemplateResponse("index.html", context)


# websocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        url_img = await websocket.receive_text()
        output = get_rgb(url_img)
        output = output/255 if np.any(output>1) else output
        color_middle, color_max = output
        color_middle, color_max = tuple(color_middle), tuple(color_max)
        if output.shape[1]==3:
            toExportMiddle = "rgb({:.2%}, {:.2%}, {:.2%})".format(*color_middle)
            toExportMax = "rgb({:.2%}, {:.2%}, {:.2%})".format(*color_max)
            await websocket.send_text(toExportMax + "-" + toExportMiddle) 
        else :
            toExportMiddle = "rgba({:.2%}, {:.2%}, {:.2%}, {:.2%})".format(*color_middle)
            toExportMax = "rgba({:.2%}, {:.2%}, {:.2%}, {:.2%})".format(*color_max)
            await websocket.send_text(toExportMax + "-" + toExportMiddle) 
