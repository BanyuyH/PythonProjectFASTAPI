from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime
from app.database import mongodb
from app.models.user import User, UserCreate
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/signup', response_model=User, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)

    user_dict = user.model_dump()
    user_dict["password"] = hashed_password  # Replace with hashed password
    user_dict["created_at"] = datetime.now()
    # Check if user already exists
    collection = mongodb.get_collection("users")
    existing_user = await collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create user document
    user_dict = user.model_dump()
    user_dict["created_at"] = datetime.now()  # Fixed typo and use UTC

    # Insert into database
    result = await collection.insert_one(user_dict)

    # Get the created user
    created_user = await collection.find_one({"_id": result.inserted_id})  # Fixed typo and field name

    # Convert ObjectId to string for response
    created_user["_id"] = str(created_user["_id"])
    return User(**created_user)


@router.get('/users', response_model=list[User])
async def get_users(skip: int = 0, limit: int = 100):
    collection = mongodb.get_collection("users")
    users = []

    async for user in collection.find().skip(skip).limit(limit):
        # Convert ObjectId to string for each user
        user["_id"] = str(user["_id"])
        users.append(User(**user))

    return users


@router.post("/login")  # Changed to POST for login (more secure)
async def login_user(email: str, password: str):  # Login typically uses email/password
    collection = mongodb.get_collection("users")

    # Find user by email and password
    user = await collection.find_one({"email": email, "password": password})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Convert ObjectId to string for response
    user["_id"] = str(user["_id"])
    return User(**user)


# Additional route to get user by ID
@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    collection = mongodb.get_collection("users")
    user = await collection.find_one({"_id": ObjectId(user_id)})  # Fixed field name

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Convert ObjectId to string for response
    user["_id"] = str(user["_id"])
    return User(**user)