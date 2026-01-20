#!/usr/bin/env python3

from faker import Faker
from random import randint

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))


def seed_database():
    """Seed the database with test data."""
    from app import app
    from models import db, Article, User
    
    fake = Faker()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Only seed if tables are empty
        if Article.query.first() is None:
            print("Seeding database for tests...")
            
            # Create users
            users = [User(name=fake.name()) for i in range(25)]
            db.session.add_all(users)
            
            # Create articles
            articles = []
            for i in range(100):
                content = fake.paragraph(nb_sentences=8)
                preview = content[:25] + '...'
                
                article = Article(
                    author=fake.name(),
                    title=fake.sentence(),
                    content=content,
                    preview=preview,
                    minutes_to_read=randint(1, 20),
                    date=fake.date_time_this_year(),
                )
                articles.append(article)
            
            db.session.add_all(articles)
            db.session.commit()
            print("Database seeded successfully.")


# Seed database before tests run
seed_database()
