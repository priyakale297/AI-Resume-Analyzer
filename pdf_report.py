from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


def create_ats_report(
    file_path,
    score,
    matched_skills,
    missing_skills,
    recommendations
):

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    content = []

    # Title
    content.append(
        Paragraph(
            "AI Resume Analyzer",
            title_style
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "ATS Resume Analysis Report",
            heading_style
        )
    )

    content.append(Spacer(1, 15))

    # ATS Score
    content.append(
        Paragraph(
            f"<b>ATS Match Score: {score}%</b>",
            normal_style
        )
    )

    content.append(Spacer(1, 15))

    # Matched Skills
    content.append(
        Paragraph(
            "Matched Skills",
            heading_style
        )
    )

    if matched_skills:
        content.append(
            Paragraph(
                ", ".join(matched_skills),
                normal_style
            )
        )
    else:
        content.append(
            Paragraph(
                "No matching skills found.",
                normal_style
            )
        )

    content.append(Spacer(1, 15))

    # Missing Skills
    content.append(
        Paragraph(
            "Missing Skills",
            heading_style
        )
    )

    if missing_skills:
        content.append(
            Paragraph(
                ", ".join(missing_skills),
                normal_style
            )
        )
    else:
        content.append(
            Paragraph(
                "No missing skills.",
                normal_style
            )
        )

    content.append(Spacer(1, 15))

    # Recommendations
    content.append(
        Paragraph(
            "Resume Recommendations",
            heading_style
        )
    )

    for recommendation in recommendations:
        content.append(
            Paragraph(
                "• " + recommendation,
                normal_style
            )
        )

        content.append(Spacer(1, 5))

    content.append(Spacer(1, 20))

    # Summary Table
    data = [
        ["Category", "Result"],
        ["ATS Score", f"{score}%"],
        ["Matched Skills", str(len(matched_skills))],
        ["Missing Skills", str(len(missing_skills))]
    ]

    table = Table(
        data,
        colWidths=[200, 200]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 8),
        ])
    )

    content.append(table)

    document.build(content)