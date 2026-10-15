from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings

from .forms import ResumeForm
from .pdf_reader import extract_text_from_pdf
from .skill_matcher import calculate_match_score
from .pdf_report import create_ats_report

import os


def home(request):

    extracted_text = ""

    if request.method == "POST":

        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():

            resume = request.FILES["resume"]

            job_description = form.cleaned_data["job_description"]

            # PDF text extraction
            extracted_text = extract_text_from_pdf(resume)

            # ATS score calculation
            score, matched_skills, missing_skills = calculate_match_score(
                extracted_text,
                job_description
            )

            # Recommendations
            recommendations = []

            for skill in missing_skills:

                recommendations.append(
                    f"Consider learning or adding {skill} "
                    f"to improve your resume match."
                )

            if score >= 80:

                recommendations.append(
                    "Your resume has a strong match "
                    "with this job description."
                )

            elif score >= 60:

                recommendations.append(
                    "Your resume has a good match, "
                    "but adding missing skills can improve it."
                )

            else:

                recommendations.append(
                    "Consider improving your resume "
                    "with more job-relevant skills."
                )

            # Save analysis data in session
            request.session["score"] = score

            request.session["matched_skills"] = matched_skills

            request.session["missing_skills"] = missing_skills

            request.session["recommendations"] = recommendations

            # Save resume and job description to database
            form.save()

            return render(
                request,
                "index.html",
                {
                    "form": ResumeForm(),

                    "success": "Resume Uploaded Successfully!",

                    "text": extracted_text,

                    "score": score,

                    "matched_skills": matched_skills,

                    "missing_skills": missing_skills,

                    "recommendations": recommendations,
                }
            )

        else:

            print("FORM ERRORS:")
            print(form.errors)

    else:

        form = ResumeForm()

    return render(
        request,
        "index.html",
        {
            "form": form,

            "text": extracted_text,
        }
    )


def download_report(request):

    # Get analysis data from session
    score = request.session.get(
        "score",
        0
    )

    matched_skills = request.session.get(
        "matched_skills",
        []
    )

    missing_skills = request.session.get(
        "missing_skills",
        []
    )

    recommendations = request.session.get(
        "recommendations",
        []
    )

    # Create media folder if it does not exist
    os.makedirs(
        settings.MEDIA_ROOT,
        exist_ok=True
    )

    # PDF file path
    file_path = os.path.join(
        settings.MEDIA_ROOT,
        "ATS_Resume_Report.pdf"
    )

    # Create ATS PDF report
    create_ats_report(
        file_path,
        score,
        matched_skills,
        missing_skills,
        recommendations
    )

    # Download PDF
    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename="ATS_Resume_Report.pdf"
    )