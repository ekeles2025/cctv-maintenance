import pandas as pd
import os

# إنشاء ملف مثال لاستيراد السلاسل
def create_chains_example():
    """إنشاء ملف Excel مثال لاستيراد السلاسل"""
    data = [
        {'اسم السلسلة': 'السلسلة الرئيسية'},
        {'اسم السلسلة': 'سلسلة المطاعم'},
        {'اسم السلسلة': 'سلسلة المحلات'},
        {'اسم السلسلة': 'سلسلة الفنادق'},
        {'اسم السلسلة': 'سلسلة المدارس'},
        {'اسم السلسلة': 'سلسلة المستشفيات'},
    ]
    
    df = pd.DataFrame(data)
    
    # حفظ الملف
    output_path = os.path.join(os.path.dirname(__file__), 'example_chains_import.xlsx')
    df.to_excel(output_path, index=False, engine='openpyxl')
    
    print("Example file created successfully!")
    return output_path

if __name__ == "__main__":
    create_chains_example()
