from apps.jobs.models.user import User
from apps.jobs.schemas.user import UserCreate, UserUpdate


class UserService:
  def create(self, user: UserCreate) -> User:
    new_user = User.objects.create_user(
      # Excluimos el password para que django lo hashee
      **user.model_dump(exclude={'password'}),
      password=user.password,
    )
    new_user.creator_id = new_user.id  # type: ignore
    new_user.modifier_id = new_user.id  # type: ignore
    new_user.save()
    return new_user

  def patch(self, user_bd: User, user: UserUpdate) -> User:
    user_data = user.model_dump(exclude_unset=True)
    if not user_data:
      return user_bd
    for field, value in user_data.items():
      if field == 'password':
        user_bd.set_password(value)
        continue
      setattr(user_bd, field, value)
    user_bd.modifier_id = user_bd.id  # type: ignore
    user_bd.save()
    return user_bd

  def deactivate(self, user_bd: User) -> User:
    user_bd.is_active = False
    user_bd.modifier_id = user_bd.id  # type: ignore
    user_bd.save()
    return user_bd


user_service = UserService()
