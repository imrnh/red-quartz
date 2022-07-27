# Copied from gfg.
# Link: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
from fastapi import HTTPException, status
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# EKhane, ora basically email ke evabe vag korce. something@something.com.
# Mane @ er age kichu regex jegulo te sudhu A-Z, a-z, 0-9 o ._%+- er jekono sign thakbe.
# @ er pore . er age A-Z, a-z, 0-9 p . ebong _ allowed. ar . er por suhdhu A-Z o a-z

def is_valid_email(email):
    if not re.fullmatch(regex, email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Given email address is not a valid email address.")
