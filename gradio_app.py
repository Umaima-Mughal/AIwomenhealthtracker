import gradio as gr
from datetime import datetime
from modules.medical_chatbot import generate_response
from modules.symptom_checker import symptoms_checker_ui
from modules.cycle_tracker import menstrual_cycle_tracker
from modules.pregnancy_tracker import pregnancy_analysis
from modules.pcos_checker import prepare_input
from modules.pcos_checker import predict_pcos
from modules.pcos_checker import bmi_category
from modules.pcos_checker import pcos_risk_checker


# =========================
# Chatbot Function
# =========================

def chatbot_response(question):

    if not question.strip():
        return "Please enter a question."

    return generate_response(question)



# =========================
# PCOS Function
# =========================
def pcos_checker_ui(
    age,
    weight,
    height,
    cycle,
    cycle_length,
    weight_gain,
    hair_growth,
    skin_darkening,
    hair_loss,
    pimples,
    fast_food,
    exercise
):

    # Convert YES / NO to 1 / 0
    cycle = 1 if cycle == "YES" else 0
    weight_gain = 1 if weight_gain == "YES" else 0
    hair_growth = 1 if hair_growth == "YES" else 0
    skin_darkening = 1 if skin_darkening == "YES" else 0
    hair_loss = 1 if hair_loss == "YES" else 0
    pimples = 1 if pimples == "YES" else 0
    fast_food = 1 if fast_food == "YES" else 0
    exercise = 1 if exercise == "YES" else 0

    return pcos_risk_checker(
        int(age),
        float(weight),
        float(height),
        cycle,
        int(cycle_length),
        weight_gain,
        hair_growth,
        skin_darkening,
        hair_loss,
        pimples,
        fast_food,
        exercise
    )

# =========================
# Pregnancy Function
# =========================

def pregnancy_tracker_ui(date):

    try:

        lmp_date = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()


        return pregnancy_analysis(lmp_date)


    except:

        return "Please enter date format YYYY-MM-DD"



# =========================
# Cycle Tracker UI
# =========================

def cycle_tracker_ui(last_period, cycle_length, duration):

    from datetime import datetime, timedelta


    try:

        last_date = datetime.strptime(
            last_period,
            "%Y-%m-%d"
        )


        next_period = last_date + timedelta(
            days=int(cycle_length)
        )


        today = datetime.today()

        cycle_day = (
            today - last_date
        ).days + 1


        if cycle_day <= int(duration):
            phase = "Menstrual Phase"

        elif cycle_day <= 14:
            phase = "Follicular Phase"

        elif cycle_day <= 16:
            phase = "Ovulation Phase"

        else:
            phase = "Luteal Phase"


        result=f"""
Menstrual Cycle Tracker


Last Period:
{last_date.date()}


Expected Next Period:
{next_period.date()}


Current Cycle Day:
{cycle_day}


Current Phase:
{phase}


Cycle Insight:
"""

        if 21 <= int(cycle_length) <=35:
            result += "✓ Cycle length is within normal range."
        else:
            result += "⚠ Cycle may be irregular."


        return result


    except:

        return "Please enter correct date format YYYY-MM-DD"



# =========================
# Gradio Interface
# =========================


with gr.Blocks(title="AI Women's Health Tracker") as demo:


    gr.Markdown(
    """
    # 🌸 AI Women's Health Tracker

    AI based women's health assistant for:
    - Menstrual health
    - PCOS risk assessment
    - Pregnancy tracking
    - Symptom information

    ⚠ This tool provides educational information only.
    """
    )


    # CHATBOT TAB

    with gr.Tab("🤖 AI Health Chatbot"):

        question = gr.Textbox(
            label="Ask your health question"
        )

        chat_output = gr.Textbox(
            label="AI Response",
            lines=8
        )


        ask = gr.Button(
            "Ask"
        )


        ask.click(
            chatbot_response,
            inputs=question,
            outputs=chat_output
        )



    # PCOS TAB

    with gr.Tab("🧪 PCOS Risk Checker"):
        gr.Markdown(
            "Fill in the following information to estimate your PCOS risk."
        )

        age = gr.Number(
            label="Age (20-48 years)"
        )

        weight = gr.Number(
            label="Weight (kg)"
        )

        height = gr.Number(
            label="Height (cm)"
        )

        cycle = gr.Radio(
            ["YES", "NO"],
            label="Irregular Menstrual Cycle?",
            # info="1 = Yes, 0 = No"
        )

        cycle_length = gr.Number(
            label="Average Cycle Length (days)"
        )

        weight_gain = gr.Radio(
            ["YES", "NO"],
            label="Recent Weight Gain?",
            # info="1 = Yes, 0 = No"
        )

        hair_growth = gr.Radio(
            ["YES", "NO"],
            label="Excess Facial / Body Hair?",
            # info="1 = Yes, 0 = No"
        )

        skin_darkening = gr.Radio(
            ["YES", "NO"],
            label="Skin Darkening?",
            # info="1 = Yes, 0 = No"
        )

        hair_loss = gr.Radio(
            ["YES", "NO"],
            label="Hair Loss?",
            # info="1 = Yes, 0 = No"
        )

        pimples = gr.Radio(
            ["YES", "NO"],
            label="Frequent Pimples?",
            # info="1 = Yes, 0 = No"
        )

        fast_food = gr.Radio(
            ["YES", "NO"],
            label="Frequent Fast Food?",
            # info="1 = Yes, 0 = No"
        )

        exercise = gr.Radio(
            ["YES", "NO"],
            label="Regular Exercise?",
            # info="1 = Yes, 0 = No"
        )
        pcos_output = gr.Textbox(
            label="Assessment Result",
            lines=25
        )

        btn = gr.Button(
            "Check PCOS Risk"
        )

        btn.click(
            pcos_checker_ui,
            inputs=[
                age,
                weight,
                height,
                cycle,
                cycle_length,
                weight_gain,
                hair_growth,
                skin_darkening,
                hair_loss,
                pimples,
                fast_food,
                exercise
            ],
            outputs=pcos_output
        )
    # SYMPTOM TAB

    with gr.Tab("🔎 Symptom Checker"):

        symptoms = gr.Textbox(
            label="Enter symptoms"
        )

        symptom_output = gr.Textbox(
            lines=6
        )


        check = gr.Button(
            "Analyze Symptoms"
        )


        check.click(
            symptoms_checker_ui,
            inputs=symptoms,
            outputs=symptom_output
        )



    # PREGNANCY TAB

    with gr.Tab("🤰 Pregnancy Tracker"):

        lmp = gr.Textbox(
            label="Last Menstrual Period (YYYY-MM-DD)"
        )


        pregnancy_output = gr.Textbox(
            lines=12
        )


        pregnancy_btn = gr.Button(
            "Track Pregnancy"
        )


        pregnancy_btn.click(
            pregnancy_tracker_ui,
            inputs=lmp,
            outputs=pregnancy_output
        )



    # CYCLE TAB

    with gr.Tab("🩸 Cycle Tracker"):


        last_period = gr.Textbox(
            label="Last Period Date YYYY-MM-DD"
        )


        cycle_length = gr.Number(
            label="Cycle Length"
        )


        duration = gr.Number(
            label="Period Duration"
        )


        cycle_output = gr.Textbox(
            lines=8
        )


        cycle_btn = gr.Button(
            "Track Cycle"
        )


        cycle_btn.click(
            cycle_tracker_ui,
            inputs=[
                last_period,
                cycle_length,
                duration
            ],
            outputs=cycle_output
        )



# Launch

demo.launch(
    share=True
)