from app import db, Branch, Region, app

with app.app_context():
    # Get all seasonal branches outside North Coast
    seasonal_branches = Branch.query.join(Region).filter(
        Branch.branch_type.in_(['موسمي', 'seasonal']),
        ~Region.name.like('%North Coast%')
    ).all()
    
    print(f'Found {len(seasonal_branches)} seasonal branches outside North Coast:')
    print('=' * 60)
    
    for branch in seasonal_branches:
        region_name = branch.region.name if branch.region else 'No region'
        chain_name = branch.region.chain.name if branch.region and branch.region.chain else 'No chain'
        
        print(f'Branch: {branch.name}')
        print(f'Region: {region_name}')
        print(f'Chain: {chain_name}')
        print(f'Current type: {branch.branch_type.encode("ascii", "ignore").decode()}')
        print('Changing to permanent...')
        
        branch.branch_type = 'دائم'
        print('Changed successfully')
        print('-' * 40)
    
    # Commit all changes
    if seasonal_branches:
        try:
            db.session.commit()
            print(f'Successfully changed {len(seasonal_branches)} branches to permanent')
        except Exception as e:
            db.session.rollback()
            print(f'Error: {e}')
    else:
        print('No seasonal branches found outside North Coast')
