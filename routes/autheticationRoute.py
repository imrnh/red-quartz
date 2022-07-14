from fastapi import APIRouter

authRouter = APIRouter()



# ------------------------------------
# ------------------------------------
#               
#               SIGNUP 
#
# ------------------------------------
# ------------------------------------

@authRouter.post("/register")
async def register():
    return {"Registration complete"}







# ------------------------------------
# ------------------------------------
#               
#               LOGIN 
#
# ------------------------------------
# ------------------------------------

@authRouter.post("/login")
async def login():
    return {"Logged in"}