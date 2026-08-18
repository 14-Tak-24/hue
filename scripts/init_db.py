#!/usr/bin/env python3
"""
Tiapma'atzu Database Initialization Script
Initializes PostgreSQL database with required tables and data
"""

import os
import sys
import psycopg2
from datetime import datetime
import json

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'hue_db'),
    'user': os.getenv('DB_USER', 'hue'),
    'password': os.getenv('DB_PASSWORD', 'huepassword'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def create_tables(conn):
    """Create required database tables"""
    print("Creating database tables...")
    
    tables = [
        """
        CREATE TABLE IF NOT EXISTS souls (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            archetype VARCHAR(100),
            rarity VARCHAR(50),
            tier VARCHAR(50),
            platforms JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tributes (
            id SERIAL PRIMARY KEY,
            soul_id VARCHAR(50) REFERENCES souls(id),
            amount DECIMAL(10, 2) NOT NULL,
            impact_area VARCHAR(100),
            platform VARCHAR(100),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS financial_transactions (
            id SERIAL PRIMARY KEY,
            transaction_type VARCHAR(50) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            description TEXT,
            category VARCHAR(100),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS analytics_events (
            id SERIAL PRIMARY KEY,
            event_type VARCHAR(100) NOT NULL,
            soul_id VARCHAR(50),
            platform VARCHAR(100),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS content_library (
            id SERIAL PRIMARY KEY,
            soul_id VARCHAR(50) REFERENCES souls(id),
            content_type VARCHAR(50),
            platform VARCHAR(100),
            content TEXT,
            template VARCHAR(100),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    cursor = conn.cursor()
    for table_sql in tables:
        try:
            cursor.execute(table_sql)
            print(f"✓ Table created successfully")
        except psycopg2.Error as e:
            print(f"✗ Error creating table: {e}")
            conn.rollback()
            return False
    
    conn.commit()
    cursor.close()
    print("All tables created successfully")
    return True

def create_indexes(conn):
    """Create database indexes for performance"""
    print("Creating database indexes...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_tributes_soul_id ON tributes(soul_id);",
        "CREATE INDEX IF NOT EXISTS idx_tributes_created_at ON tributes(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_financial_transactions_type ON financial_transactions(transaction_type);",
        "CREATE INDEX IF NOT EXISTS idx_financial_transactions_created_at ON financial_transactions(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_analytics_events_type ON analytics_events(event_type);",
        "CREATE INDEX IF NOT EXISTS idx_analytics_events_soul_id ON analytics_events(soul_id);",
        "CREATE INDEX IF NOT EXISTS idx_content_library_soul_id ON content_library(soul_id);",
        "CREATE INDEX IF NOT EXISTS idx_content_library_platform ON content_library(platform);"
    ]
    
    cursor = conn.cursor()
    for index_sql in indexes:
        try:
            cursor.execute(index_sql)
            print(f"✓ Index created successfully")
        except psycopg2.Error as e:
            print(f"✗ Error creating index: {e}")
            conn.rollback()
            return False
    
    conn.commit()
    cursor.close()
    print("All indexes created successfully")
    return True

def seed_initial_data(conn):
    """Seed database with initial data"""
    print("Seeding initial data...")
    
    cursor = conn.cursor()
    
    # Check if souls table is empty
    cursor.execute("SELECT COUNT(*) FROM souls;")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print("Database already contains data, skipping seed")
        cursor.close()
        return True
    
    # Load souls from JSON file if exists
    souls_file = "scripts/content_library_master.json"
    if os.path.exists(souls_file):
        try:
            with open(souls_file, 'r') as f:
                data = json.load(f)
            
            # Insert souls data
            for soul in data.get('souls', []):
                cursor.execute(
                    """
                    INSERT INTO souls (id, name, archetype, rarity, tier, platforms)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        soul.get('id'),
                        soul.get('name'),
                        soul.get('archetype'),
                        soul.get('rarity'),
                        soul.get('tier'),
                        json.dumps(soul.get('platforms', []))
                    )
                )
            
            conn.commit()
            print(f"✓ Seeded {len(data.get('souls', []))} souls")
        except Exception as e:
            print(f"✗ Error seeding data: {e}")
            conn.rollback()
            cursor.close()
            return False
    else:
        print("No seed data file found, skipping seed")
    
    cursor.close()
    return True

def verify_database(conn):
    """Verify database structure and data"""
    print("Verifying database...")
    
    cursor = conn.cursor()
    
    # Check tables exist
    tables = ['souls', 'tributes', 'financial_transactions', 'analytics_events', 'content_library']
    for table in tables:
        cursor.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s);",
            (table,)
        )
        exists = cursor.fetchone()[0]
        if exists:
            print(f"✓ Table {table} exists")
        else:
            print(f"✗ Table {table} missing")
            cursor.close()
            return False
    
    # Count records in each table
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} records")
    
    cursor.close()
    print("Database verification completed")
    return True

def main():
    """Main initialization function"""
    print("=" * 50)
    print("Tiapma'atzu Database Initialization")
    print("=" * 50)
    print(f"Database: {DB_CONFIG['dbname']}")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"Started: {datetime.now()}")
    print()
    
    # Connect to database
    conn = get_connection()
    print("✓ Connected to database")
    print()
    
    # Create tables
    if not create_tables(conn):
        print("Failed to create tables")
        conn.close()
        sys.exit(1)
    
    print()
    
    # Create indexes
    if not create_indexes(conn):
        print("Failed to create indexes")
        conn.close()
        sys.exit(1)
    
    print()
    
    # Seed initial data
    if not seed_initial_data(conn):
        print("Failed to seed data")
        conn.close()
        sys.exit(1)
    
    print()
    
    # Verify database
    if not verify_database(conn):
        print("Database verification failed")
        conn.close()
        sys.exit(1)
    
    # Close connection
    conn.close()
    
    print()
    print("=" * 50)
    print("Database initialization completed successfully")
    print("=" * 50)
    print(f"Completed: {datetime.now()}")

if __name__ == "__main__":
    main()