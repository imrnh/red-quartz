from fastapi import HTTPException, status

def remove_whitespaces_from_front_and_rear(newUser):
    newUser.username : str = (newUser.username).strip()
    newUser.email : str = (newUser.email).strip()
    newUser.first_name: str = (newUser.first_name).strip()
    newUser.last_name: str = (newUser.last_name).strip()
    newUser.password: str = (newUser.password).strip()  #Password can only be a-z, A-Z, 0-9 and _ ! @ # $ % ^ & * ( ) - + /   Anything else is not allowed.
    newUser.confirm_password: str = (newUser.confirm_password).strip()

    return newUser



def username_validator(userName):
    userName = userName.lower()
    username_length = len(userName) #created a variable so that we don't have to perform this operation twice while checking inside if statement as we have to use this len() functions return twice.
    if username_length > 15 or username_length <3:
        return HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, 
                    detail="Username should be at least 3 character long and not more than 15 characters")
    
    underscore_count = 0
    for singleChar in userName:
        if singleChar >= 'a' and singleChar <= 'z':
            continue
        elif singleChar >= '0' and singleChar <= '9':
            continue
        elif singleChar == "_":
            underscore_count += 1
            continue
        else:
            return HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, 
                        detail="Username should only contain [a-z, 0-9, and underscore ( _ ).] ")
            break
        
    if underscore_count > 2:
        return HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, 
                    detail="Username should not contain more than 2 underscore.")

