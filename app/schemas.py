from datetime import datetime
from pydantic import BaseModel, EmailStr


"""
            USERS
                            """

# schema or structure of a user
class UserModel(BaseModel):
    email: EmailStr
    password: str


# schema for a user response
class UserResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserInfo(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

'''
            POSTS
                            '''

# schema or structure of a post
class PostModel(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostOutModel(BaseModel):
    title: str
    content: str
    is_published: bool = True
    created_at: datetime
    owner: UserInfo

    class Config:
        from_attributes = True


# schema for creating a post
class CreatePostModel(PostModel):
    pass


class PostOut(PostModel):
    created_at: datetime
    owner: UserInfo


class PostResponse(BaseModel):
    Post: PostOutModel
    likes: int

"""
            LOGIN
                            """

# schema for user logins
class LoginModel(UserModel):
    pass


""" 
            TOKEN
                            """

# schema for access tokens
class Token(BaseModel):
    access_token: str
    token_type: str

# scheman for token data
class TokenData(BaseModel):
    id: int


""" 
            LIKES
                            """
# schema for liking a post
class LikeModel(BaseModel):
    post_id: int
    like_dir: bool