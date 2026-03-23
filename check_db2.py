from app import app, db, Branch

with app.app_context():
    # Check if there are any database constraints issues
    print('Checking database constraints...')
    
    # Get a sample branch
    branch = Branch.query.first()
    if branch:
        print(f'Sample branch ID: {branch.id}')
        print(f'Name: {branch.name}')
        print(f'Current data:')
        print(f'  location: "{branch.location}"')
        print(f'  phone_number: "{branch.phone_number}"')
        print(f'  phone_number_2: "{branch.phone_number_2}"')
        print(f'  phone_number_3: "{branch.phone_number_3}"')
        print(f'  phone_number_4: "{branch.phone_number_4}"')
        print(f'  ip_address: "{branch.ip_address}"')
        print(f'  nvr_count: {branch.nvr_count}')
        print(f'  branch_type: {branch.branch_type.encode("ascii", "ignore").decode()}')
        
        # Try to update with empty values
        try:
            branch.location = ''
            branch.phone_number = ''
            branch.phone_number_2 = ''
            branch.phone_number_3 = ''
            branch.phone_number_4 = ''
            branch.ip_address = ''
            branch.nvr_count = 0
            branch.branch_type = 'permanent'
            
            db.session.commit()
            print('Database update successful')
        except Exception as e:
            print(f'Database error: {e}')
            db.session.rollback()
    else:
        print('No branches found')
