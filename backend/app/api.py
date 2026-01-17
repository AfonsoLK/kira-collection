import cloudinary.uploader
from ninja import NinjaAPI
from core.schemas import UserCreateSchema, UserOutputSchema, UserUpdateSchema
from core.models import User
from ninja.files import UploadedFile
from ninja import Form, File
from ninja.responses import Response
from scalar_ninja import ScalarViewer


api = NinjaAPI(
    docs=ScalarViewer(),
)

@api.post("/users/create", response=UserOutputSchema)
def create_user(request, data: UserCreateSchema = Form(...), avatar: UploadedFile = File(None)):
    user = User.objects.create_user(
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=data.password,
        age=data.age,
        bio=data.bio,
    )
    
    if avatar:
        try:
            upload_result = cloudinary.uploader.upload(avatar.file)
            image_url = upload_result.get('secure_url')
            user.avatar_url = image_url
        except Exception as e:
            return Response(status=400, content={"error": f"Erro no upload: {e}"})

    user.save()
    return user

@api.get("/users/get/{user_id}", response=UserOutputSchema)
def get_user(request, user_id: int):
    user = User.objects.get(id=user_id)
    if not user:
        return Response(status=404, content={"error": "Usuário não encontrado"})
    return user


@api.put("/users/update/{user_id}", response=UserOutputSchema)
def update_user(request, user_id: int, data: UserUpdateSchema = Form(...), avatar: UploadedFile = File(None)):
    user = User.objects.get(id=user_id)
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.age = data.age
    user.bio = data.bio

    if data.password:
        user.set_password(data.password)

    if avatar:
        try:
            upload_result = cloudinary.uploader.upload(avatar.file)
            image_url = upload_result.get('secure_url')
            user.avatar_url = image_url

        except Exception as e:
            return Response(status=400, content={"error": f"Erro no upload: {e}"})

    user.save()
    return user

@api.delete("/users/delete/{user_id}", response={204: None})
def delete_user(request, user_id: int):
    user = User.objects.get(id=user_id)
    if not user:
        return Response(status=404, content={"error": "Usuário não encontrado"})
    user.delete()
    return 204