% ============================================================
% Medical Expert System - Knowledge Base (SWI-Prolog)
% SPDX-License-Identifier: AGPL-3.0-or-later
%
% The facts block between the BEGIN/END markers below is GENERATED
% from kb_catalog.json by generate_kb.py. Edit kb_catalog.json and
% run `python generate_kb.py`; do not hand-edit that block.
% The header and the inference rules below are maintained by hand.
% ============================================================

:- dynamic patient_has/1, patient_sev/2.

% ------------------- GENERATED FACTS (BEGIN) -------------------
% Knowledge facts generated from kb_catalog.json (version 3.0).
%% Do not edit by hand - regenerate with: python generate_kb.py

% Diseases
disease(flu).
disease(cold).
disease(covid19).
disease(malaria).
disease(dengue).
disease(typhoid).
disease(migraine).
disease(asthma).
disease(pneumonia).
disease(diabetes).
disease(hypertension).
disease(anemia).
disease(allergy).
disease(chickenpox).
disease(measles).
disease(hepatitis_a).
disease(tuberculosis).
disease(bronchitis).
disease(sinusitis).
disease(urinary_tract_infection).
disease(gastroenteritis).
disease(heat_stroke).
disease(insomnia).
disease(depression).
disease(arthritis).
disease(gerd).
disease(tension_headache).
disease(mononucleosis).
disease(conjunctivitis).
disease(otitis_media).
disease(laryngitis).
disease(appendicitis).
disease(kidney_stones).
disease(stroke).
disease(heart_attack).
disease(copd).
disease(hypothyroidism).
disease(hyperthyroidism).
disease(gout).
disease(fibromyalgia).
disease(ibs).
disease(diverticulitis).
disease(pancreatitis).
disease(cholecystitis).
disease(lupus).
disease(rheumatoid_arthritis).
disease(multiple_sclerosis).
disease(parkinsons).
disease(epilepsy).
disease(chronic_fatigue_syndrome).
disease(food_poisoning).
disease(whooping_cough).
disease(scarlet_fever).
disease(celiac_disease).
disease(hemorrhoids).

% Disease categories
category(flu, viral).
category(cold, viral).
category(covid19, viral).
category(malaria, parasitic).
category(dengue, viral).
category(typhoid, bacterial).
category(migraine, neurological).
category(asthma, respiratory).
category(pneumonia, respiratory).
category(diabetes, metabolic).
category(hypertension, cardiovascular).
category(anemia, hematologic).
category(allergy, immune).
category(chickenpox, viral).
category(measles, viral).
category(hepatitis_a, viral).
category(tuberculosis, bacterial).
category(bronchitis, respiratory).
category(sinusitis, inflammatory).
category(urinary_tract_infection, bacterial).
category(gastroenteritis, gastrointestinal).
category(heat_stroke, environmental).
category(insomnia, neurological).
category(depression, psychological).
category(arthritis, musculoskeletal).
category(gerd, gastrointestinal).
category(tension_headache, neurological).
category(mononucleosis, viral).
category(conjunctivitis, inflammatory).
category(otitis_media, inflammatory).
category(laryngitis, respiratory).
category(appendicitis, gastrointestinal).
category(kidney_stones, urological).
category(stroke, cardiovascular).
category(heart_attack, cardiovascular).
category(copd, respiratory).
category(hypothyroidism, metabolic).
category(hyperthyroidism, metabolic).
category(gout, metabolic).
category(fibromyalgia, musculoskeletal).
category(ibs, gastrointestinal).
category(diverticulitis, gastrointestinal).
category(pancreatitis, gastrointestinal).
category(cholecystitis, gastrointestinal).
category(lupus, autoimmune).
category(rheumatoid_arthritis, autoimmune).
category(multiple_sclerosis, autoimmune).
category(parkinsons, neurological).
category(epilepsy, neurological).
category(chronic_fatigue_syndrome, autoimmune).
category(food_poisoning, gastrointestinal).
category(whooping_cough, bacterial).
category(scarlet_fever, bacterial).
category(celiac_disease, autoimmune).
category(hemorrhoids, gastrointestinal).

% Disease descriptions
description(flu, 'Influenza is a viral infection that attacks the respiratory system. It is highly contagious and spreads through droplets.').
description(cold, 'The common cold is a viral infection of the upper respiratory tract. It is usually mild and self-limiting.').
description(covid19, 'COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus. It can range from mild to severe and is highly contagious.').
description(malaria, 'Malaria is a parasitic disease transmitted through mosquito bites. It causes recurrent fever and can be life-threatening.').
description(dengue, 'Dengue is a mosquito-borne viral infection causing severe flu-like symptoms and sometimes hemorrhagic fever.').
description(typhoid, 'Typhoid fever is a bacterial infection caused by Salmonella typhi, spread through contaminated food and water.').
description(migraine, 'Migraine is a neurological condition causing intense, debilitating headaches often accompanied by nausea and sensitivity to light.').
description(asthma, 'Asthma is a chronic respiratory condition causing airway inflammation and narrowing, leading to breathing difficulties.').
description(pneumonia, 'Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid.').
description(diabetes, 'Diabetes is a metabolic disorder characterized by high blood sugar levels over a prolonged period.').
description(hypertension, 'Hypertension or high blood pressure is a chronic condition where blood pressure in the arteries is elevated.').
description(anemia, 'Anemia is a condition where the body lacks enough healthy red blood cells to carry adequate oxygen to tissues.').
description(allergy, 'Allergies are immune system reactions to foreign substances that are typically harmless to most people.').
description(chickenpox, 'Chickenpox is a highly contagious viral infection causing an itchy rash with small fluid-filled blisters.').
description(measles, 'Measles is a highly contagious viral infection causing a distinctive red rash, fever, and cough.').
description(hepatitis_a, 'Hepatitis A is a viral liver infection transmitted through contaminated food or water.').
description(tuberculosis, 'Tuberculosis is a bacterial infection that primarily affects the lungs and spreads through airborne droplets.').
description(bronchitis, 'Bronchitis is inflammation of the bronchial tubes, causing persistent cough with mucus.').
description(sinusitis, 'Sinusitis is inflammation of the sinuses, usually caused by infection, leading to facial pain and congestion.').
description(urinary_tract_infection, 'UTI is a bacterial infection in any part of the urinary system, most commonly the bladder.').
description(gastroenteritis, 'Gastroenteritis is inflammation of the stomach and intestines, causing diarrhea and vomiting.').
description(heat_stroke, 'Heat stroke is a severe heat-related illness occurring when body temperature rises rapidly and the body cannot cool down.').
description(insomnia, 'Insomnia is a sleep disorder characterized by difficulty falling or staying asleep.').
description(depression, 'Depression is a mental health disorder causing persistent feelings of sadness and loss of interest.').
description(arthritis, 'Arthritis is inflammation of one or more joints, causing pain and stiffness that worsens with age.').
description(gerd, 'Gastroesophageal reflux disease (GERD) is a chronic condition where stomach acid frequently flows back into the esophagus, causing irritation.').
description(tension_headache, 'Tension headaches are the most common type of headache, causing a dull, aching sensation all over the head.').
description(mononucleosis, 'Mononucleosis (mono) is a viral infection caused by Epstein-Barr virus, causing fever, sore throat, and swollen glands.').
description(conjunctivitis, 'Conjunctivitis (pink eye) is inflammation of the conjunctiva, causing red, itchy, and sometimes discharge from the eye.').
description(otitis_media, 'Otitis media is an infection of the middle ear, causing ear pain, fever, and sometimes hearing loss.').
description(laryngitis, 'Laryngitis is inflammation of the voice box (larynx), causing hoarseness and voice loss.').
description(appendicitis, 'Appendicitis is inflammation of the appendix, a medical emergency requiring immediate surgical removal.').
description(kidney_stones, 'Kidney stones are hard deposits of minerals and salts that form inside the kidneys, causing severe pain.').
description(stroke, 'Stroke occurs when blood supply to part of the brain is interrupted, causing brain cell death. It is a medical emergency.').
description(heart_attack, 'Myocardial infarction (heart attack) occurs when blood flow to the heart muscle is blocked, causing tissue damage.').
description(copd, 'Chronic Obstructive Pulmonary Disease (COPD) is a progressive lung disease causing breathing difficulties.').
description(hypothyroidism, 'Hypothyroidism is an underactive thyroid gland that doesn\'t produce enough thyroid hormones, slowing metabolism.').
description(hyperthyroidism, 'Hyperthyroidism is an overactive thyroid gland producing too much thyroid hormone, speeding up metabolism.').
description(gout, 'Gout is a form of inflammatory arthritis caused by excess uric acid in the blood, causing sudden severe joint pain.').
description(fibromyalgia, 'Fibromyalgia is a chronic condition causing widespread musculoskeletal pain, fatigue, and cognitive difficulties.').
description(ibs, 'Irritable Bowel Syndrome (IBS) is a chronic gastrointestinal disorder causing abdominal pain, bloating, and altered bowel habits.').
description(diverticulitis, 'Diverticulitis is inflammation or infection of small pouches (diverticula) that develop in the colon.').
description(pancreatitis, 'Pancreatitis is inflammation of the pancreas, which can be acute or chronic, causing severe abdominal pain.').
description(cholecystitis, 'Cholecystitis is inflammation of the gallbladder, usually caused by gallstones blocking the bile duct.').
description(lupus, 'Systemic Lupus Erythematosus (SLE) is a chronic autoimmune disease where the immune system attacks healthy tissue.').
description(rheumatoid_arthritis, 'Rheumatoid arthritis is an autoimmune disorder where the immune system attacks joint linings, causing painful swelling.').
description(multiple_sclerosis, 'Multiple sclerosis is an autoimmune disease affecting the central nervous system, disrupting communication between brain and body.').
description(parkinsons, 'Parkinson\'s disease is a progressive nervous system disorder affecting movement, causing tremors and stiffness.').
description(epilepsy, 'Epilepsy is a neurological disorder causing recurrent seizures due to abnormal electrical activity in the brain.').
description(chronic_fatigue_syndrome, 'Chronic fatigue syndrome (ME/CFS) is a complex disorder causing extreme fatigue that doesn\'t improve with rest.').
description(food_poisoning, 'Food poisoning is an illness caused by eating contaminated food, leading to nausea, vomiting, and diarrhea.').
description(whooping_cough, 'Whooping cough (pertussis) is a highly contagious bacterial infection causing severe coughing fits.').
description(scarlet_fever, 'Scarlet fever is a bacterial infection causing a distinctive red rash, high fever, and sore throat.').
description(celiac_disease, 'Celiac disease is an autoimmune disorder where ingesting gluten leads to damage in the small intestine.').
description(hemorrhoids, 'Hemorrhoids are swollen veins in the lower rectum and anus, causing pain, itching, and bleeding.').

% Recommendations
recommendation(flu, 'Rest, stay hydrated, take antiviral medications if prescribed, and isolate to prevent spreading.').
recommendation(cold, 'Rest, drink warm fluids, use saline nasal drops, and take over-the-counter cold remedies.').
recommendation(covid19, 'Isolate immediately, monitor oxygen levels, seek medical attention if breathing becomes difficult.').
recommendation(malaria, 'Seek immediate medical treatment, take antimalarial drugs, and use mosquito nets.').
recommendation(dengue, 'Seek medical care, stay hydrated, avoid aspirin, and monitor platelet count.').
recommendation(typhoid, 'Consult a doctor for antibiotics, maintain hygiene, and drink only boiled water.').
recommendation(migraine, 'Rest in a dark room, avoid triggers, take prescribed migraine medication.').
recommendation(asthma, 'Use inhaler as prescribed, avoid triggers, and seek emergency care if breathing worsens.').
recommendation(pneumonia, 'Seek medical attention, take prescribed antibiotics, rest, and stay hydrated.').
recommendation(diabetes, 'Monitor blood sugar regularly, follow a diabetic diet, exercise, and take prescribed medication.').
recommendation(hypertension, 'Reduce salt intake, exercise regularly, manage stress, and take prescribed medication.').
recommendation(anemia, 'Increase iron-rich foods, take iron supplements, and consult a doctor for underlying causes.').
recommendation(allergy, 'Avoid allergens, take antihistamines, and use nasal sprays for relief.').
recommendation(chickenpox, 'Isolate, avoid scratching, use calamine lotion, and take fever reducers.').
recommendation(measles, 'Isolate, rest, stay hydrated, and seek medical care for complications.').
recommendation(hepatitis_a, 'Rest, avoid alcohol, eat a balanced diet, and consult a doctor.').
recommendation(tuberculosis, 'Seek immediate medical treatment, complete full antibiotic course, and isolate initially.').
recommendation(bronchitis, 'Rest, stay hydrated, use a humidifier, and avoid smoke exposure.').
recommendation(sinusitis, 'Use saline nasal irrigation, steam inhalation, and decongestants.').
recommendation(urinary_tract_infection, 'Drink plenty of water, urinate frequently, and take prescribed antibiotics.').
recommendation(gastroenteritis, 'Stay hydrated with oral rehydration solutions, eat bland foods, and rest.').
recommendation(heat_stroke, 'Move to a cool place, apply cold water, seek emergency medical care immediately.').
recommendation(insomnia, 'Maintain regular sleep schedule, avoid screens before bed, and practice relaxation.').
recommendation(depression, 'Seek professional counseling, maintain social connections, and consider therapy.').
recommendation(arthritis, 'Exercise gently, apply heat/cold therapy, and consult a rheumatologist.').
recommendation(gerd, 'Avoid trigger foods, eat smaller meals, elevate head while sleeping, and take antacids or proton pump inhibitors.').
recommendation(tension_headache, 'Rest, manage stress, take over-the-counter pain relievers, and practice relaxation techniques.').
recommendation(mononucleosis, 'Rest, stay hydrated, avoid strenuous activity, and manage symptoms with pain relievers.').
recommendation(conjunctivitis, 'Avoid touching eyes, wash hands frequently, use prescribed eye drops, and avoid sharing towels.').
recommendation(otitis_media, 'Seek medical attention for antibiotics, manage pain with OTC pain relievers, and apply warm compresses.').
recommendation(laryngitis, 'Rest your voice, stay hydrated, use a humidifier, and avoid irritants like smoke.').
recommendation(appendicitis, 'Seek emergency medical care immediately. Do not eat or drink anything. Surgery is required.').
recommendation(kidney_stones, 'Seek medical attention, drink plenty of fluids, and take pain medication. Large stones may require surgery.').
recommendation(stroke, 'Call emergency services immediately. Time is critical. Note the time symptoms started.').
recommendation(heart_attack, 'Call emergency services immediately. Chew aspirin if not allergic. Do not drive yourself to hospital.').
recommendation(copd, 'Quit smoking, use prescribed inhalers, attend pulmonary rehabilitation, and avoid lung irritants.').
recommendation(hypothyroidism, 'Take thyroid hormone replacement medication as prescribed, and get regular blood tests.').
recommendation(hyperthyroidism, 'Take anti-thyroid medication, radioactive iodine therapy, or surgery as recommended by your doctor.').
recommendation(gout, 'Take anti-inflammatory medication, avoid high-purine foods, stay hydrated, and rest the affected joint.').
recommendation(fibromyalgia, 'Exercise regularly, manage stress, take prescribed medications, and maintain good sleep hygiene.').
recommendation(ibs, 'Follow a low-FODMAP diet, manage stress, exercise regularly, and use prescribed medications.').
recommendation(diverticulitis, 'Seek medical attention, take prescribed antibiotics, follow a liquid diet initially, then high-fiber diet.').
recommendation(pancreatitis, 'Seek emergency care for acute pancreatitis. Stop alcohol, follow a low-fat diet, and take prescribed medications.').
recommendation(cholecystitis, 'Seek medical care, follow a low-fat diet, and surgery may be required to remove the gallbladder.').
recommendation(lupus, 'Take immunosuppressive medication, avoid sun exposure, manage fatigue, and see a rheumatologist regularly.').
recommendation(rheumatoid_arthritis, 'Take disease-modifying antirheumatic drugs (DMARDs), exercise gently, and consult a rheumatologist.').
recommendation(multiple_sclerosis, 'Take disease-modifying therapies, manage symptoms with physical therapy, and avoid heat exposure.').
recommendation(parkinsons, 'Take dopamine-enhancing medications, exercise regularly, and work with a neurologist.').
recommendation(epilepsy, 'Take anti-epileptic medications as prescribed, avoid seizure triggers, and get adequate sleep.').
recommendation(chronic_fatigue_syndrome, 'Pace activities, prioritize sleep, manage stress, and work with a specialist for symptom management.').
recommendation(food_poisoning, 'Stay hydrated, rest, avoid solid food until vomiting stops, and seek medical care if symptoms are severe.').
recommendation(whooping_cough, 'Seek medical treatment with antibiotics, stay isolated, and ensure vaccination for prevention.').
recommendation(scarlet_fever, 'Seek medical treatment with antibiotics, stay isolated, and maintain good hygiene.').
recommendation(celiac_disease, 'Follow a strict gluten-free diet, take nutritional supplements, and monitor with a gastroenterologist.').
recommendation(hemorrhoids, 'Increase fiber intake, use stool softeners, take sitz baths, and consult a doctor for persistent cases.').

% Emergency flags
is_emergency(covid19).
is_emergency(malaria).
is_emergency(dengue).
is_emergency(pneumonia).
is_emergency(hepatitis_a).
is_emergency(tuberculosis).
is_emergency(heat_stroke).
is_emergency(appendicitis).
is_emergency(kidney_stones).
is_emergency(stroke).
is_emergency(heart_attack).
is_emergency(diverticulitis).
is_emergency(pancreatitis).
is_emergency(cholecystitis).

% Symptoms
symptom(fever).
symptom(fatigue).
symptom(chills).
symptom(sweating).
symptom(weight_loss).
symptom(weight_gain).
symptom(loss_of_appetite).
symptom(night_sweats).
symptom(frequent_infections).
symptom(bruising_easily).
symptom(slow_healing_wounds).
symptom(sensitivity_to_cold).
symptom(sensitivity_to_heat).
symptom(cough).
symptom(shortness_of_breath).
symptom(sore_throat).
symptom(wheezing).
symptom(runny_nose).
symptom(nasal_congestion).
symptom(sneezing).
symptom(coughing_blood).
symptom(rapid_breathing).
symptom(loss_of_smell).
symptom(loss_of_taste).
symptom(hoarseness).
symptom(throat_swelling).
symptom(headache).
symptom(dizziness).
symptom(blurred_vision).
symptom(double_vision).
symptom(sensitivity_to_light).
symptom(confusion).
symptom(insomnia).
symptom(difficulty_concentrating).
symptom(numbness).
symptom(tremors).
symptom(seizure).
symptom(memory_problems).
symptom(mood_swings).
symptom(irritability).
symptom(loss_of_consciousness).
symptom(nausea).
symptom(vomiting).
symptom(diarrhea).
symptom(abdominal_pain).
symptom(bloating).
symptom(heartburn).
symptom(constipation).
symptom(blood_in_stool).
symptom(excessive_hunger).
symptom(dark_urine).
symptom(pale_stool).
symptom(abdominal_distension).
symptom(body_ache).
symptom(joint_pain).
symptom(muscle_pain).
symptom(back_pain).
symptom(stiff_joints).
symptom(joint_swelling).
symptom(muscle_cramps).
symptom(neck_pain).
symptom(shoulder_pain).
symptom(knee_pain).
symptom(rash).
symptom(pale_skin).
symptom(yellowing_of_skin).
symptom(itchy_skin).
symptom(dry_skin).
symptom(peeling_skin).
symptom(skin_discoloration).
symptom(hair_loss).
symptom(skin_lesions).
symptom(boils).
symptom(chest_pain).
symptom(rapid_heartbeat).
symptom(cold_hands_and_feet).
symptom(swollen_ankles).
symptom(slow_heartbeat).
symptom(leg_pain_walking).
symptom(frequent_urination).
symptom(burning_urination).
symptom(blood_in_urine).
symptom(difficulty_urinating).
symptom(urinary_urgency).
symptom(sadness).
symptom(loss_of_interest).
symptom(anxiety).
symptom(panic_attacks).
symptom(itchy_eyes).
symptom(red_eyes).
symptom(swollen_glands).
symptom(facial_pain).
symptom(ear_pain).
symptom(ear_discharge).
symptom(nosebleed).
symptom(eye_pain).
symptom(eye_discharge).
symptom(tinnitus).
symptom(hearing_loss).
symptom(tooth_pain).
symptom(mouth_ulcers).
symptom(gum_bleeding).
symptom(increased_thirst).
symptom(excessive_hunger).

% Disease-symptom links
has_symptom(flu, fever).
has_symptom(flu, cough).
has_symptom(flu, headache).
has_symptom(flu, fatigue).
has_symptom(flu, body_ache).
has_symptom(flu, chills).
has_symptom(flu, sore_throat).
has_symptom(cold, runny_nose).
has_symptom(cold, sneezing).
has_symptom(cold, sore_throat).
has_symptom(cold, cough).
has_symptom(cold, headache).
has_symptom(cold, fatigue).
has_symptom(cold, nasal_congestion).
has_symptom(covid19, fever).
has_symptom(covid19, cough).
has_symptom(covid19, shortness_of_breath).
has_symptom(covid19, fatigue).
has_symptom(covid19, body_ache).
has_symptom(covid19, headache).
has_symptom(covid19, loss_of_appetite).
has_symptom(covid19, sore_throat).
has_symptom(covid19, loss_of_smell).
has_symptom(covid19, loss_of_taste).
has_symptom(malaria, fever).
has_symptom(malaria, chills).
has_symptom(malaria, sweating).
has_symptom(malaria, headache).
has_symptom(malaria, nausea).
has_symptom(malaria, vomiting).
has_symptom(malaria, body_ache).
has_symptom(dengue, fever).
has_symptom(dengue, headache).
has_symptom(dengue, joint_pain).
has_symptom(dengue, muscle_pain).
has_symptom(dengue, rash).
has_symptom(dengue, nausea).
has_symptom(dengue, vomiting).
has_symptom(dengue, swollen_glands).
has_symptom(typhoid, fever).
has_symptom(typhoid, headache).
has_symptom(typhoid, fatigue).
has_symptom(typhoid, nausea).
has_symptom(typhoid, vomiting).
has_symptom(typhoid, diarrhea).
has_symptom(typhoid, loss_of_appetite).
has_symptom(typhoid, abdominal_pain).
has_symptom(migraine, headache).
has_symptom(migraine, nausea).
has_symptom(migraine, vomiting).
has_symptom(migraine, blurred_vision).
has_symptom(migraine, dizziness).
has_symptom(migraine, sensitivity_to_light).
has_symptom(asthma, shortness_of_breath).
has_symptom(asthma, wheezing).
has_symptom(asthma, chest_pain).
has_symptom(asthma, cough).
has_symptom(asthma, fatigue).
has_symptom(pneumonia, fever).
has_symptom(pneumonia, cough).
has_symptom(pneumonia, shortness_of_breath).
has_symptom(pneumonia, chest_pain).
has_symptom(pneumonia, fatigue).
has_symptom(pneumonia, chills).
has_symptom(pneumonia, sweating).
has_symptom(pneumonia, nausea).
has_symptom(diabetes, frequent_urination).
has_symptom(diabetes, increased_thirst).
has_symptom(diabetes, fatigue).
has_symptom(diabetes, blurred_vision).
has_symptom(diabetes, weight_loss).
has_symptom(diabetes, slow_healing_wounds).
has_symptom(diabetes, excessive_hunger).
has_symptom(diabetes, mouth_ulcers).
has_symptom(diabetes, gum_bleeding).
has_symptom(diabetes, frequent_infections).
has_symptom(hypertension, headache).
has_symptom(hypertension, dizziness).
has_symptom(hypertension, chest_pain).
has_symptom(hypertension, shortness_of_breath).
has_symptom(hypertension, blurred_vision).
has_symptom(hypertension, leg_pain_walking).
has_symptom(anemia, fatigue).
has_symptom(anemia, pale_skin).
has_symptom(anemia, dizziness).
has_symptom(anemia, shortness_of_breath).
has_symptom(anemia, cold_hands_and_feet).
has_symptom(anemia, headache).
has_symptom(anemia, rapid_heartbeat).
has_symptom(allergy, sneezing).
has_symptom(allergy, itchy_eyes).
has_symptom(allergy, runny_nose).
has_symptom(allergy, rash).
has_symptom(allergy, cough).
has_symptom(allergy, nasal_congestion).
has_symptom(chickenpox, fever).
has_symptom(chickenpox, rash).
has_symptom(chickenpox, fatigue).
has_symptom(chickenpox, headache).
has_symptom(chickenpox, loss_of_appetite).
has_symptom(chickenpox, boils).
has_symptom(chickenpox, peeling_skin).
has_symptom(measles, fever).
has_symptom(measles, rash).
has_symptom(measles, cough).
has_symptom(measles, runny_nose).
has_symptom(measles, red_eyes).
has_symptom(measles, fatigue).
has_symptom(hepatitis_a, fever).
has_symptom(hepatitis_a, fatigue).
has_symptom(hepatitis_a, nausea).
has_symptom(hepatitis_a, vomiting).
has_symptom(hepatitis_a, abdominal_pain).
has_symptom(hepatitis_a, yellowing_of_skin).
has_symptom(hepatitis_a, loss_of_appetite).
has_symptom(hepatitis_a, dark_urine).
has_symptom(hepatitis_a, pale_stool).
has_symptom(tuberculosis, cough).
has_symptom(tuberculosis, fever).
has_symptom(tuberculosis, night_sweats).
has_symptom(tuberculosis, weight_loss).
has_symptom(tuberculosis, fatigue).
has_symptom(tuberculosis, chest_pain).
has_symptom(tuberculosis, coughing_blood).
has_symptom(bronchitis, cough).
has_symptom(bronchitis, fatigue).
has_symptom(bronchitis, chest_pain).
has_symptom(bronchitis, shortness_of_breath).
has_symptom(bronchitis, wheezing).
has_symptom(bronchitis, fever).
has_symptom(sinusitis, facial_pain).
has_symptom(sinusitis, nasal_congestion).
has_symptom(sinusitis, headache).
has_symptom(sinusitis, runny_nose).
has_symptom(sinusitis, fatigue).
has_symptom(sinusitis, fever).
has_symptom(sinusitis, tooth_pain).
has_symptom(urinary_tract_infection, burning_urination).
has_symptom(urinary_tract_infection, frequent_urination).
has_symptom(urinary_tract_infection, abdominal_pain).
has_symptom(urinary_tract_infection, blood_in_urine).
has_symptom(urinary_tract_infection, fever).
has_symptom(urinary_tract_infection, difficulty_urinating).
has_symptom(urinary_tract_infection, urinary_urgency).
has_symptom(gastroenteritis, diarrhea).
has_symptom(gastroenteritis, vomiting).
has_symptom(gastroenteritis, nausea).
has_symptom(gastroenteritis, abdominal_pain).
has_symptom(gastroenteritis, fever).
has_symptom(gastroenteritis, bloating).
has_symptom(heat_stroke, fever).
has_symptom(heat_stroke, headache).
has_symptom(heat_stroke, dizziness).
has_symptom(heat_stroke, nausea).
has_symptom(heat_stroke, confusion).
has_symptom(heat_stroke, rapid_heartbeat).
has_symptom(insomnia, insomnia).
has_symptom(insomnia, fatigue).
has_symptom(insomnia, headache).
has_symptom(insomnia, difficulty_concentrating).
has_symptom(insomnia, dizziness).
has_symptom(depression, sadness).
has_symptom(depression, loss_of_interest).
has_symptom(depression, fatigue).
has_symptom(depression, insomnia).
has_symptom(depression, difficulty_concentrating).
has_symptom(depression, loss_of_appetite).
has_symptom(depression, panic_attacks).
has_symptom(arthritis, joint_pain).
has_symptom(arthritis, stiff_joints).
has_symptom(arthritis, fatigue).
has_symptom(arthritis, back_pain).
has_symptom(arthritis, muscle_pain).
has_symptom(arthritis, knee_pain).
has_symptom(arthritis, shoulder_pain).
has_symptom(gerd, heartburn).
has_symptom(gerd, chest_pain).
has_symptom(gerd, nausea).
has_symptom(gerd, bloating).
has_symptom(gerd, sore_throat).
has_symptom(gerd, cough).
has_symptom(gerd, abdominal_distension).
has_symptom(tension_headache, headache).
has_symptom(tension_headache, neck_pain).
has_symptom(tension_headache, irritability).
has_symptom(tension_headache, difficulty_concentrating).
has_symptom(mononucleosis, fever).
has_symptom(mononucleosis, sore_throat).
has_symptom(mononucleosis, fatigue).
has_symptom(mononucleosis, swollen_glands).
has_symptom(mononucleosis, headache).
has_symptom(mononucleosis, rash).
has_symptom(mononucleosis, loss_of_appetite).
has_symptom(conjunctivitis, red_eyes).
has_symptom(conjunctivitis, itchy_eyes).
has_symptom(conjunctivitis, eye_discharge).
has_symptom(conjunctivitis, eye_pain).
has_symptom(conjunctivitis, swollen_glands).
has_symptom(otitis_media, ear_pain).
has_symptom(otitis_media, fever).
has_symptom(otitis_media, hearing_loss).
has_symptom(otitis_media, ear_discharge).
has_symptom(otitis_media, irritability).
has_symptom(otitis_media, difficulty_concentrating).
has_symptom(laryngitis, hoarseness).
has_symptom(laryngitis, sore_throat).
has_symptom(laryngitis, cough).
has_symptom(laryngitis, fever).
has_symptom(laryngitis, difficulty_concentrating).
has_symptom(laryngitis, throat_swelling).
has_symptom(appendicitis, abdominal_pain).
has_symptom(appendicitis, nausea).
has_symptom(appendicitis, vomiting).
has_symptom(appendicitis, fever).
has_symptom(appendicitis, loss_of_appetite).
has_symptom(appendicitis, bloating).
has_symptom(kidney_stones, abdominal_pain).
has_symptom(kidney_stones, blood_in_urine).
has_symptom(kidney_stones, nausea).
has_symptom(kidney_stones, vomiting).
has_symptom(kidney_stones, burning_urination).
has_symptom(kidney_stones, frequent_urination).
has_symptom(stroke, confusion).
has_symptom(stroke, numbness).
has_symptom(stroke, blurred_vision).
has_symptom(stroke, difficulty_concentrating).
has_symptom(stroke, loss_of_consciousness).
has_symptom(stroke, dizziness).
has_symptom(stroke, double_vision).
has_symptom(stroke, memory_problems).
has_symptom(heart_attack, chest_pain).
has_symptom(heart_attack, shortness_of_breath).
has_symptom(heart_attack, rapid_heartbeat).
has_symptom(heart_attack, sweating).
has_symptom(heart_attack, nausea).
has_symptom(heart_attack, dizziness).
has_symptom(heart_attack, swollen_ankles).
has_symptom(copd, shortness_of_breath).
has_symptom(copd, cough).
has_symptom(copd, wheezing).
has_symptom(copd, fatigue).
has_symptom(copd, chest_pain).
has_symptom(copd, rapid_breathing).
has_symptom(copd, slow_heartbeat).
has_symptom(hypothyroidism, fatigue).
has_symptom(hypothyroidism, weight_gain).
has_symptom(hypothyroidism, sensitivity_to_cold).
has_symptom(hypothyroidism, dry_skin).
has_symptom(hypothyroidism, constipation).
has_symptom(hypothyroidism, sadness).
has_symptom(hypothyroidism, hair_loss).
has_symptom(hypothyroidism, muscle_pain).
has_symptom(hypothyroidism, muscle_cramps).
has_symptom(hypothyroidism, skin_discoloration).
has_symptom(hyperthyroidism, weight_loss).
has_symptom(hyperthyroidism, rapid_heartbeat).
has_symptom(hyperthyroidism, anxiety).
has_symptom(hyperthyroidism, tremors).
has_symptom(hyperthyroidism, sensitivity_to_heat).
has_symptom(hyperthyroidism, sweating).
has_symptom(hyperthyroidism, difficulty_concentrating).
has_symptom(hyperthyroidism, insomnia).
has_symptom(gout, joint_pain).
has_symptom(gout, joint_swelling).
has_symptom(gout, red_eyes).
has_symptom(gout, fever).
has_symptom(gout, fatigue).
has_symptom(fibromyalgia, muscle_pain).
has_symptom(fibromyalgia, joint_pain).
has_symptom(fibromyalgia, fatigue).
has_symptom(fibromyalgia, insomnia).
has_symptom(fibromyalgia, difficulty_concentrating).
has_symptom(fibromyalgia, headache).
has_symptom(fibromyalgia, sadness).
has_symptom(fibromyalgia, anxiety).
has_symptom(fibromyalgia, tinnitus).
has_symptom(fibromyalgia, muscle_cramps).
has_symptom(ibs, abdominal_pain).
has_symptom(ibs, bloating).
has_symptom(ibs, diarrhea).
has_symptom(ibs, constipation).
has_symptom(ibs, nausea).
has_symptom(ibs, fatigue).
has_symptom(ibs, abdominal_distension).
has_symptom(diverticulitis, abdominal_pain).
has_symptom(diverticulitis, fever).
has_symptom(diverticulitis, nausea).
has_symptom(diverticulitis, vomiting).
has_symptom(diverticulitis, bloating).
has_symptom(diverticulitis, constipation).
has_symptom(pancreatitis, abdominal_pain).
has_symptom(pancreatitis, nausea).
has_symptom(pancreatitis, vomiting).
has_symptom(pancreatitis, fever).
has_symptom(pancreatitis, rapid_heartbeat).
has_symptom(pancreatitis, bloating).
has_symptom(cholecystitis, abdominal_pain).
has_symptom(cholecystitis, nausea).
has_symptom(cholecystitis, vomiting).
has_symptom(cholecystitis, fever).
has_symptom(cholecystitis, bloating).
has_symptom(cholecystitis, loss_of_appetite).
has_symptom(cholecystitis, yellowing_of_skin).
has_symptom(cholecystitis, dark_urine).
has_symptom(lupus, fatigue).
has_symptom(lupus, joint_pain).
has_symptom(lupus, rash).
has_symptom(lupus, fever).
has_symptom(lupus, hair_loss).
has_symptom(lupus, sensitivity_to_cold).
has_symptom(lupus, difficulty_concentrating).
has_symptom(lupus, muscle_pain).
has_symptom(lupus, bruising_easily).
has_symptom(lupus, frequent_infections).
has_symptom(lupus, skin_lesions).
has_symptom(rheumatoid_arthritis, joint_pain).
has_symptom(rheumatoid_arthritis, joint_swelling).
has_symptom(rheumatoid_arthritis, stiff_joints).
has_symptom(rheumatoid_arthritis, fatigue).
has_symptom(rheumatoid_arthritis, fever).
has_symptom(rheumatoid_arthritis, muscle_pain).
has_symptom(multiple_sclerosis, numbness).
has_symptom(multiple_sclerosis, blurred_vision).
has_symptom(multiple_sclerosis, fatigue).
has_symptom(multiple_sclerosis, difficulty_concentrating).
has_symptom(multiple_sclerosis, muscle_pain).
has_symptom(multiple_sclerosis, dizziness).
has_symptom(multiple_sclerosis, mood_swings).
has_symptom(parkinsons, tremors).
has_symptom(parkinsons, stiff_joints).
has_symptom(parkinsons, difficulty_concentrating).
has_symptom(parkinsons, dizziness).
has_symptom(parkinsons, sadness).
has_symptom(parkinsons, fatigue).
has_symptom(parkinsons, memory_problems).
has_symptom(epilepsy, seizure).
has_symptom(epilepsy, confusion).
has_symptom(epilepsy, fatigue).
has_symptom(epilepsy, loss_of_consciousness).
has_symptom(epilepsy, difficulty_concentrating).
has_symptom(epilepsy, memory_problems).
has_symptom(chronic_fatigue_syndrome, fatigue).
has_symptom(chronic_fatigue_syndrome, headache).
has_symptom(chronic_fatigue_syndrome, joint_pain).
has_symptom(chronic_fatigue_syndrome, difficulty_concentrating).
has_symptom(chronic_fatigue_syndrome, insomnia).
has_symptom(chronic_fatigue_syndrome, muscle_pain).
has_symptom(chronic_fatigue_syndrome, sore_throat).
has_symptom(chronic_fatigue_syndrome, swollen_glands).
has_symptom(chronic_fatigue_syndrome, nosebleed).
has_symptom(food_poisoning, nausea).
has_symptom(food_poisoning, vomiting).
has_symptom(food_poisoning, diarrhea).
has_symptom(food_poisoning, abdominal_pain).
has_symptom(food_poisoning, fever).
has_symptom(food_poisoning, chills).
has_symptom(food_poisoning, fatigue).
has_symptom(whooping_cough, cough).
has_symptom(whooping_cough, sore_throat).
has_symptom(whooping_cough, runny_nose).
has_symptom(whooping_cough, fever).
has_symptom(whooping_cough, fatigue).
has_symptom(whooping_cough, vomiting).
has_symptom(scarlet_fever, fever).
has_symptom(scarlet_fever, rash).
has_symptom(scarlet_fever, sore_throat).
has_symptom(scarlet_fever, headache).
has_symptom(scarlet_fever, nausea).
has_symptom(scarlet_fever, swollen_glands).
has_symptom(celiac_disease, diarrhea).
has_symptom(celiac_disease, bloating).
has_symptom(celiac_disease, abdominal_pain).
has_symptom(celiac_disease, fatigue).
has_symptom(celiac_disease, weight_loss).
has_symptom(celiac_disease, pale_skin).
has_symptom(celiac_disease, joint_pain).
has_symptom(celiac_disease, rash).
has_symptom(hemorrhoids, blood_in_stool).
has_symptom(hemorrhoids, abdominal_pain).
has_symptom(hemorrhoids, itchy_skin).
has_symptom(hemorrhoids, pale_stool).

% Severity weights (one per disease-symptom pair; symptoms without an
% explicit weight in the catalog default to 1.0)
severity_weight(flu, fever, 1.2).
severity_weight(flu, cough, 1.0).
severity_weight(flu, headache, 1.0).
severity_weight(flu, fatigue, 1.0).
severity_weight(flu, body_ache, 1.1).
severity_weight(flu, chills, 1.0).
severity_weight(flu, sore_throat, 1.0).
severity_weight(cold, runny_nose, 1.0).
severity_weight(cold, sneezing, 1.0).
severity_weight(cold, sore_throat, 1.0).
severity_weight(cold, cough, 1.0).
severity_weight(cold, headache, 1.0).
severity_weight(cold, fatigue, 1.0).
severity_weight(cold, nasal_congestion, 1.0).
severity_weight(covid19, fever, 1.0).
severity_weight(covid19, cough, 1.0).
severity_weight(covid19, shortness_of_breath, 1.5).
severity_weight(covid19, fatigue, 1.0).
severity_weight(covid19, body_ache, 1.0).
severity_weight(covid19, headache, 1.0).
severity_weight(covid19, loss_of_appetite, 1.1).
severity_weight(covid19, sore_throat, 1.0).
severity_weight(covid19, loss_of_smell, 1.3).
severity_weight(covid19, loss_of_taste, 1.3).
severity_weight(malaria, fever, 1.0).
severity_weight(malaria, chills, 1.3).
severity_weight(malaria, sweating, 1.0).
severity_weight(malaria, headache, 1.0).
severity_weight(malaria, nausea, 1.0).
severity_weight(malaria, vomiting, 1.0).
severity_weight(malaria, body_ache, 1.0).
severity_weight(dengue, fever, 1.0).
severity_weight(dengue, headache, 1.0).
severity_weight(dengue, joint_pain, 1.2).
severity_weight(dengue, muscle_pain, 1.0).
severity_weight(dengue, rash, 1.2).
severity_weight(dengue, nausea, 1.0).
severity_weight(dengue, vomiting, 1.0).
severity_weight(dengue, swollen_glands, 1.0).
severity_weight(typhoid, fever, 1.0).
severity_weight(typhoid, headache, 1.0).
severity_weight(typhoid, fatigue, 1.0).
severity_weight(typhoid, nausea, 1.0).
severity_weight(typhoid, vomiting, 1.0).
severity_weight(typhoid, diarrhea, 1.0).
severity_weight(typhoid, loss_of_appetite, 1.0).
severity_weight(typhoid, abdominal_pain, 1.0).
severity_weight(migraine, headache, 1.0).
severity_weight(migraine, nausea, 1.0).
severity_weight(migraine, vomiting, 1.0).
severity_weight(migraine, blurred_vision, 1.0).
severity_weight(migraine, dizziness, 1.0).
severity_weight(migraine, sensitivity_to_light, 1.3).
severity_weight(asthma, shortness_of_breath, 1.0).
severity_weight(asthma, wheezing, 1.0).
severity_weight(asthma, chest_pain, 1.0).
severity_weight(asthma, cough, 1.0).
severity_weight(asthma, fatigue, 1.0).
severity_weight(pneumonia, fever, 1.0).
severity_weight(pneumonia, cough, 1.0).
severity_weight(pneumonia, shortness_of_breath, 1.4).
severity_weight(pneumonia, chest_pain, 1.3).
severity_weight(pneumonia, fatigue, 1.0).
severity_weight(pneumonia, chills, 1.0).
severity_weight(pneumonia, sweating, 1.0).
severity_weight(pneumonia, nausea, 1.0).
severity_weight(diabetes, frequent_urination, 1.3).
severity_weight(diabetes, increased_thirst, 1.3).
severity_weight(diabetes, fatigue, 1.0).
severity_weight(diabetes, blurred_vision, 1.0).
severity_weight(diabetes, weight_loss, 1.0).
severity_weight(diabetes, slow_healing_wounds, 1.0).
severity_weight(diabetes, excessive_hunger, 1.0).
severity_weight(diabetes, mouth_ulcers, 1.0).
severity_weight(diabetes, gum_bleeding, 1.0).
severity_weight(diabetes, frequent_infections, 1.0).
severity_weight(hypertension, headache, 1.0).
severity_weight(hypertension, dizziness, 1.0).
severity_weight(hypertension, chest_pain, 1.0).
severity_weight(hypertension, shortness_of_breath, 1.0).
severity_weight(hypertension, blurred_vision, 1.0).
severity_weight(hypertension, leg_pain_walking, 1.0).
severity_weight(anemia, fatigue, 1.0).
severity_weight(anemia, pale_skin, 1.0).
severity_weight(anemia, dizziness, 1.0).
severity_weight(anemia, shortness_of_breath, 1.0).
severity_weight(anemia, cold_hands_and_feet, 1.0).
severity_weight(anemia, headache, 1.0).
severity_weight(anemia, rapid_heartbeat, 1.0).
severity_weight(allergy, sneezing, 1.0).
severity_weight(allergy, itchy_eyes, 1.0).
severity_weight(allergy, runny_nose, 1.0).
severity_weight(allergy, rash, 1.0).
severity_weight(allergy, cough, 1.0).
severity_weight(allergy, nasal_congestion, 1.0).
severity_weight(chickenpox, fever, 1.0).
severity_weight(chickenpox, rash, 1.0).
severity_weight(chickenpox, fatigue, 1.0).
severity_weight(chickenpox, headache, 1.0).
severity_weight(chickenpox, loss_of_appetite, 1.0).
severity_weight(chickenpox, boils, 1.0).
severity_weight(chickenpox, peeling_skin, 1.0).
severity_weight(measles, fever, 1.0).
severity_weight(measles, rash, 1.0).
severity_weight(measles, cough, 1.0).
severity_weight(measles, runny_nose, 1.0).
severity_weight(measles, red_eyes, 1.0).
severity_weight(measles, fatigue, 1.0).
severity_weight(hepatitis_a, fever, 1.0).
severity_weight(hepatitis_a, fatigue, 1.0).
severity_weight(hepatitis_a, nausea, 1.0).
severity_weight(hepatitis_a, vomiting, 1.0).
severity_weight(hepatitis_a, abdominal_pain, 1.0).
severity_weight(hepatitis_a, yellowing_of_skin, 1.5).
severity_weight(hepatitis_a, loss_of_appetite, 1.0).
severity_weight(hepatitis_a, dark_urine, 1.0).
severity_weight(hepatitis_a, pale_stool, 1.0).
severity_weight(tuberculosis, cough, 1.0).
severity_weight(tuberculosis, fever, 1.0).
severity_weight(tuberculosis, night_sweats, 1.3).
severity_weight(tuberculosis, weight_loss, 1.0).
severity_weight(tuberculosis, fatigue, 1.0).
severity_weight(tuberculosis, chest_pain, 1.0).
severity_weight(tuberculosis, coughing_blood, 1.5).
severity_weight(bronchitis, cough, 1.0).
severity_weight(bronchitis, fatigue, 1.0).
severity_weight(bronchitis, chest_pain, 1.0).
severity_weight(bronchitis, shortness_of_breath, 1.0).
severity_weight(bronchitis, wheezing, 1.0).
severity_weight(bronchitis, fever, 1.0).
severity_weight(sinusitis, facial_pain, 1.0).
severity_weight(sinusitis, nasal_congestion, 1.0).
severity_weight(sinusitis, headache, 1.0).
severity_weight(sinusitis, runny_nose, 1.0).
severity_weight(sinusitis, fatigue, 1.0).
severity_weight(sinusitis, fever, 1.0).
severity_weight(sinusitis, tooth_pain, 1.0).
severity_weight(urinary_tract_infection, burning_urination, 1.4).
severity_weight(urinary_tract_infection, frequent_urination, 1.0).
severity_weight(urinary_tract_infection, abdominal_pain, 1.0).
severity_weight(urinary_tract_infection, blood_in_urine, 1.3).
severity_weight(urinary_tract_infection, fever, 1.0).
severity_weight(urinary_tract_infection, difficulty_urinating, 1.0).
severity_weight(urinary_tract_infection, urinary_urgency, 1.0).
severity_weight(gastroenteritis, diarrhea, 1.0).
severity_weight(gastroenteritis, vomiting, 1.0).
severity_weight(gastroenteritis, nausea, 1.0).
severity_weight(gastroenteritis, abdominal_pain, 1.0).
severity_weight(gastroenteritis, fever, 1.0).
severity_weight(gastroenteritis, bloating, 1.0).
severity_weight(heat_stroke, fever, 1.0).
severity_weight(heat_stroke, headache, 1.0).
severity_weight(heat_stroke, dizziness, 1.0).
severity_weight(heat_stroke, nausea, 1.0).
severity_weight(heat_stroke, confusion, 1.5).
severity_weight(heat_stroke, rapid_heartbeat, 1.3).
severity_weight(insomnia, insomnia, 1.0).
severity_weight(insomnia, fatigue, 1.0).
severity_weight(insomnia, headache, 1.0).
severity_weight(insomnia, difficulty_concentrating, 1.0).
severity_weight(insomnia, dizziness, 1.0).
severity_weight(depression, sadness, 1.0).
severity_weight(depression, loss_of_interest, 1.0).
severity_weight(depression, fatigue, 1.0).
severity_weight(depression, insomnia, 1.0).
severity_weight(depression, difficulty_concentrating, 1.0).
severity_weight(depression, loss_of_appetite, 1.0).
severity_weight(depression, panic_attacks, 1.0).
severity_weight(arthritis, joint_pain, 1.0).
severity_weight(arthritis, stiff_joints, 1.0).
severity_weight(arthritis, fatigue, 1.0).
severity_weight(arthritis, back_pain, 1.0).
severity_weight(arthritis, muscle_pain, 1.0).
severity_weight(arthritis, knee_pain, 1.0).
severity_weight(arthritis, shoulder_pain, 1.0).
severity_weight(gerd, heartburn, 1.5).
severity_weight(gerd, chest_pain, 1.2).
severity_weight(gerd, nausea, 1.0).
severity_weight(gerd, bloating, 1.0).
severity_weight(gerd, sore_throat, 1.0).
severity_weight(gerd, cough, 1.0).
severity_weight(gerd, abdominal_distension, 1.0).
severity_weight(tension_headache, headache, 1.5).
severity_weight(tension_headache, neck_pain, 1.2).
severity_weight(tension_headache, irritability, 1.0).
severity_weight(tension_headache, difficulty_concentrating, 1.0).
severity_weight(mononucleosis, fever, 1.0).
severity_weight(mononucleosis, sore_throat, 1.3).
severity_weight(mononucleosis, fatigue, 1.0).
severity_weight(mononucleosis, swollen_glands, 1.3).
severity_weight(mononucleosis, headache, 1.0).
severity_weight(mononucleosis, rash, 1.0).
severity_weight(mononucleosis, loss_of_appetite, 1.0).
severity_weight(conjunctivitis, red_eyes, 1.4).
severity_weight(conjunctivitis, itchy_eyes, 1.3).
severity_weight(conjunctivitis, eye_discharge, 1.3).
severity_weight(conjunctivitis, eye_pain, 1.0).
severity_weight(conjunctivitis, swollen_glands, 1.0).
severity_weight(otitis_media, ear_pain, 1.5).
severity_weight(otitis_media, fever, 1.2).
severity_weight(otitis_media, hearing_loss, 1.0).
severity_weight(otitis_media, ear_discharge, 1.0).
severity_weight(otitis_media, irritability, 1.0).
severity_weight(otitis_media, difficulty_concentrating, 1.0).
severity_weight(laryngitis, hoarseness, 1.5).
severity_weight(laryngitis, sore_throat, 1.2).
severity_weight(laryngitis, cough, 1.0).
severity_weight(laryngitis, fever, 1.0).
severity_weight(laryngitis, difficulty_concentrating, 1.0).
severity_weight(laryngitis, throat_swelling, 1.0).
severity_weight(appendicitis, abdominal_pain, 1.5).
severity_weight(appendicitis, nausea, 1.0).
severity_weight(appendicitis, vomiting, 1.0).
severity_weight(appendicitis, fever, 1.0).
severity_weight(appendicitis, loss_of_appetite, 1.0).
severity_weight(appendicitis, bloating, 1.0).
severity_weight(kidney_stones, abdominal_pain, 1.4).
severity_weight(kidney_stones, blood_in_urine, 1.3).
severity_weight(kidney_stones, nausea, 1.0).
severity_weight(kidney_stones, vomiting, 1.0).
severity_weight(kidney_stones, burning_urination, 1.0).
severity_weight(kidney_stones, frequent_urination, 1.0).
severity_weight(stroke, confusion, 1.4).
severity_weight(stroke, numbness, 1.3).
severity_weight(stroke, blurred_vision, 1.2).
severity_weight(stroke, difficulty_concentrating, 1.0).
severity_weight(stroke, loss_of_consciousness, 1.0).
severity_weight(stroke, dizziness, 1.0).
severity_weight(stroke, double_vision, 1.0).
severity_weight(stroke, memory_problems, 1.0).
severity_weight(heart_attack, chest_pain, 1.5).
severity_weight(heart_attack, shortness_of_breath, 1.4).
severity_weight(heart_attack, rapid_heartbeat, 1.3).
severity_weight(heart_attack, sweating, 1.0).
severity_weight(heart_attack, nausea, 1.0).
severity_weight(heart_attack, dizziness, 1.0).
severity_weight(heart_attack, swollen_ankles, 1.0).
severity_weight(copd, shortness_of_breath, 1.4).
severity_weight(copd, cough, 1.0).
severity_weight(copd, wheezing, 1.3).
severity_weight(copd, fatigue, 1.0).
severity_weight(copd, chest_pain, 1.0).
severity_weight(copd, rapid_breathing, 1.0).
severity_weight(copd, slow_heartbeat, 1.0).
severity_weight(hypothyroidism, fatigue, 1.0).
severity_weight(hypothyroidism, weight_gain, 1.2).
severity_weight(hypothyroidism, sensitivity_to_cold, 1.3).
severity_weight(hypothyroidism, dry_skin, 1.1).
severity_weight(hypothyroidism, constipation, 1.0).
severity_weight(hypothyroidism, sadness, 1.0).
severity_weight(hypothyroidism, hair_loss, 1.0).
severity_weight(hypothyroidism, muscle_pain, 1.0).
severity_weight(hypothyroidism, muscle_cramps, 1.0).
severity_weight(hypothyroidism, skin_discoloration, 1.0).
severity_weight(hyperthyroidism, weight_loss, 1.2).
severity_weight(hyperthyroidism, rapid_heartbeat, 1.3).
severity_weight(hyperthyroidism, anxiety, 1.0).
severity_weight(hyperthyroidism, tremors, 1.2).
severity_weight(hyperthyroidism, sensitivity_to_heat, 1.0).
severity_weight(hyperthyroidism, sweating, 1.0).
severity_weight(hyperthyroidism, difficulty_concentrating, 1.0).
severity_weight(hyperthyroidism, insomnia, 1.0).
severity_weight(gout, joint_pain, 1.5).
severity_weight(gout, joint_swelling, 1.4).
severity_weight(gout, red_eyes, 1.0).
severity_weight(gout, fever, 1.0).
severity_weight(gout, fatigue, 1.0).
severity_weight(fibromyalgia, muscle_pain, 1.3).
severity_weight(fibromyalgia, joint_pain, 1.0).
severity_weight(fibromyalgia, fatigue, 1.2).
severity_weight(fibromyalgia, insomnia, 1.0).
severity_weight(fibromyalgia, difficulty_concentrating, 1.1).
severity_weight(fibromyalgia, headache, 1.0).
severity_weight(fibromyalgia, sadness, 1.0).
severity_weight(fibromyalgia, anxiety, 1.0).
severity_weight(fibromyalgia, tinnitus, 1.0).
severity_weight(fibromyalgia, muscle_cramps, 1.0).
severity_weight(ibs, abdominal_pain, 1.3).
severity_weight(ibs, bloating, 1.2).
severity_weight(ibs, diarrhea, 1.0).
severity_weight(ibs, constipation, 1.0).
severity_weight(ibs, nausea, 1.0).
severity_weight(ibs, fatigue, 1.0).
severity_weight(ibs, abdominal_distension, 1.0).
severity_weight(diverticulitis, abdominal_pain, 1.4).
severity_weight(diverticulitis, fever, 1.0).
severity_weight(diverticulitis, nausea, 1.0).
severity_weight(diverticulitis, vomiting, 1.0).
severity_weight(diverticulitis, bloating, 1.0).
severity_weight(diverticulitis, constipation, 1.0).
severity_weight(pancreatitis, abdominal_pain, 1.5).
severity_weight(pancreatitis, nausea, 1.0).
severity_weight(pancreatitis, vomiting, 1.0).
severity_weight(pancreatitis, fever, 1.0).
severity_weight(pancreatitis, rapid_heartbeat, 1.0).
severity_weight(pancreatitis, bloating, 1.0).
severity_weight(cholecystitis, abdominal_pain, 1.4).
severity_weight(cholecystitis, nausea, 1.0).
severity_weight(cholecystitis, vomiting, 1.0).
severity_weight(cholecystitis, fever, 1.0).
severity_weight(cholecystitis, bloating, 1.0).
severity_weight(cholecystitis, loss_of_appetite, 1.0).
severity_weight(cholecystitis, yellowing_of_skin, 1.0).
severity_weight(cholecystitis, dark_urine, 1.0).
severity_weight(lupus, fatigue, 1.0).
severity_weight(lupus, joint_pain, 1.2).
severity_weight(lupus, rash, 1.3).
severity_weight(lupus, fever, 1.0).
severity_weight(lupus, hair_loss, 1.1).
severity_weight(lupus, sensitivity_to_cold, 1.0).
severity_weight(lupus, difficulty_concentrating, 1.0).
severity_weight(lupus, muscle_pain, 1.0).
severity_weight(lupus, bruising_easily, 1.0).
severity_weight(lupus, frequent_infections, 1.0).
severity_weight(lupus, skin_lesions, 1.0).
severity_weight(rheumatoid_arthritis, joint_pain, 1.4).
severity_weight(rheumatoid_arthritis, joint_swelling, 1.3).
severity_weight(rheumatoid_arthritis, stiff_joints, 1.2).
severity_weight(rheumatoid_arthritis, fatigue, 1.0).
severity_weight(rheumatoid_arthritis, fever, 1.0).
severity_weight(rheumatoid_arthritis, muscle_pain, 1.0).
severity_weight(multiple_sclerosis, numbness, 1.3).
severity_weight(multiple_sclerosis, blurred_vision, 1.2).
severity_weight(multiple_sclerosis, fatigue, 1.0).
severity_weight(multiple_sclerosis, difficulty_concentrating, 1.1).
severity_weight(multiple_sclerosis, muscle_pain, 1.0).
severity_weight(multiple_sclerosis, dizziness, 1.0).
severity_weight(multiple_sclerosis, mood_swings, 1.0).
severity_weight(parkinsons, tremors, 1.5).
severity_weight(parkinsons, stiff_joints, 1.3).
severity_weight(parkinsons, difficulty_concentrating, 1.0).
severity_weight(parkinsons, dizziness, 1.0).
severity_weight(parkinsons, sadness, 1.0).
severity_weight(parkinsons, fatigue, 1.0).
severity_weight(parkinsons, memory_problems, 1.0).
severity_weight(epilepsy, seizure, 1.5).
severity_weight(epilepsy, confusion, 1.0).
severity_weight(epilepsy, fatigue, 1.0).
severity_weight(epilepsy, loss_of_consciousness, 1.0).
severity_weight(epilepsy, difficulty_concentrating, 1.0).
severity_weight(epilepsy, memory_problems, 1.0).
severity_weight(chronic_fatigue_syndrome, fatigue, 1.5).
severity_weight(chronic_fatigue_syndrome, headache, 1.0).
severity_weight(chronic_fatigue_syndrome, joint_pain, 1.0).
severity_weight(chronic_fatigue_syndrome, difficulty_concentrating, 1.2).
severity_weight(chronic_fatigue_syndrome, insomnia, 1.0).
severity_weight(chronic_fatigue_syndrome, muscle_pain, 1.0).
severity_weight(chronic_fatigue_syndrome, sore_throat, 1.0).
severity_weight(chronic_fatigue_syndrome, swollen_glands, 1.0).
severity_weight(chronic_fatigue_syndrome, nosebleed, 1.0).
severity_weight(food_poisoning, nausea, 1.0).
severity_weight(food_poisoning, vomiting, 1.3).
severity_weight(food_poisoning, diarrhea, 1.3).
severity_weight(food_poisoning, abdominal_pain, 1.0).
severity_weight(food_poisoning, fever, 1.0).
severity_weight(food_poisoning, chills, 1.0).
severity_weight(food_poisoning, fatigue, 1.0).
severity_weight(whooping_cough, cough, 1.5).
severity_weight(whooping_cough, sore_throat, 1.0).
severity_weight(whooping_cough, runny_nose, 1.0).
severity_weight(whooping_cough, fever, 1.0).
severity_weight(whooping_cough, fatigue, 1.0).
severity_weight(whooping_cough, vomiting, 1.0).
severity_weight(scarlet_fever, fever, 1.0).
severity_weight(scarlet_fever, rash, 1.4).
severity_weight(scarlet_fever, sore_throat, 1.3).
severity_weight(scarlet_fever, headache, 1.0).
severity_weight(scarlet_fever, nausea, 1.0).
severity_weight(scarlet_fever, swollen_glands, 1.0).
severity_weight(celiac_disease, diarrhea, 1.2).
severity_weight(celiac_disease, bloating, 1.2).
severity_weight(celiac_disease, abdominal_pain, 1.1).
severity_weight(celiac_disease, fatigue, 1.0).
severity_weight(celiac_disease, weight_loss, 1.0).
severity_weight(celiac_disease, pale_skin, 1.0).
severity_weight(celiac_disease, joint_pain, 1.0).
severity_weight(celiac_disease, rash, 1.0).
severity_weight(hemorrhoids, blood_in_stool, 1.3).
severity_weight(hemorrhoids, abdominal_pain, 1.0).
severity_weight(hemorrhoids, itchy_skin, 1.0).
severity_weight(hemorrhoids, pale_stool, 1.0).

% Age-based risk factors
risk_factor(flu, age, child).
risk_factor(flu, age, elderly).
risk_factor(covid19, age, elderly).
risk_factor(pneumonia, age, child).
risk_factor(pneumonia, age, elderly).
risk_factor(diabetes, age, middle_aged).
risk_factor(diabetes, age, elderly).
risk_factor(hypertension, age, middle_aged).
risk_factor(hypertension, age, elderly).
risk_factor(arthritis, age, elderly).
risk_factor(gerd, age, middle_aged).
risk_factor(gerd, age, elderly).
risk_factor(mononucleosis, age, adolescent).
risk_factor(mononucleosis, age, adult).
risk_factor(otitis_media, age, child).
risk_factor(appendicitis, age, adolescent).
risk_factor(appendicitis, age, adult).
risk_factor(kidney_stones, age, adult).
risk_factor(kidney_stones, age, middle_aged).
risk_factor(stroke, age, middle_aged).
risk_factor(stroke, age, elderly).
risk_factor(heart_attack, age, middle_aged).
risk_factor(heart_attack, age, elderly).
risk_factor(copd, age, middle_aged).
risk_factor(copd, age, elderly).
risk_factor(hypothyroidism, age, middle_aged).
risk_factor(hypothyroidism, age, elderly).
risk_factor(hyperthyroidism, age, adult).
risk_factor(hyperthyroidism, age, middle_aged).
risk_factor(gout, age, middle_aged).
risk_factor(gout, age, elderly).
risk_factor(fibromyalgia, age, adult).
risk_factor(fibromyalgia, age, middle_aged).
risk_factor(diverticulitis, age, middle_aged).
risk_factor(diverticulitis, age, elderly).
risk_factor(pancreatitis, age, adult).
risk_factor(pancreatitis, age, middle_aged).
risk_factor(cholecystitis, age, adult).
risk_factor(cholecystitis, age, middle_aged).
risk_factor(lupus, age, adult).
risk_factor(lupus, age, middle_aged).
risk_factor(rheumatoid_arthritis, age, middle_aged).
risk_factor(rheumatoid_arthritis, age, elderly).
risk_factor(multiple_sclerosis, age, adult).
risk_factor(multiple_sclerosis, age, middle_aged).
risk_factor(parkinsons, age, middle_aged).
risk_factor(parkinsons, age, elderly).
risk_factor(epilepsy, age, child).
risk_factor(epilepsy, age, adolescent).
risk_factor(chronic_fatigue_syndrome, age, adult).
risk_factor(chronic_fatigue_syndrome, age, middle_aged).
risk_factor(whooping_cough, age, child).
risk_factor(scarlet_fever, age, child).
risk_factor(hemorrhoids, age, middle_aged).
risk_factor(hemorrhoids, age, elderly).

% ------------------- GENERATED FACTS (END) -------------------

% ------------------- Severity Scaling (user-reported severity) -------------------
% The GUI lets the patient rate each reported symptom Mild/Moderate/Severe.
% These factors scale that symptom's contribution to the confidence score.
severity_factor(mild, 0.8).
severity_factor(moderate, 1.0).
severity_factor(severe, 1.25).

% ------------------- Counts over Dynamic Patient Facts -------------------
% The controller asserts patient_has(Symptom) and patient_sev(Symptom, Severity)
% before running a diagnosis.

total_symptoms(Disease, Count) :-
    findall(S, has_symptom(Disease, S), Symptoms),
    length(Symptoms, Count).

matched_symptoms(Disease, Count) :-
    findall(S, (has_symptom(Disease, S), patient_has(S)), Matched),
    length(Matched, Count).

possible_disease(Disease) :-
    disease(Disease),
    matched_symptoms(Disease, Count),
    Count >= 2.

% ------------------- Confidence Calculation -------------------
% Confidence is the patient's severity-weighted symptom score divided by the
% disease's total (equally defaulted) weight, so the result can never exceed
% 100%, even when every symptom is reported as severe.

total_weight(Disease, Denominator) :-
    findall(Weight,
            (has_symptom(Disease, Symptom), severity_weight(Disease, Symptom, Weight)),
            Weights),
    sum_list(Weights, Denominator).

matched_weight(Disease, Numerator) :-
    findall(Weight,
            (has_symptom(Disease, Symptom),
             patient_has(Symptom),
             severity_weight(Disease, Symptom, Base),
             (patient_sev(Symptom, Severity) -> severity_factor(Severity, Factor) ; Factor = 1.0),
             Weight is Base * Factor),
            Weights),
    sum_list(Weights, Numerator).

confidence(Disease, Percentage) :-
    matched_weight(Disease, Numerator),
    total_weight(Disease, Denominator),
    Denominator > 0,
    Raw is round((Numerator / Denominator) * 100),
    (Raw > 100 -> Percentage = 100 ; Percentage = Raw).

% ------------------- Knowledge Base Accessors -------------------
get_disease_symptoms(Disease, Symptoms) :-
    findall(Symptom, has_symptom(Disease, Symptom), Symptoms).

get_all_diseases(Diseases) :-
    findall(Disease, disease(Disease), Diseases).

get_all_symptoms(Symptoms) :-
    findall(Symptom, symptom(Symptom), Symptoms).
