from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# ==============================================================================
# ÉNUMÉRATIONS (Alignées sur les contraintes CHECK de schema.sql)
# ==============================================================================

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class AvailabilityType(str, Enum):
    DAY = "DAY"
    WEEK = "WEEK"


class OrderStatus(str, Enum):
    RESERVED = "RESERVED"
    COMPLETED = "COMPLETED"
    NO_SHOW = "NO_SHOW"
    CANCELLED = "CANCELLED"


# ==============================================================================
# TABLES D'ASSOCIATION (Clés primaires composites)
# ==============================================================================

class MenuProduct(SQLModel, table=True):
    __tablename__ = "MENU_PRODUCTS"

    menu_id: Optional[int] = Field(
        default=None, foreign_key="MENUS.id", primary_key=True
    )
    product_id: Optional[int] = Field(
        default=None, foreign_key="PRODUCTS.id", primary_key=True
    )
    quantity: int = Field(default=1, gt=0)

    # Relations
    menu: Optional["Menu"] = Relationship(back_populates="menu_products")
    product: Optional["Product"] = Relationship(back_populates="menu_products")


class OrderItem(SQLModel, table=True):
    __tablename__ = "ORDER_ITEMS"

    order_id: Optional[int] = Field(
        default=None, foreign_key="ORDERS.id", primary_key=True
    )
    product_id: Optional[int] = Field(
        default=None, foreign_key="PRODUCTS.id", primary_key=True
    )
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)

    # Relations
    order: Optional["Order"] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="order_items")


# ==============================================================================
# MODÈLES PRINCIPAUX (Tables SQLite)
# ==============================================================================

class User(SQLModel, table=True):
    __tablename__ = "USERS"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    is_blocked: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relations
    orders: List["Order"] = Relationship(back_populates="user")


class Product(SQLModel, table=True):
    __tablename__ = "PRODUCTS"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    price: float = Field(ge=0, nullable=False)
    stock: int = Field(default=0, ge=0, nullable=False)
    is_available: bool = Field(default=True, nullable=False)

    # Relations
    menu_products: List[MenuProduct] = Relationship(back_populates="product")
    order_items: List[OrderItem] = Relationship(back_populates="product")


class Menu(SQLModel, table=True):
    __tablename__ = "MENUS"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    availability_type: AvailabilityType = Field(nullable=False)
    start_date: date = Field(nullable=False)
    end_date: date = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)

    # Relations
    menu_products: List[MenuProduct] = Relationship(
        back_populates="menu",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ClosureDay(SQLModel, table=True):
    __tablename__ = "CLOSURE_DAYS"

    id: Optional[int] = Field(default=None, primary_key=True)
    closure_date: date = Field(unique=True, nullable=False)
    reason: Optional[str] = Field(default=None)


class Order(SQLModel, table=True):
    __tablename__ = "ORDERS"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="USERS.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    pickup_date: date = Field(nullable=False)
    status: OrderStatus = Field(default=OrderStatus.RESERVED, nullable=False)

    # Relations
    user: Optional[User] = Relationship(back_populates="orders")
    items: List[OrderItem] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


# ==============================================================================
# SCHÉMAS D'ÉCHANGE API (DTOs pour FastAPI)
# ==============================================================================

# --- Users ---
class UserRead(SQLModel):
    id: int
    username: str
    role: UserRole
    is_blocked: bool
    created_at: datetime


class UserCreateResponse(UserRead):
    generated_password: str  # Transmis uniquement à la création du compte


class PasswordChange(SQLModel):
    old_password: str
    new_password: str


# --- Products ---
class ProductCreate(SQLModel):
    name: str
    description: Optional[str] = None
    price: float = Field(ge=0)
    stock: int = Field(default=0, ge=0)
    is_available: bool = True


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    stock: Optional[int] = Field(default=None, ge=0)
    is_available: Optional[bool] = None


class ProductRead(SQLModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    is_available: bool


# --- Menus ---
class MenuProductItem(SQLModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class MenuCreate(SQLModel):
    name: str
    description: Optional[str] = None
    availability_type: AvailabilityType
    start_date: date
    end_date: date
    is_active: bool = True
    products: List[MenuProductItem] = []


class MenuRead(SQLModel):
    id: int
    name: str
    description: Optional[str]
    availability_type: AvailabilityType
    start_date: date
    end_date: date
    is_active: bool


# --- Closure Days ---
class ClosureDayCreate(SQLModel):
    closure_date: date
    reason: Optional[str] = None


class ClosureDayRead(SQLModel):
    id: int
    closure_date: date
    reason: Optional[str]


# --- Orders ---
class OrderItemCreate(SQLModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(SQLModel):
    pickup_date: date
    items: List[OrderItemCreate]


class OrderItemRead(SQLModel):
    product_id: int
    quantity: int
    unit_price: float


class OrderRead(SQLModel):
    id: int
    user_id: int
    created_at: datetime
    pickup_date: date
    status: OrderStatus
    items: List[OrderItemRead] = []