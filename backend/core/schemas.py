from ninja import Schema

class UserCreateSchema(Schema):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    age: int
    bio: str | None = None

class UserOutputSchema(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    age: int
    bio: str
    avatar_url: str | None = None

class UserUpdateSchema(Schema):
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    age: int | None = None
    bio: str | None = None