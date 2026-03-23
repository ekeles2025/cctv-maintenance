@app.route("/branches/delete/<int:branch_id>", methods=["POST"])
@login_required
def delete_branch(branch_id):
    if current_user.role != "admin":
        flash(_("فقط المدير يمكنه حذف الفروع ❌"), "danger")
        return redirect(url_for("dashboard"))
    branch = Branch.query.get_or_404(branch_id)
    region_id = branch.region_id
    db.session.delete(branch)
    db.session.commit()
    flash("تم حذف الفرع بنجاح ✅", "success")
    return redirect(url_for("branches", region_id=region_id))

@app.route("/branches/import-excel/<int:region_id>", methods=["GET", "POST"])
@login_required
def import_branches_excel(region_id):
    """استيراد الفروع من ملف Excel"""
    if current_user.role != "admin":
        flash("فقط المدير يمكنه استيراد الفروع من Excel ❌", "danger")
        return redirect(url_for("dashboard"))
    
    region = Region.query.get_or_404(region_id)
    
    if request.method == "POST":
        if "excel_file" not in request.files:
            flash("لم يتم اختيار ملف ❌", "danger")
            return redirect(request.url)
        
        file = request.files["excel_file"]
        
        if file.filename == "":
            flash("لم يتم اختيار ملف ❌", "danger")
            return redirect(request.url)
        
        if not file.filename.endswith((".xlsx", ".xls")):
            flash("يجب أن يكون الملف من نوع Excel (.xlsx أو .xls) ❌", "danger")
            return redirect(request.url)
        
        try:
            # قراءة الملف
            file_bytes = file.read()
            workbook = load_workbook(io.BytesIO(file_bytes))
            worksheet = workbook.active
            
            branches_added = 0
            errors = []
            
            # القراءة من الصف الثاني (الصف الأول هو الرؤوس)
            for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    # تصفية الصف من القيم الفارغة و None
                    filtered_row = [cell for cell in row if cell is not None and str(cell).strip() != '']
                    
                    if len(filtered_row) < 2:
                        errors.append(f"الصف {row_idx}: بيانات ناقصة (يجب أن يحتوي على اسم الفرع والموقع على الأقل)")
                        continue
                    
                    # الأعمدة المتوقعة: اسم الفرع، الموقع، رقم التليفون، IP، عدد الكاميرات، عدد أجهزة NVR
                    branch_name = str(row[0]).strip() if len(row) > 0 and row[0] is not None else ''
                    location = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ''
                    
                    # التحقق من البيانات الأساسية
                    if not branch_name or not location:
                        errors.append(f"الصف {row_idx}: اسم الفرع والموقع إلزاميان")
                        continue
                    
                    # التحقق من وجود فرع بنفس الاسم في نفس المنطقة
                    existing_branch = Branch.query.filter_by(name=branch_name, region_id=region_id).first()
                    if existing_branch:
                        errors.append(f"الصف {row_idx}: فرع باسم '{branch_name}' موجود بالفعل في هذه المنطقة")
                        continue
                    
                    # القيم الاختيارية من الأعمدة الإضافية
                    phone_number = str(row[2]).strip() if len(row) > 2 and row[2] is not None else None
                    ip_address = str(row[3]).strip() if len(row) > 3 and row[3] is not None else None
                    camera_count = int(row[4]) if len(row) > 4 and row[4] is not None and str(row[4]).isdigit() else 0
                    nvr_count = int(row[5]) if len(row) > 5 and row[5] is not None and str(row[5]).isdigit() else 0
                    
                    # إنشاء الفرع الجديد
                    branch = Branch(
                        name=branch_name,
                        location=location,
                        region_id=region_id,
                        phone_number=phone_number,
                        ip_address=ip_address,
                        nvr_count=nvr_count
                    )
                    
                    db.session.add(branch)
                    branches_added += 1
                
                except Exception as e:
                    errors.append(f"الصف {row_idx}: {str(e)}")
                    logger.error(f"خطأ في الصف {row_idx}: {str(e)}")
            
            # حفظ التغييرات
            try:
                db.session.commit()
                flash(f"✅ تم إضافة {branches_added} فرع بنجاح من ملف Excel", "success")
                
                if errors:
                    logger.warning(f"أخطاء أثناء الاستيراد: {errors}")
                    flash(f"⚠️ هناك {len(errors)} أخطاء: " + " | ".join(errors[:3]), "warning")
                
                return redirect(url_for("branches", region_id=region_id))
            
            except Exception as e:
                db.session.rollback()
                logger.error(f"خطأ في حفظ البيانات: {str(e)}")
                flash(f"خطأ في حفظ البيانات: {str(e)} ❌", "danger")
                return redirect(request.url)
        
        except Exception as e:
            logger.error(f"خطأ في قراءة الملف: {str(e)}")
            flash(f"خطأ في قراءة الملف: {str(e)} ❌", "danger")
            return redirect(request.url)
    
    return redirect(url_for("branches", region_id=region_id))

@app.route("/cameras/<int:branch_id>")
@login_required
def cameras(branch_id):
    if current_user.role != "admin":
        flash(_("فقط المدير يمكنه الوصول لهذه الصفحة ❌"), "danger")
        return redirect(url_for("dashboard"))
    branch = Branch.query.get_or_404(branch_id)
    return render_template("cameras.html", cameras=branch.cameras, branch=branch)
