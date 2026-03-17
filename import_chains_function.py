@app.route("/chains/import-excel", methods=["GET", "POST"])
@login_required
def import_chains_excel():
    """استيراد السلاسل من ملف Excel"""
    if current_user.role != "admin":
        flash(_("فقط المدير يمكنه استيراد السلاسل ❌"), "danger")
        return redirect(url_for("chains"))
    
    if request.method == "POST":
        if 'file' not in request.files:
            flash(_("الرجاء اختيار ملف Excel ❌"), "danger")
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash(_("الرجاء اختيار ملف Excel ❌"), "danger")
            return redirect(request.url)
        
        if file and allowed_upload_file(file.filename, {'xlsx', 'xls'}):
            try:
                # قراءة ملف Excel
                df = pd.read_excel(file)
                
                # استخراج العمود الأول (عمود A) - اسماء السلاسل
                if len(df.columns) == 0:
                    flash(_("الملف فارغ ❌"), "danger")
                    return redirect(request.url)
                
                # استخدام العمود الأول فقط
                first_column = df.columns[0]
                chain_names = df[first_column].tolist()
                
                # إزالة العنوان (الصف الأول) إذا كان "اسماء السلاسل"
                if chain_names and str(chain_names[0]).strip() in ["اسماء السلاسل", "اسم السلسلة"]:
                    chain_names = chain_names[1:]  # إزالة العنوان
                
                # استيراد السلاسل
                imported_count = 0
                errors = []
                
                for index, chain_name in enumerate(chain_names):
                    try:
                        chain_name = str(chain_name).strip()
                        
                        # تخطي القيم الفارغة أو NaN
                        if not chain_name or chain_name == 'nan':
                            continue
                        
                        # التحقق إذا كانت السلسلة موجودة
                        existing_chain = Chain.query.filter_by(name=chain_name).first()
                        if existing_chain:
                            errors.append(f"الصف {index + 2}: السلسلة '{chain_name}' موجودة بالفعل")
                            continue
                        
                        # إنشاء سلسلة جديدة
                        new_chain = Chain(name=chain_name)
                        db.session.add(new_chain)
                        imported_count += 1
                        
                    except Exception as e:
                        errors.append(f"الصف {index + 2}: خطأ في استيراد السلسلة - {str(e)}")
                
                # حفظ التغييرات
                if imported_count > 0:
                    db.session.commit()
                    flash(f"تم استيراد {imported_count} سلاسل بنجاح ✅", "success")
                else:
                    db.session.rollback()
                    flash("لم يتم استيراد أي سلاسل ⚠️", "warning")
                
                # عرض الأخطاء إذا وجدت
                if errors:
                    flash(f"أخطاء: {len(errors)} خطأ", "warning")
                    for error in errors[:5]:  # عرض أول 5 أخطاء فقط
                        flash(error, "warning")
                    if len(errors) > 5:
                        flash(f"... و {len(errors) - 5} أخطاء أخرى", "warning")
                
                return redirect(url_for("chains"))
                
            except Exception as e:
                flash(f"خطأ في قراءة ملف Excel: {str(e)} ❌", "danger")
                return redirect(request.url)
        else:
            flash(_("الرجاء رفع ملف Excel صالح (.xlsx, .xls) ❌"), "danger")
            return redirect(request.url)
    
    return render_template("import_chains_excel.html")
