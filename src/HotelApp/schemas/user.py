"""
Schemas Pydantic para la entidad User.

Reglas de negocio validadas aqui:
- first_name y last_name deben tener entre 2 y 100 caracteres.
- email debe tener un formato de correo electronico valido.
"""

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserBase(BaseModel):
    """Campos comunes a todas las representaciones de User."""

    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre del usuario.",
        examples=["Cristian"],
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Apellido del usuario.",
        examples=["Escobar"],
    )
    email: EmailStr = Field(
        ...,
        description="Correo electronico unico del usuario.",
        examples=["cristian@ejemplo.com"],
    )


class UserCreate(UserBase):
    """Payload para crear un nuevo usuario (POST /users)."""


class UserUpdate(BaseModel):
    """Payload para actualizar un usuario (PATCH o PUT /users/{id}).

    Todos los campos son opcionales.
    """

    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = Field(
        default=None,
    )

    @model_validator(mode="after")
    def at_least_one_field(self) -> "UserUpdate":
        if self.first_name is None and self.last_name is None and self.email is None:
            raise ValueError(
                "Se debe enviar al menos un campo para actualizar (first_name, last_name o email)."
            )
        return self


class UserResponse(UserBase):
    """Representacion de un usuario devuelta por la API."""

    id: int = Field(..., description="Identificador unico generado por la BD.")

    model_config = {"from_attributes": True}