# استبدل دالة import_excel بالكامل بهذه النسخة المصححة

@app.route("/faults/import-excel", methods=["GET", "POST"])
@login_required
def import_excel_faults():
    """استيراد الأعطال من ملف Excel"""
    if current_user.role != "admin":
        flash("فقط المدير يمكنه استيراد الأعطال من Excel ❌", "danger")
        return redirect(url_for("dashboard"))
    
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
            
            faults_added = 0
            errors = []
            seasonal_branches_to_confirm = []
            seasonal_faults_data = []
            
            # القراءة من الصف الثاني (الصف الأول هو الرؤوس)
            for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    # تصفية الصف من القيم الفارغة و None
                    filtered_row = [cell for cell in row if cell is not None and str(cell).strip() != '']
                    
                    # التحقق من طول الصف بعد التصفية - يتطلب 3 أعمدة فقط
                    if len(filtered_row) < 3:
                        errors.append(f"الصف {row_idx}: بيانات ناقصة (يجب أن يحتوي على 3 أعمدة: Name, Address, Network Status)")
                        continue
                    
                    # الأعمدة المتوقعة (3 أعمدة فقط): Name, Address, Network Status
                    camera_name = str(row[0]).strip() if len(row) > 0 and row[0] is not None else ''
                    address = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ''
                    network_status = str(row[2]).strip() if len(row) > 2 and row[2] is not None else ''
                    
                    # القيم الاختيارية من الأعمدة الإضافية
                    reported_by = str(row[3]).strip() if len(row) > 3 and row[3] is not None else ''
                    technician_name = str(row[4]).strip() if len(row) > 4 and row[4] is not None and str(row[4]).strip() != '' else None
                    
                    # التحقق من البيانات الأساسية
                    if not camera_name or not address or not network_status:
                        errors.append(f"الصف {row_idx}: بيانات ناقصة (Name, Address, Network Status إلزامية)")
                        continue
                    
                    # تحويل Network Status إلى fault_type
                    if network_status.lower() in ['offline', 'معطلة', 'disconnected']:
                        fault_type = 'offline'
                    elif network_status.lower() in ['online', 'متاحة', 'connected']:
                        fault_type = 'online'
                    else:
                        fault_type = 'unknown'
                    
                    # البحث عن الكاميرا
                    camera = Camera.query.filter_by(name=camera_name).first()
                    if not camera:
                        errors.append(f"الصف {row_idx}: لم يتم العثور على كاميرا باسم '{camera_name}'")
                        continue
                    
                    # البحث عن الفني إن وجد
                    technician_id = None
                    if technician_name:
                        technician = User.query.filter_by(username=technician_name, role="technician").first()
                        if not technician:
                            errors.append(f"الصف {row_idx}: لم يتم العثور على فني باسم '{technician_name}'")
                            continue
                        technician_id = technician.id
                    
                    # إنشاء العطل إذا كانت الكاميرا معطلة
                    if fault_type == 'offline':
                        # التحقق من نوع الفرع قبل إضافة العطل
                        if camera.branch and camera.branch.branch_type == 'موسمي':
                            # الفرع موسمي - تخزين بيانات للتأكيد
                            seasonal_fault_data = {
                                'row_idx': row_idx,
                                'camera_name': camera_name,
                                'branch_name': camera.branch.name,
                                'address': address,
                                'reported_by': reported_by,
                                'technician_id': technician_id
                            }
                            seasonal_faults_data.append(seasonal_fault_data)
                            if camera.branch.name not in seasonal_branches_to_confirm:
                                seasonal_branches_to_confirm.append(camera.branch.name)
                            continue
                        
                        # التحقق من وجود عطل مفتوح لنفس الكاميرا
                        existing_fault = Fault.query.filter_by(
                            camera_id=camera.id,
                            resolved_at=None
                        ).first()
                        
                        if not existing_fault:
                            fault = Fault(
                                description=f'Camera {camera_name} is offline - Address: {address}',
                                fault_type='offline',
                                device_type='Camera',
                                reported_by=reported_by,
                                camera_id=camera.id,
                                technician_id=technician_id,
                                date_reported=utc_now(),
                                expires_at=utc_now() + timedelta(days=7)
                            )
                            db.session.add(fault)
                            faults_added += 1
                
                except Exception as e:
                    errors.append(f"الصف {row_idx}: {str(e)}")
                    logger.error(f"خطأ في الصف {row_idx}: {str(e)}")
            
            # حفظ التغييرات
            try:
                # إذا كان هناك فروع موسمية، عرض صفحة التأكيد
                if seasonal_branches_to_confirm:
                    # تخزين بيانات الأعطال في الجلسة للاستخدام لاحقاً
                    session['seasonal_faults_data'] = seasonal_faults_data
                    session['seasonal_branches_to_confirm'] = seasonal_branches_to_confirm
                    session['regular_faults_added'] = faults_added
                    session['excel_errors'] = errors
                    
                    # عرض صفحة التأكيد
                    return render_template("confirm_seasonal_faults.html", 
                                         seasonal_branches=seasonal_branches_to_confirm,
                                         seasonal_faults=seasonal_faults_data,
                                         regular_faults_added=faults_added,
                                         errors=errors)
                
                db.session.commit()
                flash(f"✅ تم إضافة {faults_added} عطل بنجاح من ملف Excel", "success")
                
                if errors:
                    logger.warning(f"أخطاء أثناء الاستيراد: {errors}")
                    flash(f"⚠️ هناك {len(errors)} أخطاء: " + " | ".join(errors[:3]), "warning")
                
                return redirect(url_for("all_faults"))
            
            except Exception as e:
                db.session.rollback()
                logger.error(f"خطأ في حفظ البيانات: {str(e)}")
                flash(f"خطأ في حفظ البيانات: {str(e)} ❌", "danger")
                return redirect(request.url)
        
        except Exception as e:
            logger.error(f"خطأ في قراءة الملف: {str(e)}")
            flash(f"خطأ في قراءة الملف: {str(e)} ❌", "danger")
            return redirect(request.url)
    
    return render_template("import_excel.html")
