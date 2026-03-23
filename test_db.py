#!/usr/bin/env python3
"""
Test database connection and data persistence
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Chain

def test_database():
    """Test database operations"""
    with app.app_context():
        print("Testing database connection...")
        
        # Test 1: Check if database file exists
        db_path = os.path.abspath('camera_system.db')
        print("Database path:", db_path)
        print("Database exists:", os.path.exists(db_path))
        
        # Test 2: Count existing chains
        existing_chains = Chain.query.count()
        print("Existing chains:", existing_chains)
        
        # Test 3: Add a test chain
        print("Adding test chain...")
        test_chain = Chain(name="Test Chain - " + str(os.urandom(4).hex()))
        db.session.add(test_chain)
        
        try:
            db.session.commit()
            print("Successfully added chain with ID:", test_chain.id)
        except Exception as e:
            print("Error adding chain:", e)
            db.session.rollback()
            return
        
        # Test 4: Verify chain exists
        chains_after = Chain.query.count()
        print("Chains after adding:", chains_after)
        
        # Test 5: Query the test chain
        retrieved_chain = Chain.query.filter_by(name=test_chain.name).first()
        if retrieved_chain:
            print("Successfully retrieved chain:", retrieved_chain.name, "(ID:", retrieved_chain.id, ")")
        else:
            print("Could not retrieve the test chain!")
        
        # Test 6: Delete test chain
        print("Deleting test chain...")
        db.session.delete(retrieved_chain)
        db.session.commit()
        
        final_chains = Chain.query.count()
        print("Final chains count:", final_chains)
        
        print("Database test completed!")

if __name__ == "__main__":
    test_database()
