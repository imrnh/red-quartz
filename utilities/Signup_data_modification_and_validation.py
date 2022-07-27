from fastapi import HTTPException, status


def remove_whitespaces_from_front_and_rear(new_user: object) -> object:
    new_user.username: str = new_user.username.strip()
    new_user.email: str = new_user.email.strip()
    new_user.first_name: str = new_user.first_name.strip()
    new_user.last_name: str = new_user.last_name.strip()
    new_user.password: str = new_user.password.strip()  # a-z, A-Z, 0-9 and _ ! @ # $ % ^ & * ( ) - + /

    return new_user


def username_validator(given_username):
    given_username = given_username.lower()
    username_length = len(given_username)
    if username_length > 15 or username_length < 3:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                             detail="Username should be between 3 and 15 characters")

    underscore_count = 0
    for singleChar in given_username:
        if 'a' <= singleChar <= 'z':
            continue
        elif '0' <= singleChar <= '9':
            continue
        elif singleChar == "_":
            underscore_count += 1
            continue
        else:
            return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                 detail="Username should only contain [a-z, 0-9, and underscore ( _ ).] ")
            break

    if underscore_count > 2:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                             detail="Username should not contain more than 2 underscore.")


# Password should be between 8 and 50 characters.
# Password cannot contain ;
def check_password_ok(password_given):
    pass_length = len(password_given)
    if pass_length > 50 or pass_length < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password should be between 8 and 50 characters")

    # [a-z, A-Z, 0-9, !, @, #, *, -, +, /] are allowed
    allowed_characters = set('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890!@#*-+/')
    suspicious = True if set(password_given) - set(allowed_characters) else False;

    if suspicious:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Password can only contain [a-z, A-Z, 0-9, !, @, #, *, -, +, /]")


