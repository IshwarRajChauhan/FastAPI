from fastapi import APIRouter

#To use different fastapi app , we need to route it 
# 1.First create a routers folder , and in it create your file
# 2. Import APIRouters , and just we create an instance of app , we create an instance of router
# 3.Now use that instance in place of app

router = APIRouter()

@router.get("/auth/")
async def get_user():
    return {"user":"authenticated"}











