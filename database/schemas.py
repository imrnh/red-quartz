from datetime import date
from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    authjwt_secret_key : str = "a27d43eb6d212fb74b100dda9e63da53191a10095892607c713cf0f3ba4e72a7c5b4ce55a7d71be5d3c0bbe1672e288a50c25ab67976dafe3bbdfe7f04d261ab31cf1016666cb61546d80efb7f3b8a0a2bb9b63cb459f08f60a0d5044c8ab1465208fe4e6a446607fe734c867f8fd4952affd5f31549eb4fd41ad5e51f5198b8c43c1dcc66803d6b361f2a3bbfc11962686a2d76ef5a67a37ef57a67a06db9b15cca66d16f417a33659d650d4ffaa70af9099d3b56a8a5759085262fc441b0bd1f73a14f04c6ea378c33a164d44d21f3ab8ebffe7e86594ff5fdaf8d836f297d68920dc4df4c6497cee0b0524b716e3d0f5be876f1159f5f6d04e81146a37c13470cb84e9b9a7a2e1f8e12da7c223b8b9dbb455911da3c2c7ba1b9ae936dcc083dd067383cf96ba46886028c2b95fb6de168ce3d3f1cd1371c1cf70390859b768c1b083b477e2ea271ba28b02e13c9637252089df12068785c44c0cc30693c40ad320bec84339d43d8a42a2c30218b6d0452c34906ce0c211cbe88d8eaca7c1e8561fdc3474e27f0da1901dcac14749834e55c811a4f1e54e1abcb583621b747fbbd5cd40085a1213dbf938c0c1397aea2f0608d5164f02459bd9ceb81311dbf9db4cb62a6a6d1516e3a73b2ec8777d637abe92a1f9684c279a879f5aadfdac9d6b6235387a7592c64463981e1cc29800e844aa3"


class LoginModel(BaseModel):
    username : str 
    password : str 


class UserModel(BaseModel):
    id : int 
    username : str 
    email : str 
    first_name : str 
    last_name : str
    password : str 

class TaskMode(BaseModel):
    title : str
    description: str 

    repeatOn : List[str]