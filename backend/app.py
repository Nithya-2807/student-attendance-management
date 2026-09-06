import os
import csv
from flask import Flask, render_template, request, redirect, url_for

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
STUDENT_FILE = os.path.join(DATA_DIR, "students.csv")
FACULTY_FILE = os.path.join(DATA_DIR, "faculty.csv")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- STUDENTS ----------------

@app.route("/students")
def students():

    students_list = []

    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students_list = list(reader)

    search = request.args.get("search", "").strip().lower()
    filter_dept = request.args.get("dept", "").strip()
    filter_section = request.args.get("section", "").strip()

    if search:
        students_list = [
            s for s in students_list
            if search in s["roll_no"].lower()
            or search in s["name"].lower()
        ]

    if filter_dept:
        students_list = [
            s for s in students_list
            if s["dept"] == filter_dept
        ]

    if filter_section:
        students_list = [
            s for s in students_list
            if s["section"] == filter_section
        ]

    return render_template(
        "students.html",
        students=students_list,
        search=search,
        filter_dept=filter_dept,
        filter_section=filter_section
    )


# ---------------- ADD STUDENT ----------------

@app.route("/students/add", methods=["POST"])
def add_student():

    roll_no = request.form["roll_no"].strip()
    name = request.form["name"].strip()
    dept = request.form["dept"].strip()
    section = request.form["section"].strip()

    os.makedirs(DATA_DIR, exist_ok=True)

    students_list = []

    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students_list = list(reader)

    # Prevent duplicate Roll No
    if any(s["roll_no"] == roll_no for s in students_list):
        return redirect(url_for("students"))

    file_exists = os.path.exists(STUDENT_FILE)

    with open(STUDENT_FILE, "a", newline="", encoding="utf-8") as file:

        fieldnames = ["roll_no", "name", "dept", "section"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "roll_no": roll_no,
            "name": name,
            "dept": dept,
            "section": section
        })

    return redirect(url_for("students"))


# ---------------- DELETE STUDENT ----------------

@app.route("/students/delete/<roll_no>", methods=["POST"])
def delete_student(roll_no):

    students_list = []

    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students_list = list(reader)

    students_list = [
        s for s in students_list
        if s["roll_no"] != roll_no
    ]

    with open(STUDENT_FILE, "w", newline="", encoding="utf-8") as file:

        fieldnames = ["roll_no", "name", "dept", "section"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(students_list)

    return redirect(url_for("students"))


# ---------------- EDIT STUDENT ----------------

@app.route("/students/edit/<roll_no>", methods=["GET", "POST"])
def edit_student(roll_no):
    students_list = []

    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students_list = list(reader)

    student = next(
        (s for s in students_list if s.get("roll_no", "").strip() == roll_no.strip()),
        None
    )

    if student is None:
        return redirect(url_for("students"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        dept = request.form.get("dept", "").strip()
        section = request.form.get("section", "").strip()

        if not name or not dept or not section:
            return render_template("edit_student.html", student=student, error="All fields are required.")

        student["name"] = name
        student["dept"] = dept
        student["section"] = section

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(STUDENT_FILE, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["roll_no", "name", "dept", "section"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students_list)

        return redirect(url_for("students"))

    return render_template("edit_student.html", student=student)


# ---------------- OTHER PAGES ----------------

# ---------------- FACULTY ----------------

@app.route("/faculty")
def faculty():

    faculty_list = []

    if os.path.exists(FACULTY_FILE):

        with open(
            FACULTY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)
            faculty_list = list(reader)

    search = request.args.get("search", "").strip().lower()

    if search:

        faculty_list = [
            faculty
            for faculty in faculty_list
            if search in faculty["faculty_id"].lower()
            or search in faculty["name"].lower()
        ]

    return render_template(
        "faculty.html",
        faculty=faculty_list,
        search=search
    )


# ---------------- ADD FACULTY ----------------

@app.route("/faculty/add", methods=["POST"])
def add_faculty():

    faculty_id = request.form["faculty_id"].strip()
    name = request.form["name"].strip()
    classes = request.form["classes"].strip()

    if not faculty_id or not name or not classes:
        return redirect(url_for("faculty"))

    os.makedirs(DATA_DIR, exist_ok=True)

    faculty_list = []

    if os.path.exists(FACULTY_FILE):

        with open(
            FACULTY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)
            faculty_list = list(reader)


    # Prevent duplicate Faculty ID

    if any(
        faculty["faculty_id"].lower() == faculty_id.lower()
        for faculty in faculty_list
    ):

        return redirect(url_for("faculty"))


    # Create CSV if it doesn't exist

    file_exists = os.path.exists(FACULTY_FILE)

    with open(
        FACULTY_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "faculty_id",
            "name",
            "classes"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists or os.path.getsize(FACULTY_FILE) == 0:
            writer.writeheader()

        writer.writerow({
            "faculty_id": faculty_id,
            "name": name,
            "classes": classes
        })


    return redirect(url_for("faculty"))


# ---------------- EDIT FACULTY ----------------

@app.route("/faculty/edit/<faculty_id>", methods=["GET", "POST"])
def edit_faculty(faculty_id):

    faculty_list = []

    if os.path.exists(FACULTY_FILE):

        with open(
            FACULTY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)
            faculty_list = list(reader)


    faculty_member = None

    for faculty in faculty_list:

        if faculty["faculty_id"] == faculty_id:

            faculty_member = faculty
            break


    if faculty_member is None:

        return redirect(url_for("faculty"))


    # Save edited data

    if request.method == "POST":

        faculty_member["name"] = request.form["name"].strip()

        faculty_member["classes"] = request.form["classes"].strip()


        with open(
            FACULTY_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            fieldnames = [
                "faculty_id",
                "name",
                "classes"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            writer.writerows(faculty_list)


        return redirect(url_for("faculty"))


    return render_template(
        "edit_faculty.html",
        faculty=faculty_member
    )


# ---------------- DELETE FACULTY ----------------

@app.route("/faculty/delete/<faculty_id>", methods=["POST"])
def delete_faculty(faculty_id):

    faculty_list = []

    if os.path.exists(FACULTY_FILE):

        with open(
            FACULTY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)
            faculty_list = list(reader)


    faculty_list = [
        faculty
        for faculty in faculty_list
        if faculty["faculty_id"] != faculty_id
    ]


    with open(
        FACULTY_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "faculty_id",
            "name",
            "classes"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(faculty_list)


    return redirect(url_for("faculty"))

# ---------------- CLASSES & TIMETABLE ----------------

CLASS_FILE = os.path.join(DATA_DIR, "classes.csv")
CLASS_FIELDS = ["date", "department", "section", "period", "class_type", "subject"]

DEPARTMENTS = ["CSE", "ECE", "CSM", "CSD", "IT", "CIVIL", "MECH", "EEE"]
SECTIONS = ["A", "B", "C", "D"]

def load_classes():
    if not os.path.exists(CLASS_FILE) or os.path.getsize(CLASS_FILE) == 0:
        return []
    with open(CLASS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            required = [row.get(k, "").strip() for k in CLASS_FIELDS]
            if not all(required[:4]):
                continue
            rows.append({k: row.get(k, "").strip() for k in CLASS_FIELDS})
        return rows

def save_classes(rows):
    os.makedirs(DATA_DIR, exist_ok=True)
    rows.sort(key=lambda x: (x.get("date", ""), x.get("department", ""), x.get("section", ""), int(x.get("period", "0"))))
    with open(CLASS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CLASS_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

@app.route("/classes")
def classes():
    selected_department = request.args.get("department", "").strip()
    selected_section = request.args.get("section", "").strip()
    selected_date = request.args.get("date", "").strip()
    classes_list = load_classes()
    date_classes = [c for c in classes_list if c["date"] == selected_date and c["department"] == selected_department and c["section"] == selected_section]
    timetable = []
    for period_number in range(1, 9):
        period_data = next((c for c in date_classes if c["period"] == str(period_number)), None)
        timetable.append(period_data or {"date": selected_date, "department": selected_department, "section": selected_section, "period": str(period_number), "class_type": "Not Configured", "subject": ""})
    return render_template("classes.html", timetable=timetable, departments=DEPARTMENTS, sections=SECTIONS, selected_department=selected_department, selected_section=selected_section, selected_date=selected_date)

@app.route("/classes/save", methods=["POST"])
def save_class():
    department = request.form.get("department", "").strip()
    section = request.form.get("section", "").strip()
    class_date = request.form.get("date", "").strip()
    period = request.form.get("period", "").strip()
    class_type = request.form.get("class_type", "").strip()
    subject = request.form.get("subject", "").strip()
    if not department or not section or not class_date or period not in [str(i) for i in range(1, 9)]:
        return redirect(url_for("classes", department=department, section=section, date=class_date))
    if class_type not in ["Regular", "Adjusted", "Leisure"]:
        return redirect(url_for("classes", department=department, section=section, date=class_date))
    if class_type == "Leisure":
        subject = ""
    elif not subject:
        return redirect(url_for("classes", department=department, section=section, date=class_date))
    classes_list = load_classes()
    updated = False
    for row in classes_list:
        if row["date"] == class_date and row["department"] == department and row["section"] == section and row["period"] == period:
            row.update({"class_type": class_type, "subject": subject})
            updated = True
            break
    if not updated:
        classes_list.append({"date": class_date, "department": department, "section": section, "period": period, "class_type": class_type, "subject": subject})
    save_classes(classes_list)
    return redirect(url_for("classes", department=department, section=section, date=class_date))

@app.route("/classes/delete/<department>/<section>/<date>/<period>", methods=["POST"])
def delete_class(department, section, date, period):
    classes_list = load_classes()
    classes_list = [row for row in classes_list if not (row["date"] == date and row["department"] == department and row["section"] == section and row["period"] == period)]
    save_classes(classes_list)
    return redirect(url_for("classes", department=department, section=section, date=date))

# ---------------- ATTENDANCE ----------------

DEPARTMENTS = ["CSE", "ECE", "CSM", "CSD", "IT", "CIVIL", "MECH", "EEE"]
SECTIONS = ["A", "B", "C", "D"]
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")


def _attendance_context(department, section, attendance_date, selected_periods, entries):
    students_list = []
    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            for student in csv.DictReader(file):
                if student.get("dept") == department and student.get("section") == section:
                    students_list.append(student)

    regular_periods = []
    period_subjects = {}
    for period in selected_periods:
        value = entries.get(str(period), "").strip()
        if value.lower() == "leisure" or value.lower() == "not conducted" or not value:
            continue
        regular_periods.append(str(period))
        period_subjects[str(period)] = value
    regular_periods.sort(key=int)

    return students_list, regular_periods, period_subjects


@app.route("/attendance")
def attendance():
    selected_department = request.args.get("department", "").strip()
    selected_section = request.args.get("section", "").strip()
    selected_date = request.args.get("date", "").strip()
    selected_periods = request.args.getlist("periods")

    # Show all eight periods with any previously saved class information.
    saved = {}
    for row in load_classes():
        if (row.get("date") == selected_date and
                row.get("department") == selected_department and
                row.get("section") == selected_section):
            period = row.get("period", "")
            if period:
                if row.get("class_type") == "Leisure":
                    saved[period] = "Leisure"
                elif row.get("class_type") == "Not Conducted":
                    saved[period] = "Not Conducted"
                else:
                    saved[period] = row.get("subject", "")

    period_entries = [
        {"period": str(i), "value": saved.get(str(i), "")}
        for i in range(1, 9)
    ]

    return render_template(
        "attendance.html",
        departments=DEPARTMENTS,
        sections=SECTIONS,
        period_entries=period_entries,
        students=[],
        regular_periods=[],
        period_subjects={},
        selected_department=selected_department,
        selected_section=selected_section,
        selected_date=selected_date,
        selected_periods=selected_periods,
        error=""
    )


@app.route("/attendance/setup", methods=["POST"])
def setup_attendance():
    department = request.form.get("department", "").strip()
    section = request.form.get("section", "").strip()
    attendance_date = request.form.get("date", "").strip()
    selected_periods = request.form.getlist("periods")

    if not department or not section or not attendance_date or not selected_periods:
        return redirect(url_for("attendance"))

    selected_periods = sorted(
        {p for p in selected_periods if p in [str(i) for i in range(1, 9)]},
        key=int
    )

    entries = {}
    for period in selected_periods:
        entries[period] = request.form.get(f"class_entry_{period}", "").strip()

    # Every selected period becomes a class record immediately.
    classes_list = load_classes()
    for period in selected_periods:
        raw = entries[period]
        lowered = raw.lower()
        if lowered == "leisure":
            class_type, subject = "Leisure", ""
        elif lowered == "not conducted":
            class_type, subject = "Not Conducted", ""
        elif raw:
            class_type, subject = "Regular", raw
        else:
            # A selected period without a description is not recorded as a class.
            continue

        existing = next((row for row in classes_list if
                         row["date"] == attendance_date and
                         row["department"] == department and
                         row["section"] == section and
                         row["period"] == period), None)
        data = {
            "date": attendance_date,
            "department": department,
            "section": section,
            "period": period,
            "class_type": class_type,
            "subject": subject
        }
        if existing:
            existing.update(data)
        else:
            classes_list.append(data)

    save_classes(classes_list)

    students_list, regular_periods, period_subjects = _attendance_context(
        department, section, attendance_date, selected_periods, entries
    )

    return render_template(
        "attendance.html",
        departments=DEPARTMENTS,
        sections=SECTIONS,
        period_entries=[{"period": str(i), "value": entries.get(str(i), "")} for i in range(1, 9)],
        students=students_list,
        regular_periods=regular_periods,
        period_subjects=period_subjects,
        selected_department=department,
        selected_section=section,
        selected_date=attendance_date,
        selected_periods=selected_periods,
        error=""
    )


@app.route("/attendance/mark", methods=["POST"])
def mark_attendance():
    department = request.form.get("department", "").strip()
    section = request.form.get("section", "").strip()
    attendance_date = request.form.get("date", "").strip()
    selected_periods = request.form.getlist("periods")

    if not department or not section or not attendance_date or not selected_periods:
        return redirect(url_for("attendance"))

    classes_list = load_classes()
    regular_periods = {
        row["period"] for row in classes_list
        if row.get("date") == attendance_date
        and row.get("department") == department
        and row.get("section") == section
        and row.get("class_type") == "Regular"
        and row.get("period") in selected_periods
    }

    students_list = []
    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            for student in csv.DictReader(file):
                if student.get("dept") == department and student.get("section") == section:
                    students_list.append(student)

    attendance_records = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r", newline="", encoding="utf-8") as file:
            attendance_records = list(csv.DictReader(file))

    for student in students_list:
        roll_no = student["roll_no"]
        for period in sorted(regular_periods, key=int):
            field_name = f"attendance_{roll_no}_{period}"
            status = request.form.get(field_name, "P")
            attendance_records = [
                record for record in attendance_records
                if not (record.get("roll_no") == roll_no
                        and record.get("date") == attendance_date
                        and record.get("period") == period)
            ]
            attendance_records.append({
                "roll_no": roll_no,
                "date": attendance_date,
                "period": period,
                "status": status
            })

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(ATTENDANCE_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["roll_no", "date", "period", "status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(attendance_records)

    return redirect(url_for(
        "attendance",
        department=department,
        section=section,
        date=attendance_date,
        periods=sorted(regular_periods, key=int)
    ))

# ---------------- REPORTS ----------------

@app.route("/reports")
def reports():

    selected_department = request.args.get(
        "department", ""
    ).strip()

    selected_section = request.args.get(
        "section", ""
    ).strip()

    selected_date = request.args.get(
        "date", ""
    ).strip()


    # ---------------- LOAD STUDENTS ----------------

    students_list = []

    if os.path.exists(STUDENT_FILE):

        with open(
            STUDENT_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)
            students_list = list(reader)


    # Apply department and section filters

    if selected_department:

        students_list = [
            student
            for student in students_list
            if student["dept"] == selected_department
        ]

    if selected_section:

        students_list = [
            student
            for student in students_list
            if student["section"] == selected_section
        ]


    # ---------------- LOAD ATTENDANCE ----------------

    attendance_records = []

    if os.path.exists(ATTENDANCE_FILE):

        with open(
            ATTENDANCE_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)
            attendance_records = list(reader)


    # ---------------- LOAD CLASSES ----------------

    classes_list = []

    if os.path.exists(CLASS_FILE):

        with open(
            CLASS_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)
            classes_list = list(reader)


    # Only Regular and Adjusted classes count.
    # Leisure and unrecorded periods are ignored.

    valid_periods = set()

    for class_data in classes_list:

        if class_data.get("class_type") in [
            "Regular",
            "Adjusted"
        ]:

            class_date = class_data.get("date", "")
            period = class_data.get("period", "")

            valid_periods.add(
                (class_date, class_data.get("department", ""), class_data.get("section", ""), period)
            )


    # ---------------- BUILD REPORT ----------------

    report = []

    for student in students_list:

        roll_no = student["roll_no"]

        period_status = {
            str(period): "-"
            for period in range(1, 9)
        }

        present = 0
        conducted = 0

        for record in attendance_records:

            if record["roll_no"] != roll_no:
                continue

            record_date = record["date"]
            record_period = record["period"]

            # If a date is selected, show only that date
            if selected_date and record_date != selected_date:
                continue

            # Only count classes configured as Regular/Adjusted
            if (record_date, student["dept"], student["section"], record_period) not in valid_periods:
                continue

            status = record["status"]

            if status == "P":
                present += 1
                conducted += 1

            elif status == "A":
                conducted += 1

            if record_date == selected_date or not selected_date:

                if record_period in period_status:
                    period_status[record_period] = status


        percentage = 0

        if conducted > 0:
            percentage = round(
                (present / conducted) * 100,
                2
            )


        if conducted == 0:
            attendance_status = "No Attendance"

        elif percentage < 75:
            attendance_status = "Low Attendance"

        else:
            attendance_status = "Good Attendance"


        report.append({

            "roll_no": roll_no,

            "name": student["name"],

            "dept": student["dept"],

            "section": student["section"],

            "period_status": period_status,

            "present": present,

            "conducted": conducted,

            "total": f"{present}/{conducted}",

            "percentage": percentage,

            "status": attendance_status

        })


    return render_template(
        "reports.html",

        report=report,

        departments=DEPARTMENTS,

        sections=SECTIONS,

        selected_department=selected_department,

        selected_section=selected_section,

        selected_date=selected_date
    )


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)