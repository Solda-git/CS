# from sqlalchemy import create_engine, Column, Integer, MetaData, String, Table
import os

# engine = create_engine()

if os.path.exists("./DB/chat.db"):
    print('exists')

#     os.remove("some.db")
# e = create_engine("sqlite:///some.db")