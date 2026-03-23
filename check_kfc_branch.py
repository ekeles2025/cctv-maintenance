from app import db, Branch, Region, app

with app.app_context():
    branch = Branch.query.filter(Branch.name.like('%KFC 10th of Ramadan%')).first()
    if branch:
        region_name = branch.region.name if branch.region else 'No region'
        chain_name = branch.region.chain.name if branch.region and branch.region.chain else 'No chain'
        
        print('Direct check from database:')
        print('=' * 50)
        print(f'Branch: {branch.name}')
        print(f'Type in database: {branch.branch_type.encode("ascii", "ignore").decode()}')
        print(f'Region: {region_name}')
        print(f'Chain: {chain_name}')
        print(f'North Coast in region: {"North Coast" in region_name}')
        print()
        
        # Check for both Arabic and English seasonal types
        is_seasonal = branch.branch_type in ['seasonal', 'موسمي']
        if is_seasonal and 'North Coast' not in region_name:
            print('PROBLEM: seasonal branch outside North Coast')
            print('Fixing...')
            branch.branch_type = 'دائم'
            db.session.commit()
            print('Fixed')
            print(f'New type: {branch.branch_type.encode("ascii", "ignore").decode()}')
        elif is_seasonal and 'North Coast' in region_name:
            print('CORRECT: seasonal branch in North Coast region')
        else:
            print('CORRECT: permanent branch')
    else:
        print('Branch not found')
        
        kfc_branches = Branch.query.filter(Branch.name.like('%KFC%')).all()
        print(f'Found {len(kfc_branches)} KFC branches:')
        for b in kfc_branches:
            region_name = b.region.name if b.region else 'No region'
            print(f'  - {b.name} (type: {b.branch_type.encode("ascii", "ignore").decode()}, region: {region_name})')
