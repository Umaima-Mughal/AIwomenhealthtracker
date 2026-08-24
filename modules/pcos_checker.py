# ML MODEL INTEGRATION
import joblib
import pandas as pd
from pathlib import Path
MODEL_PATH = Path(__file__).parent.parent / "models" / "pcos_model.pkl"

model = joblib.load(MODEL_PATH)

print("✅ PCOS Model Loaded Successfully!")

def predict_pcos(sample):

    prediction = model.predict(sample)

    probability = model.predict_proba(sample)

    confidence = round(
        probability[0][prediction[0]] * 100,
        2
    )

    return {
        "prediction": "PCOS Likely" if prediction[0] == 1 else "PCOS Unlikely",
        "value": int(prediction[0]),
        "confidence": confidence
    }
def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    return "Obese"

def generate_explanation(prediction, answers):

        reasons = []
        if answers["Cycle(R/I)"] in (1, 4):   #cv
            reasons.append("Irregular menstrual cycle")

        if answers["Weight gain(Y/N)"] == 1:
            reasons.append("Recent weight gain")

        if answers["hair growth(Y/N)"] == 1:
            reasons.append("Excess facial/body hair")

        if answers["Skin darkening (Y/N)"] == 1:
            reasons.append("skin darkening")

        if answers["Hair loss(Y/N)"] == 1:
            reasons.append("Hair loss")

        if answers["Pimples(Y/N)"] == 1:
            reasons.append("Frequent pimples")

        bmi = answers["BMI"]

        if bmi >= 25:
            reasons.append("BMI is above normal")

        result = ""

        result += "===================================\n"
        result += "PCOS Assessment Result\n"
        result += "===================================\n\n"
        if prediction["value"] == 1:
            result += "## 🔴 PCOS Likely\n\n"

        else:
            result += "## 💚 PCOS Unlikely\n\n"
        result += "⚠ This AI tool is intended for educational purposes only.\n"
        result += "It cannot replace professional medical diagnosis.\n\n"
        confidence = prediction["confidence"]
        if confidence >= 85:
            risk = "High"

        elif confidence >= 60:
            risk = "Moderate"

        else:
            risk = "Low"


        if risk == "High":
            result += "### 🔴 Risk Level: HIGH\n\n"

        elif risk == "Moderate":
            result += "### 🟠 Risk Level: MODERATE\n\n"

        else:
            result += "### 🟢 Risk Level: LOW\n\n"
        result += f"**Confidence:** {confidence}%\n\n"
        result += "This reflects how confident the model is in its prediction based on patterns learned from the training data.\n\n"
        result += f"BMI: {bmi:.1f} ({bmi_category(bmi)})\n\n"

        if prediction["value"] == 1:

            result += "Possible reasons:\n\n"

            if reasons:

                for reason in reasons:
                    result += f"✔ {reason}\n"

            else:

                result += "No major symptom identified from questionnaire.\n"

            result += "\nRecommendation:\n"

            if answers["Fast food (Y/N)"] == 1:
                result += "• Try to reduce fast food consumption.\n"

            if answers["Reg.Exercise(Y/N)"] == 0:
                result += "• Aim for at least 30 minutes of physical activity most days.\n"

            if answers["Weight gain(Y/N)"] == 1:
                result += "• Monitor your weight and discuss healthy weight management with a healthcare professional.\n"

            if answers["Cycle(R/I)"] == 1:
                result += "• Keep a menstrual cycle record to discuss with your doctor.\n"

            if answers["Skin darkening (Y/N)"] == 1:
                result += "• Skin darkening may indicate insulin resistance.\n"

            result += "• This AI assessment is not a medical diagnosis.\n"
        else:
            result += "Some symptoms associated with PCOS were reported.\n"
            if reasons:

                result += "\nSymptoms you reported:\n\n"

                for reason in reasons:
                    result += f"✔ {reason}\n"

                result += "\n"
            result += "However, based on the overall pattern learned by the AI model,\n"
            result += "your current responses were classified as PCOS Unlikely.\n\n"

            result += "Recommendation:\n"
            result += "• Monitor your menstrual cycle.\n"
            result += "• Maintain a healthy lifestyle.\n"
            result += "• Consult a doctor if symptoms continue.\n"
            result += "• This AI assessment does not replace medical diagnosis.\n"
        return result
def prepare_input(
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
    bmi = round(
        weight / ((height / 100) ** 2),
        2
    )
    cycle_for_model = 4 if cycle == 1 else 2 if cycle == 0 else cycle  # cv

    answers = {" Age (yrs)": age,

               "Weight (Kg)": weight,

               "Height(Cm) ": height,

               "BMI": bmi,

               "Cycle(R/I)": cycle_for_model,

            "Cycle length(days)": cycle_length,

            "Weight gain(Y/N)": weight_gain,

            "hair growth(Y/N)": hair_growth,

            "Skin darkening (Y/N)": skin_darkening,

            "Hair loss(Y/N)": hair_loss,

            "Pimples(Y/N)": pimples,

            "Fast food (Y/N)": fast_food,

            "Reg.Exercise(Y/N)": exercise
        }
    sample = pd.DataFrame([answers])
    return sample, answers

def pcos_risk_checker(
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
    sample, answers = prepare_input(
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
    )
    prediction = predict_pcos(sample)
    result = generate_explanation(
        prediction,
        answers
    )
    return result

