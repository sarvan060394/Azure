from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Jinja2 template setup
templates = Jinja2Templates(directory="templates")

# Mock database of images with versions
images_data = {
    "nginx": ["nginx:latest", "nginx:1.20", "nginx:1.19"],
    "redis": ["redis:latest", "redis:6.2", "redis:5.0"],
    "kafka": ["kafka:latest", "kafka:2.8", "kafka:2.7"],
}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renders the home page where the user inputs an image name."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/images", response_class=HTMLResponse)
async def list_images(request: Request, image_name: str = Form(...)):
    """Lists available versions of the entered image."""
    image_versions = images_data.get(image_name, [])
    return templates.TemplateResponse(
        "images.html",
        {"request": request, "image_name": image_name, "image_versions": image_versions},
    )


@app.post("/delete")
async def delete_images(request: Request, image_name: str = Form(...), selected_version: str = Form(...)):
    """Deletes the selected image version."""
    if image_name in images_data and selected_version in images_data[image_name]:
        images_data[image_name].remove(selected_version)

    return RedirectResponse(url="/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
