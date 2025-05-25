from fastmcp import Resource, Tool
from utils.eagle_api import eagle_api_get

class ApplicationResource(Resource):
    name = "application"
    description = "Eagle application operations"

    @Tool()
    async def get_application_info(self):
        return await eagle_api_get("/api/application/info")

    # 他のAPIも順次移植予定
