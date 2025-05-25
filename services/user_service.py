from models.user import User

class UserService:
    def __init__(self, redis_client):
        self._client = redis_client

    def save_user(self, name, age, location):
        user = User(name, age, location)
        key = f"user:{user.name}"
        self._client.hset(key, mapping=user.to_redis_hash())

    def get_user(self, name):
        key = f"user:{name}"
        data = self._client.hgetall(key)
        if not data:
            return "No user found with that name."
        return User.from_redis_hash(data)
    
    def get_all_users(self):
        keys = self._client.keys("user:*")
        users = []
        for key in keys:
            data = self._client.hgetall(key)
            if data:
                users.append(User.from_redis_hash(data))
        return users