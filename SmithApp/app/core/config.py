class Settings:
    DATABASE_URL: str = "postgresql://postgres.nyrjoituwybubeuodwxz:MaropeneMoa@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"
    SECRET_KEY: str = "jkdneajdfhjkhjlasdjfhweipoklvo"
    SESSION_MAX_AGE: int = 3600  # 1 hour

settings = Settings()