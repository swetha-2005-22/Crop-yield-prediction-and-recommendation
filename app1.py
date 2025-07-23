from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the model
model1 = pickle.load(open('model/agriculture.pkl', 'rb'))

app = Flask(__name__)  # initializing Flask app

# Crop recommendation dictionary (you can expand this)
# Crop recommendation dictionary with added maintenance and cultivation details
# Expanded crop recommendation dictionary with detailed content
crop_recommendations = {
    "rice": {
        "fertilizer": "Apply Urea at 60-80 kg per acre during the vegetative stage, followed by Ammonium Sulfate during the tillering stage. Potassium can be applied at the booting stage to enhance grain filling.",
        "irrigation": "Flood irrigation is most effective for rice. Maintain a water depth of 2-5 cm in the early stages and 5-7 cm during active growth. Drain excess water during maturity to avoid waterlogging.",
        "maintenance": "Ensure regular weeding, especially in the first 40 days, as rice is sensitive to weed competition. Manage pests like rice stem borers and diseases like leaf blight through biological control and timely pesticide application.",
        "cultivation": "Cultivate in clayey soil with proper leveling for uniform water distribution. Ideal planting depth is 2-3 cm. Cultivate in regions with average temperatures of 25-30°C and an annual rainfall of 100-150 cm."
    },
    "Soyabeans": {
        "fertilizer": "Apply Phosphorus (40-60 kg/ha) at sowing to promote root development. Potash (30-40 kg/ha) should be applied when pods start forming to ensure healthy grain development.",
        "irrigation": "Soybeans require less water compared to other crops. Use drip irrigation to avoid waterlogging. Irrigate at critical stages such as flowering, pod development, and seed filling.",
        "maintenance": "Control weeds using pre-emergent herbicides and mechanical weeding in the early stages. Monitor for pests like aphids and whiteflies, and use insecticides if necessary. Rotate crops to reduce disease pressure.",
        "cultivation": "Best grown in well-drained loamy soil with a neutral pH. Sow seeds 2-3 cm deep, spaced 30-40 cm apart. Soybeans prefer a warm, temperate climate with moderate rainfall."
    },
    "maize": {
        "fertilizer": "Apply Nitrogen at 120-150 kg/ha in split doses: one-third at planting, one-third during vegetative growth, and one-third at the tasseling stage. Phosphorus (50-60 kg/ha) is essential during early growth.",
        "irrigation": "Maize needs adequate water, especially during germination, flowering, and grain filling stages. Drip or furrow irrigation is recommended. Avoid water stress during the silk and tassel stages.",
        "maintenance": "Weed control is critical during the first 6 weeks. Monitor for common pests like stem borers and earworms, and apply integrated pest management (IPM) practices. Thin out weak seedlings to allow healthy growth.",
        "cultivation": "Plant in well-drained sandy loam or loamy soil. Maize is a warm-season crop that requires full sunlight. Maintain plant spacing of 20-25 cm between rows. Regular soil testing can optimize fertilization."
    },
    "peas": {
        "fertilizer": "Use Phosphate at 30-50 kg/ha to boost root development. Potassium (30-40 kg/ha) ensures strong stem growth. Organic fertilizers like compost or manure improve soil health.",
        "irrigation": "Peas are sensitive to waterlogging, so ensure well-drained soil. Light irrigation during flowering and pod formation ensures a higher yield. Avoid excess moisture as it can lead to root rot.",
        "maintenance": "Support plants with stakes or a trellis for easier harvesting. Control pests like aphids and leaf miners using organic sprays. Regular weeding is important, as peas struggle with weed competition.",
        "cultivation": "Cultivate peas in cool weather, preferably in spring or fall. They grow well in loamy, well-aerated soil. Plant seeds 2-3 cm deep and ensure spacing of 15-20 cm between plants."
    },
    "groundnuts": {
        "fertilizer": "Apply Gypsum at 500 kg/ha at the flowering stage to improve pod filling. Potash (40-60 kg/ha) promotes better root growth and ensures higher yield.",
        "irrigation": "Groundnuts need moderate irrigation, especially during flowering, pegging, and pod development. Sandy loam soil is ideal for proper drainage, but avoid over-irrigation as it can lead to diseases.",
        "maintenance": "Hand-weeding or mechanical weeding is essential in the early stages. Monitor for pests like leaf hoppers and manage diseases like rust through proper crop rotation and fungicides.",
        "cultivation": "Groundnuts thrive in well-drained sandy loam soil. Sow seeds 4-5 cm deep and ensure proper spacing of 30-45 cm between rows. A warm, dry climate is ideal for optimal pod development."
    },
    "cowpeas": {
        "fertilizer": "Use Rhizobium inoculants to enhance nitrogen fixation. Apply Phosphorus (30-50 kg/ha) and Potassium (40-60 kg/ha) during sowing to improve root and shoot growth.",
        "irrigation": "Cowpeas are drought-tolerant but benefit from light irrigation during the flowering and pod formation stages. Mulching helps retain moisture in the soil during dry periods.",
        "maintenance": "Pest control is critical, especially for aphids and weevils. Ensure proper drainage to avoid water stress and use organic mulch to retain soil moisture. Regular weeding is required in the early growth stages.",
        "cultivation": "Best cultivated in warm, tropical climates with light-textured soils. Plant seeds at a depth of 4-5 cm, and maintain row spacing of 30-40 cm. Ideal temperatures for growth range from 25-30°C."
    },
    "banana": {
        "fertilizer": "Apply Urea at 200-250 g per plant, divided into three doses during the growth cycle. Potassium (400-500 g) ensures better fruit quality and resistance to diseases.",
        "irrigation": "Bananas need consistent irrigation. Use flood or drip irrigation for best results. Water 2-3 times a week during dry periods to maintain soil moisture levels.",
        "maintenance": "Regularly remove dead or damaged leaves to promote healthy growth. Control pests like nematodes and banana weevils with proper soil management and pesticides. Apply mulch around the base to retain moisture.",
        "cultivation": "Bananas grow best in rich, organic soils with good drainage. Plant suckers 30-40 cm deep, with a spacing of 2-3 meters between plants. They thrive in tropical climates with temperatures between 15-35°C."
    },
    "mango": {
        "fertilizer": "Use organic manure (20-30 kg per tree) at planting. Apply Urea (1 kg/tree) and Potash (1.5 kg/tree) during the fruiting stage for improved yield.",
        "irrigation": "Irrigate mango trees once a week during flowering and fruit development. Use basin or drip irrigation to ensure water reaches the root zone. Reduce watering during the dormant period.",
        "maintenance": "Prune mango trees regularly to maintain airflow and reduce disease pressure. Manage common pests like fruit flies and mealybugs with traps or sprays. Apply mulch to maintain soil moisture.",
        "cultivation": "Mangoes prefer loamy, well-drained soils with a pH of 6.0-7.5. Plant saplings at a depth of 60-70 cm and space them 10-12 meters apart. Mangoes thrive in warm, tropical climates."
    },
    "grapes": {
        "fertilizer": "Apply Phosphorus (30-40 kg/ha) and Potassium (60-80 kg/ha) during planting. Organic compost or manure helps improve soil structure. Use Urea sparingly to avoid excessive vegetative growth.",
        "irrigation": "Grapes require regular irrigation during flowering and fruit set. Drip irrigation ensures even moisture distribution. Avoid water stress during berry development for better fruit quality.",
        "maintenance": "Prune vines annually to promote healthy growth and fruit production. Use trellises or support structures to prevent the vines from sprawling. Monitor for pests like grapevine moths and fungal diseases.",
        "cultivation": "Grapes grow well in loamy, well-drained soil with good sun exposure. Plant cuttings 15-20 cm deep and space rows 2-3 meters apart. They thrive in temperate climates."
    },
    "watermelon": {
        "fertilizer": "Apply Potash (60-80 kg/ha) and Nitrogen (40-50 kg/ha) at the fruit-setting stage. Phosphorus (20-30 kg/ha) at planting ensures good root development.",
        "irrigation": "Watermelons need frequent irrigation, especially during fruit development. Use drip irrigation to avoid waterlogging. Reduce irrigation when fruits reach maturity to enhance sweetness.",
        "maintenance": "Control weeds through mulching or herbicides. Monitor for pests like aphids and cucumber beetles, and apply pesticides if necessary. Thin plants to allow better air circulation.",
        "cultivation": "Best grown in sandy, loamy soils with good drainage. Plant seeds 2-3 cm deep, with a spacing of 60-90 cm between plants. Watermelons thrive in warm climates with full sunlight."
    },
    "apple": {
        "fertilizer": "Use Potassium Nitrate (1-2 kg/tree) during fruit development. Apply Urea (500-700 g/tree) in the growing season. Organic mulch helps retain soil moisture and improves soil structure.",
        "irrigation": "Irrigate regularly during the growing season, especially during flowering and fruit development. Avoid over-watering as it can lead to root rot. Drip irrigation is recommended.",
        "maintenance": "Prune apple trees annually to promote airflow and remove dead branches. Manage pests like codling moths and diseases like apple scab with organic sprays and fungicides.",
        "cultivation": "Apples prefer cool, temperate climates with well-drained loamy soils. Plant trees at a spacing of 4-5 meters apart and 2-3 meters between rows. They need full sunlight for optimal growth."
    },
    "orange": {
        "fertilizer": "Apply Phosphorus (50-60 kg/ha) and Potassium (40-60 kg/ha) at planting. Urea (40-50 kg/ha) ensures better fruit size and quality during the fruiting stage.",
        "irrigation": "Irrigate orange trees once a week, especially during the flowering and fruiting stages. Drip irrigation helps ensure proper water distribution without waterlogging the roots.",
        "maintenance": "Prune regularly to remove dead branches and promote healthy growth. Protect against frost and manage pests like aphids and citrus mites with insecticides. Mulch around trees to retain moisture.",
        "cultivation": "Oranges grow best in sandy loam soils with a pH of 6.0-7.5. Plant saplings 30-40 cm deep, spacing them 4-6 meters apart. They thrive in subtropical climates with moderate rainfall."
    },
    "cotton": {
        "fertilizer": "Apply Ammonium Nitrate (80-100 kg/ha) and Potash (60-80 kg/ha) at sowing. Phosphorus (40-50 kg/ha) should be applied during the early vegetative stage.",
        "irrigation": "Cotton needs moderate irrigation, especially during flowering and boll formation. Drip irrigation is ideal for maintaining soil moisture without waterlogging.",
        "maintenance": "Monitor for common pests like bollworms and whiteflies. Use biological control or pesticides as necessary. Regular weeding in the early stages helps reduce competition for nutrients.",
        "cultivation": "Best grown in well-drained sandy loam soils. Plant seeds 3-4 cm deep, spaced 30-40 cm apart. Cotton requires full sunlight and warm temperatures for optimal growth."
    },
    "coffee": {
        "fertilizer": "Apply Urea (100-120 kg/ha) and Phosphate (40-60 kg/ha) during the growth phase. Organic compost or manure improves soil fertility. Avoid over-fertilizing as it can affect bean quality.",
        "irrigation": "Coffee plants require regular irrigation, especially during flowering and berry formation. Drip irrigation is preferred in well-drained soil. Avoid water stress to prevent reduced yields.",
        "maintenance": "Prune coffee plants annually to promote new growth and remove diseased branches. Manage pests like coffee berry borers with organic pest control methods. Mulching helps retain soil moisture.",
        "cultivation": "Coffee thrives in tropical climates with well-drained, rich organic soils. Plant seedlings 3-4 cm deep, with a spacing of 1.5-2 meters between plants. Partial shade is beneficial for growth."
    }
}


@app.route("/", methods=['GET'])
def hello():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST': 
        # Retrieve form data
        d1 = request.form['N']
        d2 = request.form['P']
        d3 = request.form['K']
        d4 = request.form['temperature']
        d5 = request.form['humidity']
        d6 = request.form['ph']
        d7 = request.form['rainfall']  

        # Create input array for model prediction
        arr = np.array([[d1, d2, d3, d4, d5, d6, d7]])
        print([d1, d2, d3, d4, d5, d6, d7])

        # Predict the crop
        pred1 = model1.predict(arr)[0]
        print(pred1)

        # Get the recommendation based on predicted crop
        recommendation = crop_recommendations.get(pred1, "No recommendations available for this crop.")

    return render_template('result.html', prediction_text1=pred1, recommendation_text=recommendation)

if __name__ == '__main__':
    app.run(debug=False)
