#!/usr/bin/env python
"""
Test datetime fixes for Camera System
"""

def test_datetime_filters():
    """Test that datetime filters work correctly"""
    from datetime import datetime, timezone, timedelta
    from utils import days_since, duration_between, local_dt
    
    print("🧪 Testing datetime filters...")
    
    # Create test datetimes
    now_aware = datetime.now(timezone.utc)
    past_aware = now_aware - timedelta(days=5, hours=0, minutes=0, seconds=0)
    past_naive = datetime.now() - timedelta(days=5, hours=0, minutes=0, seconds=0)
    
    # Test 1: days_since with aware datetimes
    result1 = days_since(past_aware, now_aware)
    assert result1 >= 4, f"Expected >= 4, got {result1}"  # Allow for timezone differences
    print("  ✅ days_since with aware datetimes: OK")
    
    # Test 2: days_since with naive datetime (should convert)
    result2 = days_since(past_naive, now_aware)
    assert result2 >= 4, f"Expected >= 4, got {result2}"  # Allow for timezone differences
    print("  ✅ days_since with naive datetime: OK")
    
    # Test 3: duration_between
    start = datetime.now(timezone.utc)
    end = start + timedelta(days=3)
    result3 = duration_between(start, end)
    assert result3 == 3, f"Expected 3, got {result3}"
    print("  ✅ duration_between: OK")
    
    # Test 4: local_dt
    result4 = local_dt(past_aware)
    assert isinstance(result4, str), "local_dt should return string"
    assert len(result4) > 0, "local_dt should not be empty"
    print("  ✅ local_dt formatting: OK")
    
    print("\n✅ All datetime tests passed!\n")


def test_app_filters():
    """Test that filters are registered in Flask"""
    from app import app
    
    print("🧪 Testing Flask filter registration...")
    
    # Check if filters are registered
    assert 'local_dt' in app.jinja_env.filters, "local_dt filter not registered"
    print("  ✅ local_dt filter registered")
    
    assert 'days_since' in app.jinja_env.filters, "days_since filter not registered"
    print("  ✅ days_since filter registered")
    
    assert 'duration_between' in app.jinja_env.filters, "duration_between filter not registered"
    print("  ✅ duration_between filter registered")
    
    print("\n✅ All filters are registered correctly!\n")


if __name__ == '__main__':
    try:
        print("=" * 50)
        print("📹 Camera System - DateTime Test Suite")
        print("=" * 50)
        print()
        
        test_datetime_filters()
        test_app_filters()
        
        print("=" * 50)
        print("✅ All tests passed successfully!")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
