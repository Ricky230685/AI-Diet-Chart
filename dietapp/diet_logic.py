import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_ai_diet(age, gender, height, weight, goal):
    prompt = f"""
    Create a healthy one-day Indian diet plan.

    Age: {age}
    Gender: {gender}
    Height: {height} cm
    Weight: {weight} kg
    Goal: {goal}

    Give:
    Breakfast
    Lunch
    Evening Snack
    Dinner

    Keep the response short and practical.
    """

    response = model.generate_content(prompt)
    return response.text

# def generate_diet(goal, bmi):
#     if goal == "Weight Loss":
#         if bmi >= 25:
#             return [
#                 "🥣 Oats with Fruits",
#                 "🥗 Brown Rice + Dal + Salad",
#                 "🍎 Apple + Green Tea",
#                 "🍲 Vegetable Soup + Paneer"
#             ]
#         else:
#             return [
#                 "🥣 Oats",
#                 "🥗 Mixed Salad",
#                 "🍎 Seasonal Fruit",
#                 "🍲 Light Dinner"
#             ]

#     elif goal == "Weight Gain":
#         return [
#             "🥛 Milk + Banana Shake",
#             "🍛 Rice + Paneer + Vegetables",
#             "🥜 Dry Fruits",
#             "🍗 Protein-rich Dinner"
#         ]

#     else:
#         return [
#             "🥣 Balanced Breakfast",
#             "🍛 Healthy Lunch",
#             "🍎 Fresh Fruits",
#             "🍲 Balanced Dinner"
#         ]