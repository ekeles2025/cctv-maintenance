#!/usr/bin/env python3
"""
Script to review and fix seasonal branches according to new rules:
- Only branches in "North Coast" regions should be seasonal
- All other branches should be permanent
"""

import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set up environment
os.environ['DATABASE_URL'] = 'sqlite:///camera_system.db'

from app import db, Branch, Region, app

def review_and_fix_seasonal_branches():
    """Review all branches and fix seasonal branches outside North Coast regions"""

    print("🔍 مراجعة جميع الفروع والمناطق...")
    print("=" * 60)

    with app.app_context():
        # Get all branches with their regions
        branches = Branch.query.options(
            db.joinedload(Branch.region).joinedload(Region.chain)
        ).all()

        print(f"📊 إجمالي الفروع في النظام: {len(branches)}")
        print()

        # Categorize branches
        seasonal_branches = []
        permanent_branches = []
        north_coast_seasonal = []
        non_north_coast_seasonal = []

        for branch in branches:
            region_name = branch.region.name if branch.region else "بدون منطقة"
            chain_name = branch.region.chain.name if branch.region and branch.region.chain else "بدون سلسلة"

            if branch.branch_type in ['موسمي', 'seasonal']:
                seasonal_branches.append(branch)

                if branch.region and 'North Coast' in branch.region.name:
                    north_coast_seasonal.append(branch)
                    print(f"✅ موسمي صحيح - {branch.name} (منطقة: {region_name}, سلسلة: {chain_name})")
                else:
                    non_north_coast_seasonal.append(branch)
                    print(f"❌ موسمي خطأ - {branch.name} (منطقة: {region_name}, سلسلة: {chain_name})")
            else:
                permanent_branches.append(branch)

        print()
        print("=" * 60)
        print("📈 إحصائيات:")
        print(f"  • إجمالي الفروع: {len(branches)}")
        print(f"  • فروع دائمة: {len(permanent_branches)}")
        print(f"  • فروع موسمية: {len(seasonal_branches)}")
        print(f"  • موسمية صحيحة (North Coast): {len(north_coast_seasonal)}")
        print(f"  • موسمية خطأ (خارج North Coast): {len(non_north_coast_seasonal)}")
        print()

        if non_north_coast_seasonal:
            print("🔧 سيتم تغيير الفروع التالية من موسمية إلى دائمة:")
            print("-" * 60)

            for branch in non_north_coast_seasonal:
                region_name = branch.region.name if branch.region else "بدون منطقة"
                chain_name = branch.region.chain.name if branch.region and branch.region.chain else "بدون سلسلة"

                print(f"  • {branch.name} (منطقة: {region_name}, سلسلة: {chain_name})")

                # Change branch type to permanent
                branch.branch_type = 'دائم'
                print("    ✓ تم التغيير إلى دائم"            print()

            # Commit changes
            try:
                db.session.commit()
                print("✅ تم حفظ جميع التغييرات بنجاح!")
                print(f"   تم تغيير {len(non_north_coast_seasonal)} فرع من موسمي إلى دائم")
            except Exception as e:
                db.session.rollback()
                print(f"❌ خطأ في حفظ التغييرات: {e}")
                return False

        else:
            print("✅ لا توجد فروع موسمية خارج مناطق North Coast")

        print()
        print("=" * 60)
        print("🏁 تم الانتهاء من مراجعة النظام")
        return True

if __name__ == "__main__":
    print("🚀 بدء مراجعة وإصلاح الفروع الموسمية...")
    print()

    try:
        success = review_and_fix_seasonal_branches()
        if success:
            print()
            print("🎉 تم تنفيذ المهمة بنجاح!")
        else:
            print()
            print("💥 فشلت المهمة!")
            sys.exit(1)

    except Exception as e:
        print(f"💥 خطأ غير متوقع: {e}")
        sys.exit(1)
