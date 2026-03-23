from app import app, db, Branch

with app.app_context():
    # Test the edit function
    print('Testing branch edit functionality...')
    
    # Get a sample branch
    branch = Branch.query.first()
    if branch:
        print(f'Sample branch: {branch.name}')
        print(f'Current phone: {branch.phone_number}')
        print(f'Current location: {branch.location}')
        
        # Test setting empty values
        branch.phone_number = ''
        branch.phone_number_2 = ''
        branch.phone_number_3 = ''
        branch.phone_number_4 = ''
        
        try:
            db.session.commit()
            print('Test successful - empty values saved')
        except Exception as e:
            print(f'Error: {e}')
            db.session.rollback()
    else:
        print('No branches found in database')
