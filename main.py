from core.init_app import create_app
import uvicorn
from core.config import settings
app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)